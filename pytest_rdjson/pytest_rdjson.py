"""Convert pytest report json to rdjson for reviewdog."""

import json
from typing import Any

PYTEST_SEVERITY_ERROR = "ERROR"
PYTEST_SEVERITY_WARNING = "WARNING"

TEST_OUTCOME_FAILED = "failed"


def _get_rdjson_entry(
    message: str,
    severity: str,
    path: str,
    line_start: int,
    line_end: int,
    col_start: int = 1,
    col_end: int = 1,
) -> dict[str, Any]:
    return {
        "message": message,
        "severity": severity,
        "location": {
            "path": path,
            "range": {
                "start": {
                    "line": line_start,
                    "column": col_start,
                },
                "end": {
                    "line": line_end,
                    "column": col_end,
                },
            },
        },
    }


def pytest_to_rdjson(file_path: str) -> str:
    """Convert the given file_path pytest report JSON file, to rdjson for reviewdog."""
    rdjson: dict[str, str | Any] = {
        "source": {"name": "pytest", "url": "https://github.com/pytest-dev/pytest"},
        "severity": PYTEST_SEVERITY_WARNING,
        "diagnostics": None,
    }
    rdjson["diagnostics"] = []

    with open(file_path) as f:
        pytest_report = json.load(f)

        # Construct tests output
        if "tests" in pytest_report:
            for test_result in pytest_report["tests"]:
                test_result_outcome = test_result["outcome"]
                if test_result_outcome != TEST_OUTCOME_FAILED:
                    continue

                crash_report = test_result["call"]["crash"]
                crash_path = crash_report["path"]
                crash_line = crash_report["lineno"]

                # construct a message using markdown, to display the traceback
                test_message = "Traceback:"
                traceback = test_result["call"]["traceback"]
                for trace in traceback:
                    trace_path = trace["path"]
                    trace_line = trace["lineno"]
                    trace_message = trace["message"]

                    traceback_message = (
                        f"""\n\t- Location: [{trace_path}]({trace_path}#L{trace_line})\n"""
                        f"""- Line: {trace_line}"""
                    )

                    if trace_message != "":
                        traceback_message += f"\n- Message:{trace_message}"

                    test_message += traceback_message

                entry = _get_rdjson_entry(
                    test_message, PYTEST_SEVERITY_ERROR, crash_path, crash_line, crash_line
                )
                rdjson["diagnostics"].append(entry)

        # Construct warnings output
        if "warnings" in pytest_report:
            for warning in pytest_report["warnings"]:
                warning_message = warning["message"]
                warning_path = warning["filename"]
                warning_line = warning["lineno"]
                warning_category = warning["category"]

                if warning_category != "":
                    warning_message = f"{warning_category}: {warning_message}"

                entry = _get_rdjson_entry(
                    warning_message,
                    PYTEST_SEVERITY_WARNING,
                    warning_path,
                    warning_line,
                    warning_line,
                )
                rdjson["diagnostics"].append(entry)

    return json.dumps(rdjson)
