#!/usr/bin/env bash
set -Eeuo pipefail
command -v mysql >/dev/null || { echo 'Instale o cliente MySQL (mysql).' >&2; exit 127; }
: "${MYSQL_USER:?Defina MYSQL_USER}"
args=(--protocol=TCP -h "${MYSQL_HOST:-localhost}" -P "${MYSQL_PORT:-3306}" -u "$MYSQL_USER" -p)
if [[ -n "${MYSQL_DATABASE:-}" ]]; then args+=("$MYSQL_DATABASE"); fi
exec mysql "${args[@]}"
