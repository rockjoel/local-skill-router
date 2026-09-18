# local-skill-router

**Local-first skill router for coding agents** (Cursor, Claude Code, Codex, …).

Too many agent skills → wasted context tokens and wrong skill loads.  
This tool picks **at most one** skill — or **`none`** — using a small catalog you control.

- **Default: offline** (no API, milliseconds)
- **Prefer `none`** over a wrong match
- **Optional** second pass with a semantic judge (e.g. [TypeSafe Jev](https://typesafe.ai)) — not required
- **You own the catalog** — do not paste untrusted third-party skill bodies into always-on prompts

Inspired by the *idea* of selective rule/skill injection (not a fork of any plugin).

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

Edit `examples/catalog.md` (or pass `--catalog path/to/your.md`).

## How it works

1. **Greeting / empty** → `none`
2. **Alias hit** (keywords in the catalog) → that skill
3. **Token overlap** with the “when” column → best skill, or `none` if weak / ambiguous
4. Agent opens **one** `SKILL.md` (or none). Never glob the whole skills folder.

## Optional: semantic judge (Jev)

Wire your own call if local returns `none` / `ambiguous`. Keep **fail-open**: if the API is down, keep the local result.  
This repo intentionally ships **without** API keys or vendor lock-in.

## Agent skill (optional)

Copy `agent/SKILL.md` into your agent skills folder if you want the agent to run the CLI when unsure.

## Why this is useful (portfolio angle)

| Common approach | This approach |
|---|---|
| Always-on mega-rules | Thin always-on + route on demand |
| Load many skills “just in case” | Max **one** skill or **none** |
| Cloud ranking every turn | Local first; cloud optional |
| Trust random GitHub skill dumps | Catalog is yours; treat foreign skills as untrusted data |

## License

MIT — see [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Forks and pull requests welcome.
