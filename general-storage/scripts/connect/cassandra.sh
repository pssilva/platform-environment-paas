#!/usr/bin/env bash
set -Eeuo pipefail
command -v cqlsh >/dev/null || { echo 'Instale cqlsh compatível com o servidor Cassandra.' >&2; exit 127; }
exec cqlsh "${CASSANDRA_HOST:-localhost}" "${CASSANDRA_PORT:-9042}"
