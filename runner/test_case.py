from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class TestCase:
    name: str
    input_data: bytes
    expected_stdout: bytes
    expected_stderr: Optional[bytes]
    expected_returncode: int
    timeout: float

    @staticmethod
    def from_directory(test_dir: Path, base_name: str, timeout: float = 2.0) -> "TestCase":
        inp = test_dir / f"{base_name}.in"
        out = test_dir / f"{base_name}.out"
        err = test_dir / f"{base_name}.err"
        rc = test_dir / f"{base_name}.rc"

        if not inp.exists():
            raise FileNotFoundError(inp)
        if not out.exists():
            raise FileNotFoundError(out)

        input_data = inp.read_bytes()
        expected_stdout = out.read_bytes()
        expected_stderr = err.read_bytes() if err.exists() else None
        expected_returncode = int(rc.read_text().strip()) if rc.exists() else 0

        return TestCase(
            name=base_name,
            input_data=input_data,
            expected_stdout=expected_stdout,
            expected_stderr=expected_stderr,
            expected_returncode=expected_returncode,
            timeout=timeout,
        )
