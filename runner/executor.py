import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ExecutionResult:
    stdout: bytes
    stderr: bytes
    returncode: int
    timeout: bool


def execute(
        program: str,
        input_data: bytes,
        timeout: float
) -> ExecutionResult:
    try:
        completed = subprocess.run(
            [program],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return ExecutionResult(
            stdout=completed.stdout,
            stderr=completed.stderr,
            returncode=completed.returncode,
            timeout=False,
        )
    except subprocess.TimeoutExpired as e:
        return ExecutionResult(
            stdout=e.stdout or b"",
            stderr=e.stderr or b"",
            returncode=-1,
            timeout=True,
        )
