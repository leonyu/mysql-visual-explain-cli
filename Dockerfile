# This Dockerfile is used as a Continuous Integration smoke test

FROM docker.io/library/debian:testing-slim AS builder

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  file \
  python3-cairocffi \
  unzip \
  && rm -rf /var/lib/apt/lists/*

COPY / /stage
WORKDIR /stage

RUN ./scripts/build.sh
RUN ./scripts/test.sh
