from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class TestReport:
    name: str
    passed: bool
    reason: str


def print_report(reports: List[TestReport]) -> None:
    passed = 0
    failed = 0

    for report in reports:
        if report.passed:
            print(f"[PASS] {report.name}")
            passed += 1
        else:
            print(f"[FAIL] {report.name}")
            print(f"  {report.reason}")
            failed += 1

    print()
    print("Summary:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
