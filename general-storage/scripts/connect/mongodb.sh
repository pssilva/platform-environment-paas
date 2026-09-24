#!/usr/bin/env bash
set -Eeuo pipefail
command -v mongosh >/dev/null || { echo 'Instale mongosh conforme a documentação do MongoDB.' >&2; exit 127; }
: "${MONGODB_URI:?Defina MONGODB_URI para o servidor alvo}"
exec mongosh "$MONGODB_URI"
