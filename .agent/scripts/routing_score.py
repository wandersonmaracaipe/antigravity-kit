#!/usr/bin/env python3
"""
Routing Score Engine
--------------------
Scores user intent by domain and returns structured routing output:
- request_type
- selected_agents
- confidence
- needs_clarification
- clarifying_questions
- suggested_workflow
- rationale

Usage:
  python .agent/scripts/routing_score.py "build secure login api"
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass
class DomainRule:
    domain: str
    agent: str
    keywords: tuple[str, ...]
    weight: float = 1.0


RULES: tuple[DomainRule, ...] = (
    DomainRule("security", "security-auditor", ("security", "auth", "jwt", "password", "token", "vulnerability"), 1.2),
    DomainRule("backend", "backend-specialist", ("api", "endpoint", "server", "laravel", "php", "golang", "go", "fastapi", "node"), 1.1),
    DomainRule("frontend", "frontend-specialist", ("ui", "frontend", "component", "react", "css", "tailwind"), 1.0),
    DomainRule("mobile", "mobile-developer", ("flutter", "react native", "android", "ios", "mobile"), 1.0),
    DomainRule("database", "database-architect", ("database", "schema", "migration", "sql", "prisma"), 1.0),
    DomainRule("testing", "test-engineer", ("test", "e2e", "coverage", "unit test"), 0.9),
    DomainRule("devops", "devops-engineer", ("deploy", "docker", "ci/cd", "kubernetes", "pipeline"), 0.9),
    DomainRule("legacy", "code-archaeologist", ("legacy", "refactor", "delphi", "pascal", "spaghetti"), 1.0),
)

REQUEST_TYPE_PATTERNS = {
    "question": ("what", "how", "why", "explain", "qual", "como", "por que"),
    "bugfix": ("fix", "bug", "error", "quebrado", "corrigir"),
    "new_feature": ("build", "create", "implement", "adicionar", "criar", "fazer"),
    "review": ("review", "audit", "analyze", "analisar", "revisar"),
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9\-\+]+", text.lower())


def classify_request_type(text: str) -> str:
    joined = " ".join(tokenize(text))
    scores = {}
    for typ, kws in REQUEST_TYPE_PATTERNS.items():
        scores[typ] = sum(1 for kw in kws if kw in joined)
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else "general"


def suggest_workflow(request_type: str, multi_domain: bool) -> str:
    if request_type == "question":
        return "direct-answer"
    if request_type == "review":
        return "/status" if not multi_domain else "/orchestrate"
    if request_type == "bugfix":
        return "/debug" if multi_domain else "/test"
    if request_type == "new_feature":
        return "/create" if not multi_domain else "/orchestrate"
    return "/plan" if multi_domain else "direct-answer"


def build_clarifying_questions(multi_domain: bool, request_type: str, selected_agents: list[str], max_questions: int) -> list[str]:
    qs: list[str] = []
    if request_type == "new_feature":
        qs.append("Qual é o objetivo principal e o escopo mínimo desta entrega?")
    if "backend-specialist" in selected_agents:
        qs.append("Você prefere stack específica (Laravel, Go, Node, Python)?")
    if "mobile-developer" in selected_agents:
        qs.append("O alvo é iOS, Android ou ambos?")
    if multi_domain:
        qs.append("Qual prioridade: velocidade, qualidade, segurança ou prazo?")
    return qs[: max(max_questions, 0)]


def score_text(text: str, max_questions: int = 2, include_debug: bool = False) -> dict:
    tokens = tokenize(text)
    joined = " ".join(tokens)
    domain_scores: dict[str, float] = {}
    agent_scores: dict[str, float] = {}

    for rule in RULES:
        hits = sum(1 for kw in rule.keywords if kw in joined)
        if hits == 0:
            continue
        score = hits * rule.weight
        domain_scores[rule.domain] = domain_scores.get(rule.domain, 0.0) + score
        agent_scores[rule.agent] = agent_scores.get(rule.agent, 0.0) + score

    request_type = classify_request_type(text)

    if not agent_scores:
        return {
            "request_type": request_type,
            "selected_agents": [],
            "confidence": 0.0,
            "needs_clarification": True,
            "suggested_workflow": "direct-answer",
        }

    ranked = sorted(agent_scores.items(), key=lambda x: x[1], reverse=True)
    top_score = ranked[0][1]
    total = sum(agent_scores.values()) or 1.0
    confidence = round(top_score / total, 2)

    multi_domain = len([d for d, s in domain_scores.items() if s > 0]) > 1
    selected = [ranked[0][0]]
    if multi_domain:
        selected = [name for name, _ in ranked[:3]]

    needs_clarification = confidence < 0.55 or request_type in {"new_feature", "review"}
    rationale = (
        "Needs clarification for safer routing and better execution quality."
        if needs_clarification
        else "Routing confidence acceptable."
    )

    result = {
        "request_type": request_type,
        "selected_agents": selected,
        "confidence": confidence,
        "needs_clarification": needs_clarification,
        "suggested_workflow": suggest_workflow(request_type, multi_domain),
    }
    if needs_clarification:
        result["clarifying_questions"] = build_clarifying_questions(multi_domain, request_type, selected, max_questions)
    if include_debug:
        result["rationale"] = rationale
        result["domain_scores"] = domain_scores
    return result


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Score request and suggest best agent/workflow")
    parser.add_argument("request", nargs="+", help="User request text")
    parser.add_argument("--max-questions", type=int, default=2, help="Max clarifying questions in output")
    parser.add_argument("--verbose", action="store_true", help="Include rationale/domain_scores debug fields")
    args = parser.parse_args()

    text = " ".join(args.request).strip()
    print(json.dumps(score_text(text, max_questions=args.max_questions, include_debug=args.verbose), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
