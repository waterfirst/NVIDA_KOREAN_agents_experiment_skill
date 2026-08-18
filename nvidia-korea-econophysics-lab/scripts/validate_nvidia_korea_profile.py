#!/usr/bin/env python3
"""Validate an aggregate NVIDIA Korea profile and reject narrative fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from profile_contract import validate_profile


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", type=Path, help="검증할 집계 JSON")
    parser.add_argument("--strict", action="store_true", help="경고도 실패로 처리")
    parser.add_argument("--report", type=Path, help="검증 보고서 JSON 저장 경로")
    args = parser.parse_args()

    try:
        profile = json.loads(args.profile.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"프로필을 읽을 수 없습니다: {exc}") from exc

    errors, warnings, summary = validate_profile(profile)
    report = {
        "valid": not errors and not (args.strict and warnings),
        "errors": errors,
        "warnings": warnings,
        "summary": summary,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    print(rendered)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered + "\n", encoding="utf-8")
    if errors or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
