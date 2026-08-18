#!/usr/bin/env python3
"""Stream NVIDIA Korean personas into a minimal, validated aggregate profile."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Iterator

from profile_contract import DATASET_ID, SCHEMA_VERSION, validate_profile

DATASET_VERSION = "1.0"
ALIASES = {
    "age": ("age", "age_years", "current_age"),
    "sex": ("sex", "gender", "biological_sex"),
    "region": ("province", "region", "sido", "residence_province"),
    "education": ("education_level", "education", "highest_education"),
    "occupation": ("occupation", "job", "profession", "detailed_occupation"),
}
PROVINCES = {
    "서울": "서울", "부산": "부산", "대구": "대구", "인천": "인천", "광주": "광주",
    "대전": "대전", "울산": "울산", "세종": "세종", "경기": "경기", "강원": "강원",
    "충북": "충북", "충청북": "충북", "충남": "충남", "충청남": "충남",
    "전북": "전북", "전라북": "전북", "전남": "전남", "전라남": "전남",
    "경북": "경북", "경상북": "경북", "경남": "경남", "경상남": "경남", "제주": "제주",
}


def clean(value: Any) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text or "미상"


def pick(row: dict[str, Any], field: str) -> Any:
    lowered = {str(key).lower(): value for key, value in row.items()}
    for alias in ALIASES[field]:
        value = lowered.get(alias)
        if value not in (None, ""):
            return value
    return "미상"


def age_group(value: Any) -> str:
    if type(value) in (int, float):
        age = int(value)
    else:
        digits = re.findall(r"\d+", clean(value))
        if not digits:
            return "미상"
        age = int(digits[0])
    if age < 19 or age > 120:
        return "미상"
    if age < 30:
        return "19-29"
    if age < 40:
        return "30-39"
    if age < 50:
        return "40-49"
    if age < 65:
        return "50-64"
    if age < 75:
        return "65-74"
    return "75-99"


def normalize_sex(value: Any) -> str:
    text = clean(value).lower()
    if text in {"m", "male", "man", "남", "남성"}:
        return "남성"
    if text in {"f", "female", "woman", "여", "여성"}:
        return "여성"
    return clean(value)


def normalize_province(value: Any) -> str:
    text = clean(value)
    if text == "미상":
        return text
    for token, label in sorted(PROVINCES.items(), key=lambda item: len(item[0]), reverse=True):
        if token in text:
            return label
    return text


def macro_region(province: str) -> str:
    if province in {"서울", "경기", "인천"}:
        return "수도권"
    if province in {"충북", "충남", "대전", "세종"}:
        return "충청권"
    if province in {"전북", "전남", "광주"}:
        return "호남권"
    if province in {"경북", "경남", "부산", "대구", "울산"}:
        return "영남권"
    if province in {"강원", "제주"}:
        return "강원·제주"
    return province


def normalize_education(value: Any) -> str:
    text = clean(value)
    if text == "미상":
        return text
    rules = (
        (("박사",), "박사"),
        (("석사", "대학원"), "대학원"),
        (("학사", "대학교", "4년제"), "대학교"),
        (("전문대", "2년제", "3년제"), "전문대"),
        (("고등", "고졸"), "고등학교"),
        (("중학", "중졸"), "중학교"),
        (("초등", "초졸"), "초등학교"),
        (("무학",), "무학"),
    )
    for tokens, label in rules:
        if any(token in text for token in tokens):
            return label
    return text


def broad_occupation(value: Any) -> str:
    text = clean(value)
    if text == "미상":
        return text
    rules = (
        (("군인",), "군인"),
        (("관리자", "임원", "경영"), "관리자"),
        (("연구", "교수", "교사", "의사", "약사", "변호", "전문가", "엔지니어", "개발자", "과학"), "전문가·기술직"),
        (("사무", "행정", "회계", "금융", "보험"), "사무·행정"),
        (("서비스", "돌봄", "간호", "보육", "요양", "미용", "조리"), "서비스·돌봄"),
        (("판매", "영업", "매장"), "판매"),
        (("농", "임업", "어업", "축산"), "농림어업"),
        (("기능", "숙련", "건설", "정비", "용접"), "기능·건설"),
        (("장치", "기계", "조립", "운전", "생산", "제조"), "장치·기계·생산"),
        (("단순", "노무", "청소", "배달"), "단순노무"),
        (("학생", "무직", "은퇴", "퇴직", "주부"), "비경제활동"),
    )
    for tokens, label in rules:
        if any(token in text for token in tokens):
            return label
    return "기타"


def local_jsonl(path: Path, limit: int) -> Iterator[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        for index, line in enumerate(handle):
            if index >= limit:
                break
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path}:{index + 1}은 JSON 객체가 아닙니다.")
            yield value


def huggingface_rows(dataset: str, split: str, limit: int) -> Iterator[dict[str, Any]]:
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise SystemExit("Hugging Face 스트리밍에는 `pip install datasets`가 필요합니다.") from exc
    stream = load_dataset(dataset, split=split, streaming=True)
    for index, row in enumerate(stream):
        if index >= limit:
            break
        yield row


def aggregate(
    records: Iterable[dict[str, Any]],
    region_mode: str,
    occupation_mode: str,
) -> tuple[Counter[tuple[str, ...]], int, str]:
    counts: Counter[tuple[str, ...]] = Counter()
    digest = hashlib.sha256()
    total = 0
    for row in records:
        province = normalize_province(pick(row, "region"))
        region = macro_region(province) if region_mode == "macro" else province
        occupation_raw = clean(pick(row, "occupation"))
        occupation = broad_occupation(occupation_raw) if occupation_mode == "broad" else occupation_raw
        key = (
            age_group(pick(row, "age")),
            normalize_sex(pick(row, "sex")),
            region,
            normalize_education(pick(row, "education")),
            occupation,
        )
        counts[key] += 1
        digest.update(("\x1f".join(key) + "\n").encode("utf-8"))
        total += 1
    return counts, total, digest.hexdigest()


def build_payload(
    counts: Counter[tuple[str, ...]],
    total: int,
    digest: str,
    dataset: str,
    dataset_version: str,
    region_mode: str,
    occupation_mode: str,
    min_cell: int,
) -> dict[str, Any]:
    retained = [(key, count) for key, count in counts.items() if count >= min_cell]
    retained.sort(key=lambda item: item[0])
    retained_size = sum(count for _, count in retained)
    return {
        "schemaVersion": SCHEMA_VERSION,
        "source": "NVIDIA Nemotron-Personas-Korea",
        "dataset": dataset,
        "datasetVersion": dataset_version,
        "license": "CC BY 4.0",
        "sampleSize": total,
        "retainedSampleSize": retained_size,
        "suppressedSampleSize": total - retained_size,
        "sourceDigestSha256": digest,
        "aggregation": {
            "dimensions": ["ageGroup", "sex", "region", "education", "occupation"],
            "regionMode": region_mode,
            "occupationMode": occupation_mode,
            "minimumCell": min_cell,
        },
        "dataPolicy": {
            "retainedSourceFields": ["age", "sex", "province", "education_level", "occupation"],
            "discarded": ["uuid", "persona and all *_persona fields", "narrative attributes"],
            "individualRecordsExported": False,
        },
        "strata": [
            {
                "ageGroup": key[0],
                "sex": key[1],
                "region": key[2],
                "education": key[3],
                "occupation": key[4],
                "count": count,
            }
            for key, count in retained
        ],
        "limitations": [
            "NVIDIA records are fully synthetic and are not survey respondents or real people.",
            "The dataset card documents independence assumptions that can distort joint distributions.",
            "Audit and reweight against current Korean official statistics before empirical interpretation.",
            "Do not infer public opinion, individual behavior, or causal policy effects from this profile.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=100_000, help="최대 스트리밍 레코드 수")
    parser.add_argument("--input-jsonl", type=Path, help="Hugging Face 대신 사용할 로컬 JSONL")
    parser.add_argument("--dataset", default=DATASET_ID)
    parser.add_argument("--dataset-version", default=DATASET_VERSION)
    parser.add_argument("--split", default="train")
    parser.add_argument("--region-mode", choices=("province", "macro"), default="province")
    parser.add_argument("--occupation-mode", choices=("broad", "raw"), default="broad")
    parser.add_argument("--min-cell", type=int, default=5, help="이 값 미만인 층은 출력에서 제외")
    parser.add_argument("--output", type=Path, default=Path("data/nvidia-korea-profile.json"))
    args = parser.parse_args()

    if args.rows < 1:
        raise SystemExit("--rows는 1 이상이어야 합니다.")
    if args.min_cell < 1:
        raise SystemExit("--min-cell은 1 이상이어야 합니다.")
    records = local_jsonl(args.input_jsonl, args.rows) if args.input_jsonl else huggingface_rows(args.dataset, args.split, args.rows)
    try:
        counts, total, digest = aggregate(records, args.region_mode, args.occupation_mode)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"입력 데이터를 처리할 수 없습니다: {exc}") from exc
    if not total:
        raise SystemExit("입력에서 레코드를 읽지 못했습니다.")

    payload = build_payload(
        counts, total, digest, args.dataset, args.dataset_version,
        args.region_mode, args.occupation_mode, args.min_cell,
    )
    errors, warnings, summary = validate_profile(payload)
    if errors:
        raise SystemExit("프로필 검증 실패: " + "; ".join(errors))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "warnings": warnings, **summary}, ensure_ascii=False))


if __name__ == "__main__":
    main()
