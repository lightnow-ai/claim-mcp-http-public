FROM python:3.13-slim

ARG VERSION=0.1.0
ARG VCS_REF=unknown

LABEL org.opencontainers.image.title="LightNow Claim MCP http public" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.source="https://github.com/lightnow-ai/claim-mcp-http-public"

RUN addgroup --system --gid 10001 lightnow && adduser --system --uid 10001 --ingroup lightnow lightnow

WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

USER 10001:10001
EXPOSE 8000
ENTRYPOINT ["claim-mcp-http-public"]

