#!/usr/bin/env bash
set -Eeuo pipefail
command -v sqlplus >/dev/null || { echo 'Instale SQL*Plus (Oracle Instant Client).' >&2; exit 127; }
: "${ORACLE_HOST:?Defina ORACLE_HOST}"
: "${ORACLE_SERVICE:?Defina ORACLE_SERVICE}"
: "${ORACLE_USER:?Defina ORACLE_USER}"
exec sqlplus "${ORACLE_USER}@//${ORACLE_HOST}:${ORACLE_PORT:-1521}/${ORACLE_SERVICE}"
