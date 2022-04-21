#!/bin/bash
set -eu

BASE_PATH="$(cd "$(dirname "$0")" && pwd)"

if [ -n "${GITHUB_WORKSPACE}" ]; then
  cd "${GITHUB_WORKSPACE}/${INPUT_WORKDIR}" || exit
fi

export REVIEWDOG_GITHUB_API_TOKEN="${INPUT_GITHUB_TOKEN}"

echo "[action-pytest] Pytest version:"
pytest --version

pytestArgsArr=("--json-report" "--json-report-file=./.report.json")
IFS=' ' read -ra pytestArgsArr <<<"${INPUT_PYTEST_CUSTOM_ARGS}"

# Check profiling arguments and take precedence with svg output, if true
if [ "${PYTEST_PROFILING_VISUAL}" == true ]; then
  pytestArgsArr+=("--profile-svg")
elif [ "${PYTEST_PROFILING}" == true ]; then
  pytestArgsArr+=("--profile")
fi

# Check coverage argument
if [ "${PYTEST_COVERAGE}" == true ]; then
  pytestArgsArr+=("--cov")
fi

# remove any duplicates
# TODO: give priority to custom args
# TODO: make this split on value as well
IFS=" " read -r -a pytestArgsArr <<<"$(tr ' ' '\n' <<<"${pytestArgsArr[@]}" | sort -u | tr '\n' ' ')"

pytestArgs=${pytestArgsArr[*]}
echo pytestArgs

echo "[action-pytest] Running pytest on \"${INPUT_WORKDIR}\"..."
exit_val="0"
pytest "${pytestArgs}" "${INPUT_WORKDIR}"

python "${BASE_PATH}/pytest_rdjson/pytest_rdjson.py" |
  /tmp/reviewdog -f=rdjson \
    -name="${INPUT_TOOL_NAME}" \
    -reporter="${INPUT_REPORTER}" \
    -filter-mode="${INPUT_FILTER_MODE}" \
    -fail-on-error="${INPUT_FAIL_ON_ERROR}" \
    "${INPUT_REVIEWDOG_FLAGS}" || exit_val="$?"

# TODO: handle SVG profiling image as reviewdog comment somehow
# if [ "${PYTEST_PROFILING_VISUAL}" == true ]; then

# fi

echo "[action-pytest] Clean up reviewdog..."
rm /tmp/reviewdog

if [[ "${exit_val}" -ne "0" ]]; then
  exit 1
fi
