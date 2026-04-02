#!/usr/bin/env bash
set -euo pipefail

PAIRING_CODE=""
BACKEND_URL=""
INSTALL_DIR="/opt/ssd-agent"
AGENT_USER=""
ALLOW_INSECURE_HTTP="${ALLOW_INSECURE_HTTP:-false}"

usage() {
  echo "Usage:"
  echo "  bootstrap.sh --pairing-code XXXX-XXXX --backend-url https://admin.example.com [--agent-user USER] [--install-dir /opt/ssd-agent]"
  echo
  echo "By default, insecure HTTP is refused."
  echo "To override temporarily (not recommended), run with:"
  echo "  ALLOW_INSECURE_HTTP=true ./bootstrap.sh ..."
  exit 1
}

detect_agent_user() {
  if [[ -n "${AGENT_USER}" ]]; then
    return 0
  fi

  if [[ -n "${SUDO_USER:-}" && "${SUDO_USER}" != "root" ]]; then
    local sudo_home
    sudo_home="$(getent passwd "${SUDO_USER}" | cut -d: -f6 || true)"
    if [[ -n "${sudo_home}" && -d "${sudo_home}/seedbox-compose" ]]; then
      AGENT_USER="${SUDO_USER}"
      return 0
    fi
  fi

  mapfile -t compose_dirs < <(find /home /root -maxdepth 2 -type d -name seedbox-compose 2>/dev/null | sort)

  if [[ "${#compose_dirs[@]}" -eq 1 ]]; then
    local detected_dir owner
    detected_dir="${compose_dirs[0]}"
    owner="$(stat -c '%U' "${detected_dir}")"

    if [[ -z "${owner}" || "${owner}" == "root" ]]; then
      echo "[bootstrap] Could not safely infer a non-root agent user from ${detected_dir}"
      echo "[bootstrap] Re-run with --agent-user <user>"
      exit 1
    fi

    AGENT_USER="${owner}"
    return 0
  fi

  if [[ "${#compose_dirs[@]}" -eq 0 ]]; then
    echo "[bootstrap] No seedbox-compose directory found under /home or /root."
  else
    echo "[bootstrap] Multiple seedbox-compose directories found:"
    printf ' - %s\n' "${compose_dirs[@]}"
  fi

  echo "[bootstrap] Unable to determine agent user automatically."
  echo "[bootstrap] Re-run with --agent-user <user>"
  exit 1
}

run_as_agent_user() {
  runuser -u "${AGENT_USER}" -- "$@"
}

if [[ "${EUID}" -ne 0 ]]; then
  echo "[bootstrap] This script must run as root."
  exit 1
fi

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pairing-code)
      PAIRING_CODE="${2:-}"
      shift 2
      ;;
    --backend-url)
      BACKEND_URL="${2:-}"
      shift 2
      ;;
    --agent-user)
      AGENT_USER="${2:-}"
      shift 2
      ;;
    --install-dir)
      INSTALL_DIR="${2:-}"
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
  echo "[bootstrap] User '${AGENT_USER}' does not exist."
  exit 1
fi

AGENT_HOME="$(getent passwd "${AGENT_USER}" | cut -d: -f6)"
if [[ -z "${AGENT_HOME}" || ! -d "${AGENT_HOME}" ]]; then
  echo "[bootstrap] Could not resolve home directory for user '${AGENT_USER}'."
  exit 1
fi

COMPOSE_DIR="${AGENT_HOME}/seedbox-compose"
if [[ ! -d "${COMPOSE_DIR}" ]]; then
  echo "[bootstrap] Expected compose directory not found: ${COMPOSE_DIR}"
  echo "[bootstrap] Create it first or use the correct agent user."
  exit 1
fi

echo "[bootstrap] Agent user resolved to: ${AGENT_USER}"
echo "[bootstrap] Agent home: ${AGENT_HOME}"
echo "[bootstrap] Compose dir: ${COMPOSE_DIR}"

echo "[bootstrap] Installing prerequisites..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv python3-pip curl ca-certificates

echo "[bootstrap] Creating install directory..."
mkdir -p "${INSTALL_DIR}/agent"
mkdir -p "${INSTALL_DIR}/logs"
chown -R "${AGENT_USER}:${AGENT_USER}" "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}/agent"
chmod 750 "${INSTALL_DIR}/logs"

echo "[bootstrap] Creating virtualenv..."
rm -rf "${INSTALL_DIR}/.venv"
run_as_agent_user python3 -m venv "${INSTALL_DIR}/.venv"
run_as_agent_user "${INSTALL_DIR}/.venv/bin/pip" install --upgrade pip
run_as_agent_user "${INSTALL_DIR}/.venv/bin/pip" install requests

