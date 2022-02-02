"""Testing pytest to rdjson with pytest (things are getting pretty circular)."""

import pytest
import json
from typing import Any

from .pytest_rdjson import pytest_to_rdjson


def ordered(obj):
    # credit to https://stackoverflow.com/a/25851972

    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def remove_paths(rdjson_obj: dict[str, Any]) -> dict[str, Any]:
    for i in range(len(rdjson_obj["diagnostics"])):
        del rdjson_obj["diagnostics"][i]["location"]["path"]

    return rdjson_obj


class TestPytestRdjson:
    """Tests for pytest to rdjson."""

    @pytest.mark.timeout(10)
    def test_pytest_to_rdjson(self):
        """Test that pytest_to_rdjson gives the expected output."""
        pytest_json_filepath = "./.report.json"
        rdjson_filepath = "./pytest_rdjson/expected_rdjson.json"

        with open(rdjson_filepath, "r") as f:
            rdjson_exp = f.read()

        rdjson_exp_obj = json.loads(rdjson_exp)

        pytest_args = [
            "--json-report",
            "./testdata",
        ]
        exit_code = pytest.main(pytest_args)
        assert exit_code == 1  # testdata tests should fail

        rdjson_out = pytest_to_rdjson(pytest_json_filepath)
        rdjson_out_obj = json.loads(rdjson_out)

        # remove the "path" key/value from each object, since these will never be constants
        rdjson_exp_obj = remove_paths(rdjson_exp_obj)
        rdjson_out_obj = remove_paths(rdjson_out_obj)

        # # uncomment this to get a new rdjson file
        # with open("./out.json", "w") as f:
        #     json.dump(rdjson_out_obj, f)

        difference_out = {
            k: rdjson_out_obj[k]
            for k in rdjson_out_obj
            if k in rdjson_exp_obj and rdjson_out_obj[k] != rdjson_exp_obj[k]
        }

        difference_exp = {
            k: rdjson_exp_obj[k]
            for k in rdjson_out_obj
            if k in rdjson_exp_obj and rdjson_out_obj[k] != rdjson_exp_obj[k]
        }

        # TODO: Figure out why this is False still
        assert ordered(rdjson_out_obj) == ordered(rdjson_exp_obj)
