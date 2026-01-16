from pathlib import Path

from cli import parse_args
from runner.test_case import TestCase
from runner.executor import execute
from runner.comparator import compare
from runner.reporter import TestReport, print_report
from runner.errors import InvalidTestDirectory


def main():
    args = parse_args()
    test_dir = Path(args.tests)

    if not test_dir.exists() or not test_dir.is_dir():
        raise InvalidTestDirectory(test_dir)

    base_names = sorted({p.stem for p in test_dir.glob("*.in")})
    reports = []

    for name in base_names:
        test = TestCase.from_directory(test_dir, name, args.timeout)
        result = execute(args.program, test.input_data, test.timeout)

        if result.timeout:
            reports.append(
                TestReport(
                    name=name,
                    passed=False,
                    reason="timeout",
                )
            )
            continue

        comparison = compare(
            actual_stdout=result.stdout,
            actual_stderr=result.stderr,
            actual_returncode=result.returncode,
            expected_stdout=test.expected_stdout,
            expected_stderr=test.expected_stderr,
            expected_returncode=test.expected_returncode,
        )

        reports.append(
            TestReport(
                name=name,
                passed=comparison.success,
                reason=comparison.reason or "",
            )
        )

    print_report(reports)


if __name__ == "__main__":
    main()
