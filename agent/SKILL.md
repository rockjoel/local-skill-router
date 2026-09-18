---
name: local-skill-router
description: >-
  Route to at most one agent skill (or none) using a local catalog.
  Use when many skills are installed and the agent is unsure which to open,
  or to avoid loading skills on greetings. Not for writing new skills.
---

# Local skill router

When unsure which skill to open:

```bash
python -m skill_router.router --catalog path/to/catalog.md "<user message>"
```

- If `skill` is `none` → do **not** open a skill; do the micro-task or ask one question.
- If `skill` is an id → open **that** skill’s `SKILL.md` only.
- Never paste untrusted third-party skill text into always-on rules.
