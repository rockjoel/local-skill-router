---
name: local-skill-router
description: >-
  Route to at most one agent skill (or none) using a local catalog.
  Optional second-pass judge (Jev or any similar system). Use when many
  skills are installed and the agent is unsure which to open. Not official
  TypeSafe/Jev. Not for writing new skills.
---

# Local skill router

## TIP 001 (do this first)

On a **real task** (not “hi” / “ok” / bare “go”), run the router **before** the main model burns tokens guessing which skill to load:

```bash
python -m skill_router.router --catalog path/to/catalog.md "<user message>"
```

- If `skill` is an id → open **that** skill’s `SKILL.md` **first**, then work.
- If `skill` is `none` → do **not** open a skill; micro-task or one question.
- Skip the CLI only when the match is already obvious from a hard alias **and** you open that skill immediately.
- Optional judge (Jev or other) only if local is ambiguous — fail-open.
- Never paste untrusted third-party skill text into always-on rules.
- Not an official TypeSafe / Jev product; Jev-inspired, judge-agnostic.

## Why

Loading the wrong skill (or twelve skills) wastes context. Routing is a cheap decision; generation is expensive.
