#!/usr/bin/env bash
set -Eeuo pipefail

PAIRING_CODE=""
BACKEND_URL=""
INSTALL_DIR="/opt/ssd-agent"
AGENT_USER=""
ALLOW_INSECURE_HTTP="${ALLOW_INSECURE_HTTP:-false}"
AGENT_VERSION="0.1.0"

usage() {
  cat <<'EOF'
Usage:
  bootstrap.sh --pairing-code XXXX-XXXX --backend-url https://admin.example.com [--agent-user USER] [--install-dir /opt/ssd-agent]

By default, insecure HTTP is refused.
To override temporarily (not recommended), run with:
  ALLOW_INSECURE_HTTP=true ./bootstrap.sh ...
EOF
  exit 1
}

log() {
  echo "[bootstrap] $*"
}

die() {
  echo "[bootstrap] $*" >&2
  exit 1
}

on_error() {
  local exit_code="$?"
  local line_no="${1:-unknown}"
  echo "[bootstrap] Error on or near line ${line_no} (exit=${exit_code})" >&2
  exit "${exit_code}"
}

trap 'on_error $LINENO' ERR

require_arg_value() {
  local flag="${1:-}"
  local value="${2:-}"
  if [[ -z "${value}" || "${value}" == --* ]]; then
    die "Missing value for ${flag}"
  fi
}

detect_agent_user() {
  if [[ -n "${AGENT_USER}" ]]; then
    return 0
  fi

  if [[ -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    if id "${SUDO_USER}" >/dev/null 2>&1; then
      AGENT_USER="${SUDO_USER}"
      return 0
    fi
  fi

  mapfile -t human_users < <(
    awk -F: '
      $3 >= 1000 &&
      $1 != "nobody" &&
      $6 ~ "^/home/" &&
      $7 !~ /(nologin|false)$/ {
        print $1
      }
    ' /etc/passwd
  )

  if [[ "${#human_users[@]}" -eq 1 ]]; then
    AGENT_USER="${human_users[0]}"
    return 0
  fi

  if [[ "${#human_users[@]}" -eq 0 ]]; then
    echo "[bootstrap] No non-root user found under /home."
  else
    echo "[bootstrap] Multiple candidate users found:"
    printf ' - %s\n' "${human_users[@]}"
  fi

  echo "[bootstrap] Unable to determine agent user automatically."
  echo "[bootstrap] Re-run with --agent-user <user>"
  exit 1
}

run_as_agent_user() {
  runuser -u "${AGENT_USER}" -- "$@"
}

if [[ "${EUID}" -ne 0 ]]; then
  die "This script must run as root."
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pairing-code)
      require_arg_value "$1" "${2:-}"
      PAIRING_CODE="${2}"
      shift 2
      ;;
    --backend-url)
      require_arg_value "$1" "${2:-}"
      BACKEND_URL="${2}"
      shift 2
      ;;
    --agent-user)
      require_arg_value "$1" "${2:-}"
      AGENT_USER="${2}"
      shift 2
      ;;
    --install-dir)
      require_arg_value "$1" "${2:-}"
      INSTALL_DIR="${2}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      ;;
  esac
done

if [[ -z "${PAIRING_CODE}" || -z "${BACKEND_URL}" ]]; then
  usage
fi

BACKEND_URL="${BACKEND_URL%/}"

