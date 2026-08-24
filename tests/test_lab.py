"""Kiểm thử cục bộ các gate không cần gọi API bên ngoài."""

import ast
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))


def load_step(filename: str, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, SRC / filename)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class LabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.step2 = load_step("02_prompt_hub_ab_routing.py", "step2")
        cls.step3 = load_step("03_ragas_evaluation.py", "step3")
        cls.step4 = load_step("04_guardrails_validator.py", "step4")

    def test_no_executable_ellipsis_remains(self):
        for path in SRC.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            ellipses = [
                node for node in ast.walk(tree)
                if isinstance(node, ast.Constant) and node.value is Ellipsis
            ]
            self.assertEqual(ellipses, [], f"Còn Ellipsis trong {path.name}")

    def test_ab_routing_is_deterministic_and_uses_both_versions(self):
        ids = [f"req-{index:04d}" for index in range(50)]
        first = [self.step2.get_prompt_version(request_id) for request_id in ids]
        second = [self.step2.get_prompt_version(request_id) for request_id in ids]
        self.assertEqual(first, second)
        self.assertEqual(set(first), {self.step2.PROMPT_V1_NAME, self.step2.PROMPT_V2_NAME})

    def test_ragas_dataset_has_required_fields(self):
        rows = [{
            "question": "question",
            "reference": "reference",
            "answer": "answer",
            "contexts": ["context one", "context two"],
        }]
        dataset = self.step3.build_ragas_dataset(rows)
        sample = dataset.samples[0]
        self.assertEqual(sample.user_input, "question")
        self.assertEqual(sample.response, "answer")
        self.assertEqual(sample.reference, "reference")
        self.assertEqual(sample.retrieved_contexts, ["context one", "context two"])

    def test_pii_patterns_cover_four_types(self):
        samples = {
            "EMAIL": "john.doe@example.com",
            "PHONE": "(555) 867-5309",
            "SSN": "123-45-6789",
            "CREDIT_CARD": "4532 1234 5678 9010",
        }
        import re
        for pii_type, value in samples.items():
            self.assertRegex(value, self.step4.PIIDetector.PII_PATTERNS[pii_type])

    def test_json_repair_handles_all_required_cases(self):
        cases = [
            '```json\n{"name": "Bob"}\n```',
            "{'name': 'Charlie', 'score': 95}",
            '{"key": "value",}',
        ]
        for value in cases:
            repaired = self.step4.JSONFormatter._repair(value)
            self.assertIsInstance(json.loads(repaired), dict)


if __name__ == "__main__":
    unittest.main()
