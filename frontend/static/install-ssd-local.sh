#!/usr/bin/env bash
set -Eeuo pipefail

REPO_URL="${REPO_URL:-https://github.com/projetssd/ssdv2.git}"
REPO_BRANCH="${REPO_BRANCH:-master}"

log() {
  printf '\n\033[1;36m[SSD bootstrap]\033[0m %s\n' "$*"
}

warn() {
  printf '\n\033[1;33m[SSD bootstrap]\033[0m %s\n' "$*" >&2
}

die() {
  printf '\n\033[1;31m[SSD bootstrap]\033[0m %s\n' "$*" >&2
  exit 1
}

is_root() {
  [[ "$(id -u)" -eq 0 ]]
}

run_privileged() {
  if is_root; then
    "$@"
  else
    command -v sudo >/dev/null 2>&1 || die "sudo est requis pour cette opération."
    sudo "$@"
  fi
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "Commande requise absente: $1"
}

get_home_dir() {
  local user="$1"
  getent passwd "$user" | cut -d: -f6
}

run_as_target_user() {
  local cmd="$1"

  if is_root; then
    su - "$TARGET_USER" -s /bin/bash -c "$cmd"
  else
    bash -lc "$cmd"
  fi
}

install_bootstrap_prereqs() {
  local missing=()

  command -v git >/dev/null 2>&1 || missing+=("git")
  command -v curl >/dev/null 2>&1 || missing+=("curl")
  command -v sudo >/dev/null 2>&1 || missing+=("sudo")
  command -v visudo >/dev/null 2>&1 || missing+=("sudo")

  if [[ ${#missing[@]} -eq 0 ]]; then
    return 0
  fi

  if command -v apt-get >/dev/null 2>&1; then
    log "Installation des prérequis bootstrap: ${missing[*]}"
    run_privileged apt-get update
    run_privileged env DEBIAN_FRONTEND=noninteractive apt-get install -y git curl sudo ca-certificates
  else
    die "Pré-requis manquants (${missing[*]}). Installe-les manuellement, puis relance."
  fi
}

configure_passwordless_sudo() {
  local sudoers_file="/etc/sudoers.d/90-ssdv2-${TARGET_USER}"
  local tmpfile

  tmpfile="$(mktemp)"
  printf '%s\n' "${TARGET_USER} ALL=(ALL:ALL) NOPASSWD:ALL" > "${tmpfile}"

  log "Configuration sudo sans mot de passe pour ${TARGET_USER}"
  run_privileged install -m 0440 "${tmpfile}" "${sudoers_file}"
  rm -f "${tmpfile}"

  run_privileged visudo -cf "${sudoers_file}" >/dev/null
}

clone_or_update_repo() {
  if [[ -d "${INSTALL_DIR}/.git" ]]; then
    log "Mise à jour du dépôt dans ${INSTALL_DIR}"
    run_as_target_user "git -C '${INSTALL_DIR}' fetch --all --prune"
    run_as_target_user "git -C '${INSTALL_DIR}' checkout '${REPO_BRANCH}'"
    run_as_target_user "git -C '${INSTALL_DIR}' pull --ff-only origin '${REPO_BRANCH}'"
  else
    log "Clonage du dépôt dans ${INSTALL_DIR}"
    run_privileged mkdir -p "$(dirname "${INSTALL_DIR}")"

    if is_root; then
      run_privileged chown "${TARGET_USER}:${TARGET_USER}" "$(dirname "${INSTALL_DIR}")"
    fi

    run_as_target_user "git clone --branch '${REPO_BRANCH}' '${REPO_URL}' '${INSTALL_DIR}'"
  fi

  if is_root; then
    run_privileged chown -R "${TARGET_USER}:${TARGET_USER}" "${INSTALL_DIR}"
  fi
}

launch_seedbox() {
  log "Lancement de seedbox.sh depuis ${INSTALL_DIR}"

  if is_root; then
    exec su - "${TARGET_USER}" -s /bin/bash -c "cd '${INSTALL_DIR}' && exec bash './seedbox.sh'"
  else
    cd "${INSTALL_DIR}"
    exec bash "./seedbox.sh"
  fi
}

main() {
  if is_root; then
    TARGET_USER="${TARGET_USER:-}"
    [[ -n "${TARGET_USER}" ]] || die "En root, passe TARGET_USER=nom_utilisateur."
  else
    TARGET_USER="${TARGET_USER:-$USER}"
  fi

  [[ "${TARGET_USER}" != "root" ]] || die "TARGET_USER ne peut pas être root."
  id "${TARGET_USER}" >/dev/null 2>&1 || die "Utilisateur introuvable: ${TARGET_USER}"

  TARGET_HOME="$(get_home_dir "${TARGET_USER}")"
  [[ -n "${TARGET_HOME}" ]] || die "Impossible de déterminer le HOME de ${TARGET_USER}"
  [[ -d "${TARGET_HOME}" ]] || die "Le HOME de ${TARGET_USER} n'existe pas: ${TARGET_HOME}"

  INSTALL_DIR="${INSTALL_DIR:-${TARGET_HOME}/seedbox-compose}"

  install_bootstrap_prereqs
  require_command git
  require_command curl
  require_command visudo

  configure_passwordless_sudo
  clone_or_update_repo
  launch_seedbox
}

main "$@"