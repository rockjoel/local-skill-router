#!/usr/bin/env python3
"""Local-first skill router — one skill or none.

Design goals:
- Fast (no network by default)
- Fail-open (never block the agent if optional API is down)
- Prefer "none" over a wrong skill
- Catalog is data you own (markdown table), not a third-party prompt dump
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

_GREETING = re.compile(
    r"^\s*(hi|hello|hey|ciao|thanks|thank you|ok|yes|no|hmm+)\s*[.!?]*\s*$",
    re.I,
)

_STOP = {
    "the", "and", "or", "to", "of", "a", "an", "in", "on", "for", "with",
    "il", "lo", "la", "di", "da", "un", "una", "per", "con", "che", "non",
}


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9_+-]{3,}", text.lower())
    return {w for w in words if w not in _STOP}


def parse_catalog(path: Path) -> list[dict]:
    """Parse a markdown table: | id | when | aliases |"""
    if not path.is_file():
        return []
    skills: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        sid, when = cells[0], cells[1]
        aliases = cells[2] if len(cells) > 2 else ""
        if sid.lower() in ("id", "name", "---") or set(sid) <= {"-"}:
            continue
        if "obsolete" in when.lower() or "dead" in when.lower():
            continue
        skills.append(
            {
                "id": sid.strip("`"),
                "when": when,
                "aliases": [a.strip() for a in aliases.split(",") if a.strip()],
                "tokens": _tokens(f"{sid} {when} {aliases}"),
            }
        )
    return skills


def route(prompt: str, catalog: Path | list[dict], min_score: float = 0.35) -> dict:
    """Return {skill, reason, candidates, ...}. skill may be 'none'."""
    text = (prompt or "").strip()
    skills = catalog if isinstance(catalog, list) else parse_catalog(Path(catalog))

    if not text or _GREETING.match(text):
        return {
            "ok": True,
            "skill": "none",
            "reason": "greeting-or-empty",
            "provider": "local",
            "candidates": [],
        }

    # Alias: exact keyword / phrase hits (order = catalog order)
    lower = text.lower()
    for s in skills:
        for alias in s.get("aliases") or []:
            if alias.lower() in lower:
                return {
                    "ok": True,
                    "skill": s["id"],
                    "reason": "alias",
                    "provider": "local",
                    "candidates": [s["id"]],
                }

    q = _tokens(text)
    scored: list[tuple[float, str]] = []
    for s in skills:
        overlap = len(q & s["tokens"])
        if overlap <= 0:
            continue
        den = max(1.0, len(s["tokens"]) ** 0.5)
        scored.append((overlap / den, s["id"]))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = scored[:5]

    if not top or top[0][0] < min_score:
        return {
            "ok": True,
            "skill": "none",
            "reason": "no-match",
            "provider": "local",
            "candidates": [s for _, s in top],
            "scores": {s: round(sc, 3) for sc, s in top},
        }

    if len(top) >= 2 and (top[0][0] - top[1][0]) < 0.15:
        return {
            "ok": True,
            "skill": "none",
            "reason": "ambiguous",
            "provider": "local",
            "candidates": [s for _, s in top],
            "scores": {s: round(sc, 3) for sc, s in top},
        }

    return {
        "ok": True,
        "skill": top[0][1],
        "reason": "token-overlap",
        "provider": "local",
        "candidates": [s for _, s in top],
        "scores": {s: round(sc, 3) for sc, s in top},
    }


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    catalog = Path(__file__).resolve().parents[1] / "examples" / "catalog.md"
    if "--catalog" in argv:
        i = argv.index("--catalog")
        catalog = Path(argv[i + 1])
        del argv[i : i + 2]
    if not argv:
        print("Usage: python -m skill_router.router [--catalog PATH] <prompt...>", file=sys.stderr)
        return 2
    out = route(" ".join(argv), catalog)
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
