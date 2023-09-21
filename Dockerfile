# This Dockerfile is used as a Continuous Integration smoke test

FROM docker.io/library/debian:testing-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
  p7zip-full \
  python3-cairocffi \
  python3-poetry \
  && rm -rf /var/lib/apt/lists/*

COPY / /stage
WORKDIR /stage

RUN ./scripts/build.sh
RUN ./scripts/test.sh
