#!/usr/bin/env bash
set -Eeuo pipefail
command -v redis-cli >/dev/null || { echo 'Instale redis-cli conforme a documentação do Redis.' >&2; exit 127; }
args=(-h "${REDIS_HOST:-localhost}" -p "${REDIS_PORT:-6379}")
if [[ "${REDIS_TLS:-false}" == true ]]; then args+=(--tls); fi
if [[ "${REDIS_ASKPASS:-false}" == true ]]; then args+=(--askpass); fi
exec redis-cli "${args[@]}"
