# local-skill-router

**Local-first skill router for coding agents** (Cursor, Claude Code, Codex, …).

> Phase 1 of every agent setup: *“I’ll just add one more skill.”*  
> Phase 2: the context window looks like lasagna.  
> Phase 3: this repo.

If you’ve ever watched an agent politely load **twelve** playbooks for “hi”, burn a pile of tokens, and still pick the wrong one — welcome. You’re among friends.

This tool picks **at most one** skill — or proudly returns **`none`** — from a small catalog **you** control.

- **Default: offline** (no API, milliseconds — your wallet can breathe)
- **Prefer `none`** over a wrong match (silence is a feature)
- **Thin always-on** mindset: don’t pay rent on rules you don’t need every turn
- **Optional** second pass with a semantic judge (e.g. [TypeSafe Jev](https://typesafe.ai)) when local is unsure — not required
- **You own the catalog** — random GitHub skill dumps are *data*, not gospel (prompt injection is a thing)

Inspired by the *idea* of selective rule/skill injection — not a fork of any plugin, and not “install everything, hope for the best.”

## The plot twist (short version)

Stacking skills feels productive. Until it doesn’t.  
Everything starts to mush together: overlapping triggers, stale instructions, always-on bloat, mysterious loops.

What helped here: treat routing as a **decision**, not as “paste more markdown into every chat.”  
Local rules first. A typed judge (Jev / System One–style) only when the easy path is ambiguous. Fail open if the cloud naps.

I’m oddly proud of how boring that sounds. Boring is how you keep tokens.

## Quickstart

```bash
python tests/test_router.py
python -m skill_router.router "got a 429 on download"
python -m skill_router.router "hello"
```

Example output:

```json
{
  "ok": true,
  "skill": "rate-limit-helper",
  "reason": "alias",
  "provider": "local",
  "candidates": ["rate-limit-helper"]
}
```

`"hello"` → `none`. The agent can just say hello. Revolutionary.

Edit `examples/catalog.md` (or pass `--catalog path/to/your.md`).

## How it works

1. **Greeting / empty** → `none`
2. **Alias hit** (keywords in the catalog) → that skill
3. **Token overlap** with the “when” column → best skill, or `none` if weak / ambiguous
4. Agent opens **one** `SKILL.md` (or none). Never glob the whole skills folder like it’s an all-you-can-eat buffet.

## Optional: semantic judge (Jev)

Wire your own call if local returns `none` / `ambiguous`. Keep **fail-open**: if the API is down, keep the local result.  
This repo ships **without** API keys or vendor lock-in on purpose.

## Agent skill (optional)

Copy `agent/SKILL.md` into your agent skills folder if you want the agent to run the CLI when unsure.

## Why this beats “skill maximalism”

| The lasagna path | This path |
|---|---|
| Always-on mega-rules | Thin always-on + route on demand |
| Load many skills “just in case” | Max **one** skill or **none** |
| Cloud ranking every turn | Local first; cloud optional |
| Trust random GitHub skill dumps | Catalog is yours; foreign text is untrusted |

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Forks and pull requests welcome.  
If you open a PR that adds “always load 40 skills”, I will gently send you back to Phase 1.
