"""Xác minh artifact bắt buộc trước khi nộp bài Day 22."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).parent.parent
EVIDENCE = ROOT / "evidence"
REQUIRED = [
    "01_langsmith_traces.png",
    "02_prompt_hub.png",
    "02_ab_routing_log.txt",
    "03_ragas_scores.png",
    "03_ragas_report.json",
    "04_pii_demo_log.txt",
    "04_json_demo_log.txt",
]


def main() -> None:
    failures = []
    for name in REQUIRED:
        path = EVIDENCE / name
        if not path.exists() or path.stat().st_size == 0:
            failures.append(f"Thiếu evidence/{name}")

    report_path = ROOT / "data" / "ragas_report.json"
    if not report_path.exists():
        failures.append("Thiếu data/ragas_report.json")
    else:
        report = json.loads(report_path.read_text(encoding="utf-8"))
        for version in ("prompt_v1_scores", "prompt_v2_scores"):
            scores = report.get(version, {})
            for metric in (
                "faithfulness", "answer_relevancy", "context_recall", "context_precision"
            ):
                if metric not in scores:
                    failures.append(f"{version} thiếu {metric}")
        best = max(
            report["prompt_v1_scores"]["faithfulness"],
            report["prompt_v2_scores"]["faithfulness"],
        )
        if best < 0.8:
            failures.append(f"Faithfulness {best:.4f} < 0.8")

    ab_log = EVIDENCE / "02_ab_routing_log.txt"
    if ab_log.exists():
        text = ab_log.read_text(encoding="utf-8")
        routed = re.findall(r"^\[\d{2}\] \[prompt-v[12]\]", text, re.MULTILINE)
        if len(routed) != 50:
            failures.append(f"A/B log có {len(routed)}/50 dòng routing")
        if "[prompt-v1]" not in text or "[prompt-v2]" not in text:
            failures.append("A/B log chưa có đủ cả V1 và V2")

    run_all_log = EVIDENCE / "05_run_all_log.txt"
    if not run_all_log.exists() or run_all_log.stat().st_size == 0:
        failures.append("Thiếu evidence/05_run_all_log.txt")
    else:
        run_all_text = run_all_log.read_text(encoding="utf-8")
        for step in range(1, 5):
            marker = f"✅ PASS  Bước {step}:"
            if marker not in run_all_text:
                failures.append(f"Run-all log thiếu trạng thái PASS của Bước {step}")

    if failures:
        print("❌ VERIFY FAIL")
        for failure in failures:
            print(f"  - {failure}")
        raise SystemExit(1)

    print(
        "✅ VERIFY PASS: đủ 7 evidence bắt buộc, run_all 4/4 PASS, "
        "report hợp lệ, routing đủ 50 dòng"
    )


if __name__ == "__main__":
    main()