echo "[bootstrap] Verifying pairing code..."

CURL_FLAGS=(-fsSL --connect-timeout 10 --max-time 30)
if [[ "${BACKEND_URL}" == https://* ]]; then
  CURL_FLAGS+=(--proto '=https' --tlsv1.2)
fi

VERIFY_RESPONSE="$(curl "${CURL_FLAGS[@]}" -X POST "${BACKEND_URL}/pairing/verify" \
  -H "Content-Type: application/json" \
  -d "{\"pairing_code\":\"${PAIRING_CODE}\"}")"

echo "[bootstrap] Pairing response received."

MACHINE_TOKEN="$(python3 - <<'PY' "${VERIFY_RESPONSE}"
import json, sys
data = json.loads(sys.argv[1])
if not data.get("valid"):
    raise SystemExit("Pairing code invalid")
print(data["machine_token"])
PY
)"

MACHINE_ID="$(python3 - <<'PY' "${VERIFY_RESPONSE}"
import json, sys
data = json.loads(sys.argv[1])
print(data["machine_id"])
PY
)"

MACHINE_UUID="$(python3 - <<'PY' "${VERIFY_RESPONSE}"
import json, sys
data = json.loads(sys.argv[1])
print(data["machine_uuid"])
PY
)"

HOSTNAME_VALUE="$(hostname)"

echo "[bootstrap] Writing agent files..."

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


