#!/usr/bin/env python3
"""Shared schema validation for privacy-preserving NVIDIA Korea profiles."""

from __future__ import annotations

from collections import Counter
from typing import Any

SCHEMA_VERSION = 1
DATASET_ID = "nvidia/Nemotron-Personas-Korea"
REQUIRED_ROOT = {
    "schemaVersion",
    "source",
    "dataset",
    "datasetVersion",
    "license",
    "sampleSize",
    "retainedSampleSize",
    "strata",
}
ALLOWED_ROOT = REQUIRED_ROOT | {
    "suppressedSampleSize",
    "sourceDigestSha256",
    "aggregation",
    "dataPolicy",
    "limitations",
}
STRATUM_FIELDS = {"ageGroup", "sex", "region", "education", "occupation", "count"}
AGE_GROUPS = {"19-29", "30-39", "40-49", "50-64", "65-74", "75-99", "미상"}
UNKNOWN_LABELS = {"", "미상", "unknown", "none", "null", "n/a"}
FORBIDDEN_KEY_FRAGMENTS = {
    "uuid",
    "name",
    "persona",
    "cultural_background",
    "skills_and_expertise",
    "hobbies",
    "interests",
    "career_goals",
    "ambitions",
}


def _is_positive_int(value: Any) -> bool:
    return type(value) is int and value > 0


def _walk_keys(value: Any, prefix: str = "") -> list[str]:
    keys: list[str] = []
    if isinstance(value, dict):
        for raw_key, child in value.items():
            key = str(raw_key)
            path = f"{prefix}.{key}" if prefix else key
            keys.append(path)
            keys.extend(_walk_keys(child, path))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            keys.extend(_walk_keys(child, f"{prefix}[{index}]"))
    return keys


def validate_profile(profile: Any) -> tuple[list[str], list[str], dict[str, Any]]:
    errors: list[str] = []
    warnings: list[str] = []
    summary: dict[str, Any] = {}

    if not isinstance(profile, dict):
        return ["루트는 JSON 객체여야 합니다."], warnings, summary

    keys = set(profile)
    missing = sorted(REQUIRED_ROOT - keys)
    unexpected = sorted(keys - ALLOWED_ROOT)
    if missing:
        errors.append(f"필수 루트 키 누락: {', '.join(missing)}")
    if unexpected:
        errors.append(f"허용되지 않은 루트 키: {', '.join(unexpected)}")

    forbidden_paths = [
        path
        for path in _walk_keys(profile)
        if any(fragment in path.rsplit(".", 1)[-1].lower() for fragment in FORBIDDEN_KEY_FRAGMENTS)
    ]
    if forbidden_paths:
        errors.append(f"식별자·서술형 필드가 포함됨: {', '.join(forbidden_paths[:8])}")

    if profile.get("schemaVersion") != SCHEMA_VERSION:
        errors.append(f"schemaVersion은 {SCHEMA_VERSION}이어야 합니다.")
    if profile.get("dataset") != DATASET_ID:
        errors.append(f"dataset은 {DATASET_ID}이어야 합니다.")
    if "CC BY 4.0" not in str(profile.get("license", "")).upper():
        errors.append("license에 CC BY 4.0이 명시되어야 합니다.")

    sample_size = profile.get("sampleSize")
    retained_size = profile.get("retainedSampleSize")
    if not _is_positive_int(sample_size):
        errors.append("sampleSize는 양의 정수여야 합니다.")
    if not _is_positive_int(retained_size):
        errors.append("retainedSampleSize는 양의 정수여야 합니다.")
    if _is_positive_int(sample_size) and sample_size < 100:
        warnings.append("sampleSize가 100 미만이어서 연구용 분포로는 너무 작습니다.")

    strata = profile.get("strata")
    if not isinstance(strata, list) or not strata:
        errors.append("strata는 하나 이상의 층을 가진 배열이어야 합니다.")
        return errors, warnings, summary

    total = 0
    unknown_total = 0
    signatures: Counter[tuple[str, ...]] = Counter()
    max_count = 0
    for index, item in enumerate(strata):
        if not isinstance(item, dict):
            errors.append(f"strata[{index}]는 객체여야 합니다.")
            continue
        item_keys = set(item)
        if item_keys != STRATUM_FIELDS:
            missing_item = sorted(STRATUM_FIELDS - item_keys)
            extra_item = sorted(item_keys - STRATUM_FIELDS)
            if missing_item:
                errors.append(f"strata[{index}] 키 누락: {', '.join(missing_item)}")
            if extra_item:
                errors.append(f"strata[{index}] 허용되지 않은 키: {', '.join(extra_item)}")
            continue
        count = item["count"]
        if not _is_positive_int(count):
            errors.append(f"strata[{index}].count는 양의 정수여야 합니다.")
            continue
        if item["ageGroup"] not in AGE_GROUPS:
            errors.append(f"strata[{index}].ageGroup 값이 허용 범위 밖입니다: {item['ageGroup']}")
        dimensions = tuple(str(item[field]).strip() for field in ("ageGroup", "sex", "region", "education", "occupation"))
        if any(not value for value in dimensions):
            errors.append(f"strata[{index}]의 차원 값은 빈 문자열일 수 없습니다.")
        signatures[dimensions] += 1
        total += count
        max_count = max(max_count, count)
        if any(value.lower() in UNKNOWN_LABELS for value in dimensions):
            unknown_total += count

    duplicates = sum(amount - 1 for amount in signatures.values() if amount > 1)
    if duplicates:
        errors.append(f"동일한 층 조합이 {duplicates}개 중복되었습니다.")
    if _is_positive_int(retained_size) and total != retained_size:
        errors.append(f"strata count 합계({total})가 retainedSampleSize({retained_size})와 다릅니다.")
    if _is_positive_int(sample_size) and _is_positive_int(retained_size) and retained_size > sample_size:
        errors.append("retainedSampleSize는 sampleSize를 초과할 수 없습니다.")

    suppressed = profile.get("suppressedSampleSize")
    if suppressed is not None:
        if type(suppressed) is not int or suppressed < 0:
            errors.append("suppressedSampleSize는 0 이상의 정수여야 합니다.")
        elif _is_positive_int(sample_size) and _is_positive_int(retained_size) and suppressed != sample_size - retained_size:
            errors.append("suppressedSampleSize가 sampleSize-retainedSampleSize와 다릅니다.")

    if total:
        unknown_share = unknown_total / total
        dominant_share = max_count / total
        summary.update(
            strataCount=len(strata),
            retainedCount=total,
            unknownShare=round(unknown_share, 6),
            dominantStratumShare=round(dominant_share, 6),
        )
        if unknown_share > 0.05:
            warnings.append(f"미상 값 포함 비중이 {unknown_share:.1%}로 높습니다.")
        if dominant_share > 0.50:
            warnings.append(f"최대 단일 층 비중이 {dominant_share:.1%}로 높습니다.")

    limitations = profile.get("limitations")
    if not isinstance(limitations, list) or not limitations:
        warnings.append("limitations 배열에 합성자료·독립성·비인과 한계를 기록하십시오.")

    return errors, warnings, summary
