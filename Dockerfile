FROM python:alpine

ENV REVIEWDOG_VERSION=v0.13.0

WORKDIR /src

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]

# hadolint ignore=DL3006,DL3018
RUN apk --no-cache add build-base libffi-dev git graphviz

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN wget -O - -q https://raw.githubusercontent.com/reviewdog/reviewdog/master/install.sh| sh -s -- -b /usr/local/bin ${REVIEWDOG_VERSION}

# hadolint ignore=DL3013,SC2169,SC3001
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir --upgrade poetry && \
    python -m pip install --no-cache-dir --requirement <(poetry export --format requirements.txt)

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
