---
description: Create new application command. Triggers App Builder skill and starts interactive dialogue with user.
---

# /create - Create Application

$ARGUMENTS

---

## Task

This command starts a new application creation process.

### Steps:

1. **Request Analysis**
   - Understand what the user wants
   - If information is missing, use `conversation-manager` skill to ask

2. **Project Planning**
   - Use `project-planner` agent for task breakdown
   - Determine tech stack
   - Plan file structure
   - Create plan file and proceed to building

3. **Application Building (After Approval)**
   - Orchestrate with `app-builder` skill
   - Coordinate expert agents:
     - `database-architect` → Schema
     - `backend-specialist` → API
     - `frontend-specialist` → UI

4. **Preview**
   - Start with `auto_preview.py` when complete
   - Present URL to user

---

## Usage Examples

```
/create blog site
/create e-commerce app with product listing and cart
/create todo app
/create Instagram clone
/create crm system with customer management
```

---

## Before Starting

If request is unclear, ask these questions:
- What type of application?
- What are the basic features?
- Who will use it?

Use defaults, add details later.


## 🧭 Routing + Memory + Gate (NEW)

### 1) Route confidence first

```bash
python .agent/scripts/routing_score.py "$ARGUMENTS"
```

### 2) Log key architecture decision (ADR)

```bash
python .agent/scripts/knowledge_manager.py add   --type adr   --title "initial stack decision"   --content "Document chosen stack and rationale for this create flow"
```

### 3) Run final delivery quality gate

```bash
python .agent/scripts/quality_gate.py   --input .agent/quality/sample.json   --profile deploy   --thresholds .agent/quality/thresholds.json
```
