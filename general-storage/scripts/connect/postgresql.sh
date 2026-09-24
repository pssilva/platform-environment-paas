#!/usr/bin/env bash
set -Eeuo pipefail
command -v psql >/dev/null || { echo 'Instale o cliente PostgreSQL (psql).' >&2; exit 127; }
exec psql -h "${PGHOST:-localhost}" -p "${PGPORT:-5432}" -U "${PGUSER:-platform}" -d "${PGDATABASE:-platform}"
