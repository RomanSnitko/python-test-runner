# python-test-runner
Each test case is represented by a set of input and expected-output files. The test runner launches the target executable as an isolated subprocess, redirects its standard streams, enforces a configurable execution timeout, and captures stdout and stderr without decoding the raw byte streams. The resulting output is compared against the expected data together with the process exit code.

The execution layer is isolated from the comparison and reporting logic. A dedicated test-case loader converts filesystem-based test definitions into immutable data objects, the executor manages subprocess lifecycle and timeout handling, the comparator performs deterministic output validation, and the reporter aggregates individual results into structured pass/fail information with explicit failure causes such as output mismatch, runtime error, or timeout.

The runner relies exclusively on the Python standard library, using subprocess and process signals for execution control, dataclasses for test-case representation, and pathlib for filesystem operations. The modular design keeps process management, validation, error handling, and CLI orchestration independent, allowing the runner to execute arbitrary native binaries without coupling the framework to a specific target language or build system.

## Tech Stack
* Core: Python 3.10+ (Modern Syntax).
* System: subprocess (Process management), signal (IPC).
* Data Structures: dataclasses (Immutable test case definitions).
* Filesystem: pathlib (Cross-platform path handling).
* Concepts: OOP, Separation of Concerns, Stream Redirection, Exception Handling.

## Project Structure
Проект следует принципам модульной архитектуры, отделяя логику исполнения от CLI-интерфейса.

```text
python-test-runner/
├── runner/                 # Core logic package
│   ├── __init__.py         # Package marker
│   ├── test_case.py        # DTO for test scenarios (.in/.out/.rc parsing)
│   ├── executor.py         # Subprocess wrapper & timeout logic
│   ├── comparator.py       # Byte-stream comparison logic
│   ├── reporter.py         # Console output formatter
│   └── errors.py           # Custom exception hierarchy
├── tests/                  # Integration tests & Example C++ binaries
├── cli.py                  # Argument parsing logic
├── main.py                 # Application entry point & orchestration
├── .gitignore              # Build artifacts exclusion
└── README.md               # Project documentation
```

## Quick Start
Инструмент не требует установки зависимостей. Достаточно наличие Python 3.8+.
### 1. Clone the repository

```Bash
git clone https://github.com/RomanSnitko/python-test-runner.git
cd python-test-runner
```

### 2. Prepare Test Cases
Тесты организуются в папке. Имя файла определяет входные и эталонные данные:
test01.in — Входные данные (stdin)
test01.out — Ожидаемый вывод (stdout)
test01.err — (Опционально) Ожидаемый stderr
test01.rc — (Опционально) Ожидаемый код возврата (default: 0)

### 3. Usage

```Bash
# Basic usage: python main.py <executable> <tests_directory>
python main.py ./my_cpp_program ./tests
# With custom timeout (in seconds)
python main.py ./solver ./tests --timeout 1.0
```

# Example Output

```Text
[PASS] 01_simple
[PASS] 02_edge_case
[FAIL] 03_overflow
  return code mismatch: expected 0, got 139 (SIGSEGV)
[FAIL] 04_infinite_loop
  timeout (limit: 2.0s)
[PASS] 05_performance

Summary:
  Passed: 3
  Failed: 2
```

## Architecture Details
* Test Case Loader (test_case.py): Автоматически сканирует указанную директорию, сопоставляет файлы .in, .out, .rc по префиксу и собирает их в иммутабельные объекты TestCase.
* Executor (executor.py): Обертка над subprocess.run. Перехватывает TimeoutExpired, обеспечивает корректное завершение дочерних процессов и захватывает потоки байтов без декодирования (для поддержки любых кодировок).
* Comparator (comparator.py): Чистая функция сравнения. Реализует логику строгого соответствия или ignore-trailing-whitespace (в планах). Генерирует объект ComparisonResult с причиной расхождения.

## Requirements
* OS: Cross-platform (Linux/Windows/macOS).
* Runtime: Python 3.8 or newer.
* Target: Любой исполняемый файл (C++, C, Rust, Go binary).