if [[ "${BACKEND_URL}" != https://* && "${ALLOW_INSECURE_HTTP}" != "true" ]]; then
  echo "[bootstrap] BACKEND_URL must start with https://"
  echo "[bootstrap] Refusing insecure HTTP bootstrap by default"
  exit 1
fi

detect_agent_user

if ! id "${AGENT_USER}" >/dev/null 2>&1; then
  die "User '${AGENT_USER}' does not exist."
fi

AGENT_HOME="$(getent passwd "${AGENT_USER}" | cut -d: -f6)"
if [[ -z "${AGENT_HOME}" || ! -d "${AGENT_HOME}" ]]; then
  die "Could not resolve home directory for user '${AGENT_USER}'."
fi

COMPOSE_DIR="${AGENT_HOME}/seedbox-compose"
DOCKER_BIN="/usr/bin/docker"

VERIFY_TLS_VALUE="true"
if [[ "${BACKEND_URL}" == http://* ]]; then
  VERIFY_TLS_VALUE="false"
fi

HOSTNAME_VALUE="$(hostname)"

SUPPLEMENTARY_GROUPS_LINE=""
if getent group docker >/dev/null 2>&1; then
  if id -nG "${AGENT_USER}" | tr ' ' '\n' | grep -qx docker; then
    SUPPLEMENTARY_GROUPS_LINE="SupplementaryGroups=docker"
  else
    log "User ${AGENT_USER} is not in docker group. Adding it now..."
    usermod -aG docker "${AGENT_USER}"
    SUPPLEMENTARY_GROUPS_LINE="SupplementaryGroups=docker"
  fi
fi

log "Agent user resolved to: ${AGENT_USER}"
log "Agent home: ${AGENT_HOME}"
log "Compose dir: ${COMPOSE_DIR}"
log "Requested install dir: ${INSTALL_DIR}"

log "Installing prerequisites..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv python3-pip curl ca-certificates

INSTALL_DIR="$(python3 - <<'PY' "${INSTALL_DIR}"
import os, sys
print(os.path.abspath(sys.argv[1]))
PY
)"

log "Normalized install dir: ${INSTALL_DIR}"

if [[ ! -d "${COMPOSE_DIR}" ]]; then
  die "${COMPOSE_DIR} not found. Install seedbox-compose first before bootstrapping the agent."
fi

if [[ ! -f "${COMPOSE_DIR}/includes/functions.sh" ]]; then
  die "${COMPOSE_DIR}/includes/functions.sh not found."
fi

if [[ ! -f "${COMPOSE_DIR}/includes/variables.sh" ]]; then
  die "${COMPOSE_DIR}/includes/variables.sh not found."
fi

log "Creating install directory..."
mkdir -p "${INSTALL_DIR}/agent"
mkdir -p "${INSTALL_DIR}/logs"
mkdir -p "${INSTALL_DIR}/tmp/ansible"
mkdir -p "${AGENT_HOME}/.ansible/tmp"

chown -R "${AGENT_USER}:${AGENT_USER}" "${INSTALL_DIR}"
chown -R "${AGENT_USER}:${AGENT_USER}" "${AGENT_HOME}/.ansible"

chmod 750 "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}/agent"
chmod 750 "${INSTALL_DIR}/logs"
chmod 750 "${INSTALL_DIR}/tmp"
chmod 750 "${INSTALL_DIR}/tmp/ansible"
chmod 700 "${AGENT_HOME}/.ansible"
chmod 700 "${AGENT_HOME}/.ansible/tmp"

log "Creating virtualenv..."
rm -rf "${INSTALL_DIR}/.venv"
run_as_agent_user python3 -m venv "${INSTALL_DIR}/.venv"
run_as_agent_user "${INSTALL_DIR}/.venv/bin/pip" install --upgrade pip
run_as_agent_user "${INSTALL_DIR}/.venv/bin/pip" install requests websockets
run_as_agent_user "${INSTALL_DIR}/.venv/bin/python" - <<'PY'
import importlib.util
missing = [name for name in ("requests", "websockets") if importlib.util.find_spec(name) is None]
if missing:
    raise SystemExit(f"Missing Python packages after install: {', '.join(missing)}")
print("Python dependencies verified: requests, websockets")
PY

log "Verifying pairing code..."

CURL_FLAGS=(-fsSL --connect-timeout 10 --max-time 30)
if [[ "${BACKEND_URL}" == https://* ]]; then
  CURL_FLAGS+=(--proto '=https' --tlsv1.2)
fi

PAIRING_REQUEST="$(python3 - <<'PY' "${PAIRING_CODE}"
import json, sys
print(json.dumps({"pairing_code": sys.argv[1]}))
PY
)"

VERIFY_RESPONSE="$(curl "${CURL_FLAGS[@]}" \
  -X POST "${BACKEND_URL}/pairing/verify" \
  -H "Content-Type: application/json" \
  --data "${PAIRING_REQUEST}")"

log "Pairing response received."

IFS=$'\t' read -r MACHINE_TOKEN MACHINE_ID MACHINE_UUID < <(
  python3 - <<'PY' "${VERIFY_RESPONSE}"
import json, sys

data = json.loads(sys.argv[1])

if not data.get("valid"):
    raise SystemExit(data.get("message") or "Pairing code invalid")

print(
    data["machine_token"],
    data["machine_id"],
    data["machine_uuid"],
    sep="\t",
)
PY
)

if [[ -z "${MACHINE_TOKEN}" || -z "${MACHINE_ID}" || -z "${MACHINE_UUID}" ]]; then
  die "Pairing response is missing required fields."
fi

log "Writing agent files..."

cat > "${INSTALL_DIR}/agent/__init__.py" <<'PY'
PY

cat > "${INSTALL_DIR}/agent/config.py" <<PY
import os
from pathlib import Path


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if key and key not in os.environ:
            os.environ[key] = value


load_env_file("${INSTALL_DIR}/.env")

BACKEND_URL = os.environ["BACKEND_URL"].rstrip("/")
MACHINE_TOKEN = os.environ["MACHINE_TOKEN"]
HOSTNAME = os.environ.get("HOSTNAME", "unknown-host")
AGENT_VERSION = os.environ.get("AGENT_VERSION", "0.1.0")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))
VERIFY_TLS = os.environ.get("VERIFY_TLS", "true").lower() == "true"
DOCKER_BIN = os.environ.get("DOCKER_BIN", "/usr/bin/docker")
PY

cat > "${INSTALL_DIR}/agent/api.py" <<'PY'
import requests

from agent.config import BACKEND_URL, MACHINE_TOKEN, VERIFY_TLS


def auth_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {MACHINE_TOKEN}",
        "Content-Type": "application/json",
    }


def post(path: str, payload: dict | None = None) -> requests.Response:
    return requests.post(
        f"{BACKEND_URL}{path}",
        json=payload,
        headers=auth_headers(),
        timeout=30,
        verify=VERIFY_TLS,
    )


def authenticate() -> dict:
    response = post("/agent/auth")
    response.raise_for_status()
    return response.json()


def heartbeat(
    hostname: str,
    agent_version: str,
    ssdv2_installed: bool,
    installed_apps: list[dict[str, str | None]] | None = None,
) -> dict:
    response = post(
        "/agent/heartbeat",
        {
            "hostname": hostname,
            "agent_version": agent_version,
            "ssdv2_installed": ssdv2_installed,
            "installed_apps": installed_apps or [],
        },
    )
    response.raise_for_status()
    return response.json()


def fetch_job() -> dict:
    response = post("/agent/jobs/fetch")
    response.raise_for_status()
    return response.json()


def send_log(job_id: str, seq: int, level: str, message: str) -> dict:
    response = post(
        f"/agent/jobs/{job_id}/logs",
        {
            "seq": seq,
            "level": level,
            "message": message,
        },
    )
    if response.status_code >= 400:
        raise requests.HTTPError(
            f"{response.status_code} Client Error for url: {response.url} | response={response.text}",
            response=response,
        )
    return response.json()


def complete_job(job_id: str, result: dict | None = None, error_message: str | None = None) -> dict:
    response = post(
        f"/agent/jobs/{job_id}/complete",
        {
            "result": result,
            "error_message": error_message,
        },
    )
    response.raise_for_status()
    return response.json()
PY

cat > "${INSTALL_DIR}/agent/discovery.py" <<'PY'
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from agent.config import DOCKER_BIN

PREFERRED_NAME_MAP = {
    "bazarr": "Bazarr",
    "crowdsec": "CrowdSec",
    "error-pages": "Error Pages",
    "jellyfin": "Jellyfin",
    "lidarr": "Lidarr",
    "prowlarr": "Prowlarr",
    "qbittorrent": "qBittorrent",
    "radarr": "Radarr",
    "readarr": "Readarr",
    "sabnzbd": "SABnzbd",
    "sonarr": "Sonarr",
    "traefik": "Traefik",
}

IGNORED_PREFIXES = {"ssd", "docker", "compose", "svc", "service"}


def run_command(command: list[str]) -> tuple[int, str]:
    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    output = process.stdout.strip()

    if process.stderr.strip():
        output = f"{output}\n{process.stderr.strip()}".strip()

    return process.returncode, output


def normalize_slug(value: str | None) -> str | None:
    if value is None:
        return None

    slug = str(value).strip().lower()
    if not slug:
        return None

    slug = slug.replace(" ", "-")
    slug = re.sub(r"[^a-z0-9._-]", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-._")
    slug = re.sub(r"-(?:\d+)$", "", slug)
    slug = re.sub(r"_(?:\d+)$", "", slug)

    return slug or None


def prettify_slug(slug: str) -> str:
    if slug in PREFERRED_NAME_MAP:
        return PREFERRED_NAME_MAP[slug]
    return slug.replace("-", " ").replace("_", " ").title()


def candidate_slugs_from_name(name: str) -> list[str]:
    normalized = normalize_slug(name)
    if not normalized:
        return []

    results: list[str] = [normalized]

    for separator in ("-", "_"):
        parts = [part for part in normalized.split(separator) if part]
        if len(parts) >= 2 and parts[0] in IGNORED_PREFIXES:
            results.append(parts[1])

    seen: set[str] = set()
    deduped: list[str] = []

    for item in results:
        slug = normalize_slug(item)
        if not slug or slug in seen:
            continue
        seen.add(slug)
        deduped.append(slug)

    return deduped


def resolve_docker_bin() -> str | None:
    configured = str(DOCKER_BIN or "").strip()
    if configured:
        return configured

    found = shutil.which("docker")
    if found:
        return found

    fallback = "/usr/bin/docker"
    if Path(fallback).exists():
        return fallback

    return None


def add_app(
    results: dict[str, dict[str, str | None]],
    slug: str | None,
    public_url: str | None = None,
) -> None:
    normalized_slug = normalize_slug(slug)
    if not normalized_slug:
        return

    existing = results.get(normalized_slug)
    if existing is None:
        results[normalized_slug] = {
            "app_slug": normalized_slug,
            "app_name": prettify_slug(normalized_slug),
            "public_url": public_url,
        }
        return

    if public_url and not existing.get("public_url"):
        existing["public_url"] = public_url


def extract_public_url_from_labels(labels: dict[str, str] | None) -> str | None:
    if not labels:
        return None

    if str(labels.get("traefik.enable", "")).strip().lower() not in {"true", "1", "yes", "on"}:
        return None

    for key, value in labels.items():
        if not key.startswith("traefik.http.routers."):
            continue
        if not key.endswith(".rule"):
            continue

        rule = str(value or "").strip()
        if not rule:
            continue

        match = re.search(r"Host\(\s*`([^`]+)`\s*\)", rule)
        if match:
            host = match.group(1).strip()
            if host:
                return f"https://{host}"

        match = re.search(r'Host\(\s*"([^"]+)"\s*\)', rule)
        if match:
            host = match.group(1).strip()
            if host:
                return f"https://{host}"

    return None


def inspect_container_labels(docker_bin: str, container_name: str) -> dict[str, str]:
    return_code, output = run_command(
        [docker_bin, "inspect", container_name, "--format", "{{json .Config.Labels}}"]
    )
    if return_code != 0 or not output:
        return {}

    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return {}

    if not isinstance(data, dict):
        return {}

    result: dict[str, str] = {}
    for key, value in data.items():
        result[str(key)] = "" if value is None else str(value)
    return result


def discover_installed_apps() -> list[dict[str, str | None]]:
    results: dict[str, dict[str, str | None]] = {}

    docker_bin = resolve_docker_bin()
    if not docker_bin:
        return []

    return_code, output = run_command(
        [docker_bin, "ps", "-a", "--format", "{{.Names}}\t{{.Image}}"]
    )
    if return_code != 0 or not output:
        return []

    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        parts = line.split("\t")
        container_name = parts[0].strip() if len(parts) >= 1 else ""
        image_name = parts[1].strip() if len(parts) >= 2 else ""

        image_basename = ""
        if image_name:
            image_basename = image_name.split("/")[-1].split(":")[0]

        candidates: list[str] = []
        if container_name:
            candidates.extend(candidate_slugs_from_name(container_name))
        if image_basename:
            candidates.extend(candidate_slugs_from_name(image_basename))

        selected_slug = candidates[0] if candidates else None
        if not selected_slug:
            continue

        labels = inspect_container_labels(docker_bin, container_name) if container_name else {}
        public_url = extract_public_url_from_labels(labels)

        add_app(results, selected_slug, public_url)

    return [results[slug] for slug in sorted(results)]
PY

cat > "${INSTALL_DIR}/agent/presence.py" <<'PY'
import asyncio
import threading
from urllib.parse import quote

import websockets

from agent.config import BACKEND_URL, MACHINE_TOKEN, VERIFY_TLS


def _build_ws_url(machine_id: str) -> str:
    if BACKEND_URL.startswith("https://"):
        base = "wss://" + BACKEND_URL[len("https://"):]
    elif BACKEND_URL.startswith("http://"):
        base = "ws://" + BACKEND_URL[len("http://"):]
    else:
        raise RuntimeError("Unsupported BACKEND_URL for websocket presence")

    token = quote(MACHINE_TOKEN, safe="")
    return f"{base}/ws/machines/{machine_id}/agent?token={token}"


async def _presence_loop(machine_id: str, log) -> None:
    url = _build_ws_url(machine_id)

    while True:
        try:
            async with websockets.connect(
                url,
                open_timeout=10,
                close_timeout=5,
                ping_interval=20,
                ping_timeout=20,
                user_agent_header="ssd-agent-presence/0.1",
                ssl=VERIFY_TLS if url.startswith("wss://") else None,
            ) as websocket:
                log(f"presence websocket connected: machine_id={machine_id}")
                while True:
                    await websocket.send("ping")
                    await asyncio.sleep(10)
        except Exception as exc:
            log(f"presence websocket disconnected: {exc}")
            await asyncio.sleep(2)


def start_presence_thread(machine_id: str, log) -> threading.Thread:
    def runner() -> None:
        asyncio.run(_presence_loop(machine_id, log))

    thread = threading.Thread(target=runner, name="ssd-agent-presence", daemon=True)
    thread.start()
    return thread
PY

cat > "${INSTALL_DIR}/agent/main.py" <<'PY'
import time
from datetime import datetime, timezone
from pathlib import Path

from agent.api import authenticate, fetch_job, heartbeat
from agent.config import AGENT_VERSION, HOSTNAME, POLL_INTERVAL
from agent.discovery import discover_installed_apps
from agent.presence import start_presence_thread
from agent.runner import run_job


def log(message: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] [agent] {message}", flush=True)


def is_ssdv2_installed() -> bool:
    target = Path.home() / "seedbox-compose" / "ssddb"
    return target.exists()


def main() -> None:
    auth_data = authenticate()
    machine_id = str(auth_data["machine_id"])
    log(f"authenticated: machine_id={machine_id} status={auth_data['status']}")

    start_presence_thread(machine_id, log)

    while True:
        try:
            ssdv2_installed = is_ssdv2_installed()
            installed_apps = discover_installed_apps()

            hb = heartbeat(HOSTNAME, AGENT_VERSION, ssdv2_installed, installed_apps)
            log(
                f"heartbeat ok: last_seen_at={hb['last_seen_at']} "
                f"ssdv2_installed={ssdv2_installed} "
                f"installed_apps={len(installed_apps)}"
            )

            if installed_apps:
                log(
                    "discovered apps: "
                    + ", ".join(app["app_slug"] for app in installed_apps if app.get("app_slug"))
                )
            else:
                log("discovered apps: none")

            job_response = fetch_job()

            if job_response.get("has_job"):
                log(f"received job: {job_response['job_id']} type={job_response['type']}")
                run_job(job_response)
                log(f"finished job: {job_response['job_id']}")
            else:
                log("no job")

        except Exception as exc:
            log(f"error: {exc}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
PY

cat > "${INSTALL_DIR}/agent/runner.py" <<'PY'
import shlex
import subprocess

from agent.api import complete_job, send_log


def shell_line(command: str) -> tuple[int, str]:
    process = subprocess.run(
        ["bash", "-lc", command],
        capture_output=True,
        text=True,
    )
    output = process.stdout.strip()

    if process.stderr.strip():
        output = f"{output}\n{process.stderr.strip()}".strip()

    return process.returncode, output


def quote(value: object) -> str:
    return shlex.quote("" if value is None else str(value))


def parse_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def compose_runtime_prefix(compose_dir: str = "~/seedbox-compose") -> str:
    return " && ".join(
        [
            f"cd {compose_dir}",
            "test -f includes/functions.sh",
            "source includes/functions.sh",
            "test -f includes/variables.sh",
            "source includes/variables.sh",
            'if [ -f venv/bin/activate ]; then source venv/bin/activate; fi',
            'if [ -f profile.sh ]; then source profile.sh >/dev/null 2>&1 || true; fi',
        ]
    )


def run_logged_command(
    job_id: str,
    seq: int,
    command: str,
    *,
    reveal_command: bool = True,
    label: str | None = None,
) -> tuple[int, int]:
    if reveal_command:
        send_log(job_id, seq, "info", f"running command: {command}")
    else:
        send_log(job_id, seq, "info", label or "running hidden command")
    seq += 1

    return_code, output = shell_line(command)

    if output:
        for line in output.splitlines():
            message = line.rstrip()
            if not message:
                continue
            send_log(job_id, seq, "info", message)
            seq += 1

    return return_code, seq


def run_streaming_command(
    job_id: str,
    seq: int,
    command: str,
) -> tuple[int, int]:
    send_log(job_id, seq, "info", f"running command: {command}")
    seq += 1

    process = subprocess.Popen(
        ["bash", "-lc", command],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    assert process.stdout is not None

    for line in process.stdout:
        message = line.rstrip()
        if not message:
            continue
        send_log(job_id, seq, "info", message)
        seq += 1

    return_code = process.wait()
    return return_code, seq


def run_install_app(job_id: str, payload: dict, seq: int) -> tuple[bool, int, dict | None, str | None]:
    app_slug = payload.get("app_slug")
    subdomain = payload.get("subdomain")
    auth_type = payload.get("auth_type")

    if not app_slug:
        return False, seq, None, "Missing app_slug in payload"
    if not subdomain:
        return False, seq, None, "Missing subdomain in payload"
    if not auth_type:
        return False, seq, None, "Missing auth_type in payload"

    compose_dir = "~/seedbox-compose"
    prefix = compose_runtime_prefix(compose_dir)

    pre_commands = [
        (
            f"{prefix} && manage_account_yml sub.{quote(app_slug)}.{quote(app_slug)} {quote(subdomain)}",
            f"updating all.yml: sub.{app_slug}.{app_slug}",
        ),
        (
            f"{prefix} && manage_account_yml sub.{quote(app_slug)}.auth {quote(auth_type)}",
            f"updating all.yml: sub.{app_slug}.auth",
        ),
    ]

    for command, label in pre_commands:
        return_code, seq = run_logged_command(
            job_id,
            seq,
            command,
            reveal_command=False,
            label=label,
        )
        if return_code != 0:
            send_log(job_id, seq, "error", f"command failed with return code={return_code}")
            seq += 1
            return False, seq, None, f"Preparation command failed with return code {return_code}"

    command = f"{prefix} && launch_service {quote(app_slug)}"
    return_code, seq = run_streaming_command(job_id, seq, command)

    if return_code == 0:
        result = {
            "message": "install finished",
            "app_slug": app_slug,
            "subdomain": subdomain,
            "auth_type": auth_type,
            "return_code": return_code,
        }
        return True, seq, result, None

    return False, seq, None, f"Command failed with return code {return_code}"


def run_uninstall_app(job_id: str, payload: dict, seq: int) -> tuple[bool, int, dict | None, str | None]:
    app_slug = payload.get("app_slug")

    if not app_slug:
        return False, seq, None, "Missing app_slug in payload"

    compose_dir = "~/seedbox-compose"
    prefix = compose_runtime_prefix(compose_dir)

    command = f"{prefix} && suppression_appli {quote(app_slug)}"
    return_code, seq = run_streaming_command(job_id, seq, command)

    if return_code == 0:
        result = {
            "message": "uninstall finished",
            "app_slug": app_slug,
            "return_code": return_code,
        }
        return True, seq, result, None

    return False, seq, None, f"Command failed with return code {return_code}"


def run_job(job: dict) -> None:
    job_id = job["job_id"]
    job_type = job["type"]
    payload = job.get("payload") or {}
    seq = 1

    try:
        if job_type == "install_app":
            success, seq, result, error_message = run_install_app(job_id, payload, seq)
        elif job_type == "uninstall_app":
            success, seq, result, error_message = run_uninstall_app(job_id, payload, seq)
        else:
            send_log(job_id, seq, "error", f"unsupported job type={job_type}")
            complete_job(job_id, error_message=f"Unsupported job type: {job_type}")
            return

        if success:
            send_log(job_id, seq, "info", f"job finished successfully for type={job_type}")
            complete_job(job_id, result=result)
        else:
            send_log(job_id, seq, "error", error_message or "job failed")
            complete_job(job_id, error_message=error_message or "Job failed")

    except Exception as exc:
        try:
            send_log(job_id, seq, "error", f"exception: {exc}")
            complete_job(job_id, error_message=str(exc))
        except Exception:
            pass
        raise
PY

cat > "${INSTALL_DIR}/.env" <<EOF
BACKEND_URL=${BACKEND_URL}
MACHINE_TOKEN=${MACHINE_TOKEN}
HOSTNAME=${HOSTNAME_VALUE}
AGENT_VERSION=${AGENT_VERSION}
POLL_INTERVAL=5
VERIFY_TLS=${VERIFY_TLS_VALUE}
MACHINE_ID=${MACHINE_ID}
MACHINE_UUID=${MACHINE_UUID}
DOCKER_BIN=${DOCKER_BIN}
EOF

chown -R "${AGENT_USER}:${AGENT_USER}" "${INSTALL_DIR}"
chmod 600 "${INSTALL_DIR}/.env"

log "Creating systemd service..."

cat > /etc/systemd/system/ssd-agent.service <<EOF
[Unit]
Description=SSD Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${AGENT_USER}
Group=${AGENT_USER}
${SUPPLEMENTARY_GROUPS_LINE}
WorkingDirectory=${INSTALL_DIR}
Environment=PYTHONUNBUFFERED=1
Environment=HOME=${AGENT_HOME}
Environment=TERM=xterm
Environment=TMPDIR=${INSTALL_DIR}/tmp
Environment=ANSIBLE_LOCAL_TEMP=${INSTALL_DIR}/tmp/ansible
Environment=ANSIBLE_REMOTE_TMP=${INSTALL_DIR}/tmp/ansible
ExecStart=${INSTALL_DIR}/.venv/bin/python -m agent.main
Restart=always
RestartSec=5

PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=off
ProtectHome=off
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictSUIDSGID=no
RestrictRealtime=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
RemoveIPC=yes
UMask=0077

SystemCallArchitectures=native

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now ssd-agent

log "Done."
log "Agent installed in ${INSTALL_DIR}"
log "Agent user: ${AGENT_USER}"
log "Compose dir: ${COMPOSE_DIR}"
log "Service status:"
systemctl --no-pager --full status ssd-agent || true