def heartbeat(hostname: str, agent_version: str) -> dict:
    response = post(
        "/agent/heartbeat",
        {
            "hostname": hostname,
            "agent_version": agent_version,
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
    response.raise_for_status()
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

cat > "${INSTALL_DIR}/agent/runner.py" <<'PY'
import re
import shlex
import subprocess

from agent.api import complete_job, send_log

ALLOWED_JOB_TYPE = "install_app"
ALLOWED_INSTALL_PROFILE = "seedbox_standard"
ALLOWED_AUTH_TYPES = {"aucune", "basique", "oauth", "authelia", "oauth2-proxy"}
SLUG_RE = re.compile(r"^[a-zA-Z0-9_.+-]+$")
SUBDOMAIN_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


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


def validate_payload(payload: dict) -> tuple[str, str, str, str]:
    app_slug = str(payload.get("app_slug") or "").strip()
    install_profile = str(payload.get("install_profile") or "").strip()
    subdomain = str(payload.get("subdomain") or "").strip().lower()
    auth_type = str(payload.get("auth_type") or "").strip().lower()

    if not app_slug:
        raise ValueError("Missing app_slug in payload")

    if not SLUG_RE.fullmatch(app_slug):
        raise ValueError("Invalid app_slug format")

    if install_profile != ALLOWED_INSTALL_PROFILE:
        raise ValueError(f"Unsupported install_profile: {install_profile!r}")

    if not subdomain:
        raise ValueError("Missing subdomain in payload")

    if not SUBDOMAIN_RE.fullmatch(subdomain):
        raise ValueError("Invalid subdomain format")

    if auth_type not in ALLOWED_AUTH_TYPES:
        raise ValueError(f"Unsupported auth_type: {auth_type!r}")

    return app_slug, install_profile, subdomain, auth_type


def run_seedbox_standard(job_id: str, seq: int, app_slug: str, subdomain: str, auth_type: str) -> tuple[int, int]:
    compose_dir = '"$HOME/seedbox-compose"'
    app_slug_q = shlex.quote(app_slug)
    subdomain_q = shlex.quote(subdomain)
    auth_type_q = shlex.quote(auth_type)
    app_key_q = shlex.quote(f"sub.{app_slug}.{app_slug}")
    auth_key_q = shlex.quote(f"sub.{app_slug}.auth")

    pre_commands = [
        f"cd {compose_dir} && source profile.sh && manage_account_yml {app_key_q} {subdomain_q}",
        f"cd {compose_dir} && source profile.sh && manage_account_yml {auth_key_q} {auth_type_q}",
    ]

    for command in pre_commands:
        send_log(job_id, seq, "info", f"running command: {command}")
        seq += 1

        return_code, output = shell_line(command)

        if output:
            for line in output.splitlines():
                send_log(job_id, seq, "info", line)
                seq += 1

        if return_code != 0:
            send_log(job_id, seq, "error", f"command failed with return code={return_code}")
            complete_job(job_id, error_message=f"Preparation command failed with return code {return_code}")
            return seq, return_code

    command = f"cd {compose_dir} && source profile.sh && launch_service {app_slug_q}"

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
    return seq, return_code


def run_job(job: dict) -> None:
    job_id = job["job_id"]
    job_type = job["type"]
    payload = job.get("payload") or {}

    seq = 1

    try:
        if job_type != ALLOWED_JOB_TYPE:
            send_log(job_id, seq, "error", f"unsupported job type={job_type}")
            complete_job(job_id, error_message=f"Unsupported job type: {job_type}")
            return

        try:
            app_slug, install_profile, subdomain, auth_type = validate_payload(payload)
        except ValueError as exc:
            send_log(job_id, seq, "error", str(exc))
            complete_job(job_id, error_message=str(exc))
            return

        send_log(
            job_id,
            seq,
            "info",
            f"validated payload: app_slug={app_slug} install_profile={install_profile} subdomain={subdomain} auth_type={auth_type}",
        )
        seq += 1

        if install_profile != ALLOWED_INSTALL_PROFILE:
            send_log(job_id, seq, "error", f"unsupported install profile={install_profile}")
            complete_job(job_id, error_message=f"Unsupported install profile: {install_profile}")
            return

        seq, return_code = run_seedbox_standard(
            job_id=job_id,
            seq=seq,
            app_slug=app_slug,
            subdomain=subdomain,
            auth_type=auth_type,
        )

        if return_code == 0:
            send_log(job_id, seq, "info", f"job finished successfully for app={app_slug}")
            complete_job(
                job_id,
                result={
                    "message": "install finished",
                    "app_slug": app_slug,
                    "install_profile": install_profile,
                    "subdomain": subdomain,
                    "auth_type": auth_type,
                    "return_code": return_code,
                },
            )
        else:
            send_log(job_id, seq, "error", f"job failed with return code={return_code}")
            complete_job(
                job_id,
                error_message=f"Command failed with return code {return_code}",
            )

    except Exception as exc:
        try:
            send_log(job_id, seq, "error", f"exception: {exc}")
            complete_job(job_id, error_message=str(exc))
        except Exception:
            pass
        raise
PY

cat > "${INSTALL_DIR}/agent/main.py" <<'PY'
import time
from datetime import datetime

from agent.api import authenticate, fetch_job, heartbeat
from agent.config import AGENT_VERSION, HOSTNAME, POLL_INTERVAL
from agent.runner import run_job


def log(message: str) -> None:
    print(f"[{datetime.utcnow().isoformat()}] [agent] {message}", flush=True)


def main() -> None:
    auth_data = authenticate()
    log(f"authenticated: machine_id={auth_data['machine_id']} status={auth_data['status']}")

    while True:
        try:
            hb = heartbeat(HOSTNAME, AGENT_VERSION)
            log(f"heartbeat ok: last_seen_at={hb['last_seen_at']}")

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

cat > "${INSTALL_DIR}/.env" <<EOF
BACKEND_URL=${BACKEND_URL}
MACHINE_TOKEN=${MACHINE_TOKEN}
HOSTNAME=${HOSTNAME_VALUE}
AGENT_VERSION=0.1.0
POLL_INTERVAL=5
VERIFY_TLS=true
MACHINE_ID=${MACHINE_ID}
MACHINE_UUID=${MACHINE_UUID}
EOF

chown -R "${AGENT_USER}:${AGENT_USER}" "${INSTALL_DIR}"
chmod 600 "${INSTALL_DIR}/.env"

echo "[bootstrap] Creating systemd service..."

cat > /etc/systemd/system/ssd-agent.service <<EOF
[Unit]
Description=SSD Agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=${AGENT_USER}
Group=${AGENT_USER}
WorkingDirectory=${INSTALL_DIR}
Environment=PYTHONUNBUFFERED=1
Environment=HOME=${AGENT_HOME}
ExecStart=${INSTALL_DIR}/.venv/bin/python -m agent.main
Restart=always
RestartSec=5

NoNewPrivileges=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectSystem=full
ProtectHome=read-only
ProtectKernelTunables=yes
ProtectKernelModules=yes
ProtectControlGroups=yes
ProtectClock=yes
ProtectHostname=yes
RestrictSUIDSGID=yes
RestrictRealtime=yes
LockPersonality=yes
MemoryDenyWriteExecute=yes
RemoveIPC=yes
UMask=0077

ReadWritePaths=${COMPOSE_DIR} ${INSTALL_DIR}
SystemCallArchitectures=native

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ssd-agent
systemctl restart ssd-agent

echo "[bootstrap] Done."
echo "[bootstrap] Agent installed in ${INSTALL_DIR}"
echo "[bootstrap] Agent user: ${AGENT_USER}"
echo "[bootstrap] Compose dir: ${COMPOSE_DIR}"
echo "[bootstrap] Service status:"
systemctl --no-pager --full status ssd-agent || true