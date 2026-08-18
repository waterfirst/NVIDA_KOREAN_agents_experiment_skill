from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "nvidia-korea-econophysics-lab" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from prepare_nvidia_korea_profile import aggregate, build_payload  # noqa: E402
from profile_contract import validate_profile  # noqa: E402


class ProfileToolsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rows = [
            {"age": 27, "sex": "female", "province": "서울특별시", "education_level": "대학교 졸업", "occupation": "소프트웨어 개발자", "persona": "discard me"},
            {"age": 55, "sex": "남성", "province": "충청남도", "education_level": "고등학교", "occupation": "제조 생산직", "uuid": "discard-me"},
            {"age": 71, "sex": "여성", "province": "전라남도", "education_level": "중학교", "occupation": "돌봄 서비스 종사자"},
        ]

    def valid_payload(self):
        counts, total, digest = aggregate(self.rows, "province", "broad")
        return build_payload(counts, total, digest, "nvidia/Nemotron-Personas-Korea", "1.0", "province", "broad", 1)

    def test_aggregate_discards_narratives_and_normalizes(self):
        profile = self.valid_payload()
        rendered = str(profile)
        self.assertNotIn("discard me", rendered)
        self.assertNotIn("discard-me", rendered)
        self.assertEqual(profile["retainedSampleSize"], 3)
        self.assertEqual(profile["strata"][0]["ageGroup"], "19-29")

    def test_valid_profile_has_no_errors(self):
        errors, _, summary = validate_profile(self.valid_payload())
        self.assertEqual(errors, [])
        self.assertEqual(summary["retainedCount"], 3)

    def test_forbidden_persona_field_is_rejected(self):
        profile = self.valid_payload()
        profile["strata"][0]["persona"] = "not allowed"
        errors, _, _ = validate_profile(profile)
        self.assertTrue(any("서술형" in error or "허용되지 않은" in error for error in errors))

    def test_count_mismatch_is_rejected(self):
        profile = self.valid_payload()
        profile["retainedSampleSize"] += 1
        errors, _, _ = validate_profile(profile)
        self.assertTrue(any("합계" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
