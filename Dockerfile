# This Dockerfile is used as a Continuous Integration smoke test

FROM docker.io/library/debian:testing-slim AS builder

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

FROM docker.io/library/alpine:3.21 AS runner

RUN apk add py3-cairocffi
COPY --from=builder /stage/dist/mysql_visual_explain_cli.pyz /mysql_visual_explain_cli
RUN chmod +x /mysql_visual_explain_cli
RUN /mysql_visual_explain_cli || true
ENTRYPOINT /mysql_visual_explain_cli
