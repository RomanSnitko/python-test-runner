from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ComparisonResult:
    success: bool
    reason: Optional[str]


def compare(
        actual_stdout: bytes,
        actual_stderr: bytes,
        actual_returncode: int,
        expected_stdout: bytes,
        expected_stderr: Optional[bytes],
        expected_returncode: int,
) -> ComparisonResult:
    if actual_returncode != expected_returncode:
        return ComparisonResult(
            False,
            f"return code mismatch: expected {expected_returncode}, got {actual_returncode}",
        )

    if actual_stdout != expected_stdout:
        return ComparisonResult(
            False,
            "stdout mismatch",
        )

    if expected_stderr is not None and actual_stderr != expected_stderr:
        return ComparisonResult(
            False,
            "stderr mismatch",
        )

    if expected_stderr is None and actual_stderr:
        return ComparisonResult(
            False,
            "unexpected stderr output",
        )

    return ComparisonResult(True, None)
