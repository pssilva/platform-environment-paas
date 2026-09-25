#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../../../../.." && pwd)"
GO_SCRIPT="$REPO_ROOT/scripts/src/main/automation/PaaSScriptsUteis/golang/paas_scripts_uteis.go"
TEMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TEMP_DIR"' EXIT
export GOCACHE="$TEMP_DIR/go-build-cache"

run_script() {
  go run "$GO_SCRIPT" "$@"
}

assert_contains() {
  local output="$1"
  local expected="$2"
  if [[ "$output" != *"$expected"* ]]; then
    printf 'ERRO: saída não contém "%s". Saída recebida:\n%s\n' "$expected" "$output" >&2
    exit 1
  fi
}

output="$(run_script --help)"
assert_contains "$output" "Uso: paas_scripts_uteis <comando>"
printf 'OK: --help\n'

output="$(run_script version)"
assert_contains "$output" "1.0"
printf 'OK: version\n'

output="$(run_script summary)"
assert_contains "$output" "Rotinas de criação de pastas, CSV e instalação de ferramentas."
printf 'OK: summary\n'

output="$(run_script make-all-tools)"
assert_contains "$output" "NÃO IMPLEMENTADO AINDA"
printf 'OK: make-all-tools\n'

structure_root="$TEMP_DIR/projeto-teste"
run_script create-structure "$structure_root"
for relative_dir in \
  docs/imgs \
  docs/indexacoes \
  docs/provedores_nuvem \
  scripts/src/main/automation \
  scripts/src/test/automation; do
  [[ -d "$structure_root/$relative_dir" ]] || {
    printf 'ERRO: diretório não criado: %s\n' "$relative_dir" >&2
    exit 1
  }
  [[ -f "$structure_root/$relative_dir/.gitkeep" ]] || {
    printf 'ERRO: .gitkeep não criado em: %s\n' "$relative_dir" >&2
    exit 1
  }
done
printf 'OK: create-structure\n'

printf 'Todos os testes passaram.\n'
