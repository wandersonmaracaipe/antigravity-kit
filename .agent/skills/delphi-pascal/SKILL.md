---
name: delphi-pascal
description: Delphi/Object Pascal engineering patterns for legacy and modern codebases. Focuses on maintainability, memory safety, component architecture, and migration strategy.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Delphi / Pascal

> Prioritize safe modernization over risky rewrites.

## 1) Context Split

- Legacy VCL desktop maintenance
- Modernization toward newer Delphi versions / modular architecture
- Interop with external services (REST, DB, message systems)

## 2) Code Organization

- Keep units cohesive by domain
- Separate UI event handlers from business logic
- Encapsulate data access and external integration boundaries

## 3) Memory & Resource Safety

- Prefer clear ownership rules
- Avoid leaks in object lifecycle paths
- Ensure deterministic cleanup of resources (DB, files, sockets)
- Validate exception safety in constructor/destructor flows

## 4) Refactoring Strategy for Legacy

- Characterization tests before behavior changes
- Small, reversible refactors
- Replace global state progressively
- Introduce interfaces where substitution/testing is needed

## 5) Interop & Modernization

- Wrap legacy modules behind stable service boundaries
- Gradually adopt modern language/compiler features when safe
- Prioritize risk-based migration (critical modules first)

## 6) Anti-Patterns

- Big-bang rewrite of mission-critical systems
- Business rules hidden inside form event handlers
- Global mutable state with implicit side effects
- Silent exception swallowing
