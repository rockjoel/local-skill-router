#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from skill_router.router import route, parse_catalog  # noqa: E402

CAT = ROOT / "examples" / "catalog.md"


def expect(cond: bool, msg: str) -> None:
    if not cond:
        raise SystemExit(f"FAIL: {msg}")


def main() -> int:
    skills = parse_catalog(CAT)
    expect(len(skills) >= 4, "catalog parses")

    r = route("hello", CAT)
    expect(r["skill"] == "none", "greeting→none")

    r = route("got a 429 on download", CAT)
    expect(r["skill"] == "rate-limit-helper", "429→rate-limit")

    r = route("please commit and push", CAT)
    expect(r["skill"] == "git-publish", "commit→git-publish")

    r = route("refactor one helper function", CAT)
    expect(r["skill"] == "none", "micro-fix→none")

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
