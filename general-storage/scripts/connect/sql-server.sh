#!/usr/bin/env bash
set -Eeuo pipefail
command -v sqlcmd >/dev/null || { echo 'Instale sqlcmd conforme a documentação da Microsoft.' >&2; exit 127; }
: "${SQLSERVER_HOST:?Defina SQLSERVER_HOST}"
: "${SQLSERVER_USER:?Defina SQLSERVER_USER}"
exec sqlcmd -S "${SQLSERVER_HOST},${SQLSERVER_PORT:-1433}" -d "${SQLSERVER_DATABASE:-master}" -U "$SQLSERVER_USER"
