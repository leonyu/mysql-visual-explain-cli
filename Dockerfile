# This Dockerfile is used as a Continuous Integration smoke test

FROM docker.io/library/debian:testing-slim AS test-runner

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  fonts-urw-base35 \
  python3-cairocffi \
  python3-poetry \
  unzip \
  && rm -rf /var/lib/apt/lists/*

COPY / /stage
WORKDIR /stage

RUN ./scripts/build.sh
RUN poetry install
RUN poetry run pytest
