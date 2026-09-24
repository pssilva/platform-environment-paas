#!/usr/bin/env bash
set -Eeuo pipefail

provider="${1:-}"
if [[ -z "$provider" ]]; then
  echo "Uso: install-cloud-cli {aws|azure|gcp|heroku|oci|openshift|spring-cloud|all}" >&2
  exit 2
fi

if [[ "$(id -u)" -eq 0 ]]; then
  SUDO=""
else
  SUDO="sudo"
fi

install_aws() {
  local architecture archive
  case "$(dpkg --print-architecture)" in
    amd64) architecture=x86_64 ;;
    arm64) architecture=aarch64 ;;
    *) echo "Arquitetura não suportada pelo instalador da AWS CLI." >&2; return 1 ;;
  esac
  archive="$(mktemp --suffix=.zip)"
  curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-${architecture}.zip" -o "$archive"
  unzip -q "$archive" -d "$(dirname "$archive")"
  "$SUDO" "$(dirname "$archive")/aws/install" \
    --update --install-dir /usr/local/aws-cli --bin-dir /usr/local/bin
  rm -rf "$archive" "$(dirname "$archive")/aws"
}

install_azure() {
  . /etc/os-release
  [[ "${ID:-}" == ubuntu ]] || { echo "Azure CLI: use os comandos oficiais da sua distribuição; este script cobre Ubuntu." >&2; return 1; }
  local keyring=/etc/apt/keyrings/microsoft.gpg
  $SUDO install -d -m 0755 /etc/apt/keyrings
  curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | $SUDO gpg --dearmor --yes -o "$keyring"
  $SUDO chmod 0644 "$keyring"
  echo "deb [arch=$(dpkg --print-architecture) signed-by=${keyring}] https://packages.microsoft.com/repos/azure-cli/ ${VERSION_CODENAME} main" \
    | $SUDO tee /etc/apt/sources.list.d/azure-cli.list >/dev/null
  $SUDO apt-get update
  $SUDO apt-get install -y azure-cli
}

install_gcp() {
  local keyring=/usr/share/keyrings/cloud.google.gpg
  $SUDO install -d -m 0755 /usr/share/keyrings
  curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | $SUDO gpg --dearmor --yes -o "$keyring"
  echo "deb [signed-by=${keyring}] https://packages.cloud.google.com/apt cloud-sdk main" \
    | $SUDO tee /etc/apt/sources.list.d/google-cloud-sdk.list >/dev/null
  $SUDO apt-get update
  $SUDO apt-get install -y google-cloud-cli
}

install_heroku() {
  curl -fsSL https://cli-assets.heroku.com/install.sh | $SUDO sh
}

install_oci() {
  local install_dir exec_dir
  if [[ "$(id -u)" -eq 0 ]]; then
    install_dir=/opt/oci-cli
    exec_dir=/usr/local/bin
  else
    install_dir="${HOME}/.local/share/oci-cli"
    exec_dir="${HOME}/.local/bin"
  fi
  mkdir -p "$install_dir" "$exec_dir"
  curl -fsSL https://raw.githubusercontent.com/oracle/oci-cli/master/scripts/install/install.sh \
    | bash -s -- --accept-all-defaults --install-dir "$install_dir" --exec-dir "$exec_dir"
}

install_openshift() {
  local architecture archive temp_dir
  case "$(dpkg --print-architecture)" in
    amd64) architecture=linux ;;
    arm64) architecture=linux-arm64 ;;
    *) echo "Arquitetura não suportada pelo cliente OpenShift." >&2; return 1 ;;
  esac
  archive="https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/openshift-client-${architecture}.tar.gz"
  temp_dir="$(mktemp -d)"
  curl -fsSL "$archive" | tar -xz -C "$temp_dir" oc kubectl
  $SUDO install -m 0755 "$temp_dir/oc" /usr/local/bin/oc
  $SUDO install -m 0755 "$temp_dir/kubectl" /usr/local/bin/kubectl
  rm -rf "$temp_dir"
}

install_spring_cloud() {
  local springboot_version="${SPRING_BOOT_CLI_VERSION:-4.1.1}"
  local sdkman_dir
  if [[ "$(id -u)" -eq 0 ]]; then
    sdkman_dir=/opt/sdkman
  else
    sdkman_dir="${HOME}/.sdkman"
  fi
  export SDKMAN_DIR="$sdkman_dir"
  mkdir -p "$SDKMAN_DIR"
  curl -fsSL https://get.sdkman.io | bash
  # shellcheck disable=SC1090
  source "${SDKMAN_DIR}/bin/sdkman-init.sh"
  sdk install springboot "$springboot_version" -y
}

case "$provider" in
  aws) install_aws ;;
  azure) install_azure ;;
  gcp) install_gcp ;;
  heroku) install_heroku ;;
  oci) install_oci ;;
  openshift) install_openshift ;;
  spring-cloud) install_spring_cloud ;;
  all) for cli in aws azure gcp heroku oci openshift spring-cloud; do "$BASH" "$0" "$cli"; done ;;
  *) echo "Provedor desconhecido: $provider" >&2; exit 2 ;;
esac
