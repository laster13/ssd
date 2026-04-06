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
mkdir -p "${INSTALL_DIR}/tmp/ansible"
mkdir -p "${AGENT_HOME}/.ansible/tmp"
mkdir -p "${AGENT_HOME}/seedbox"

chown -R "${AGENT_USER}:${AGENT_USER}" "${INSTALL_DIR}"
chown -R "${AGENT_USER}:${AGENT_USER}" "${AGENT_HOME}/.ansible"
chown -R "${AGENT_USER}:${AGENT_USER}" "${AGENT_HOME}/seedbox"

chmod 750 "${INSTALL_DIR}"
chmod 750 "${INSTALL_DIR}/agent"
chmod 750 "${INSTALL_DIR}/logs"
chmod 750 "${INSTALL_DIR}/tmp"
chmod 750 "${INSTALL_DIR}/tmp/ansible"

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


def heartbeat(hostname: str, agent_version: str, ssdv2_installed: bool) -> dict:
    response = post(
        "/agent/heartbeat",
        {
            "hostname": hostname,
            "agent_version": agent_version,
            "ssdv2_installed": ssdv2_installed,
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

cat > "${INSTALL_DIR}/agent/main.py" <<'PY'
import time
from datetime import datetime, timezone
from pathlib import Path

from agent.api import authenticate, fetch_job, heartbeat
from agent.config import AGENT_VERSION, HOSTNAME, POLL_INTERVAL
from agent.runner import run_job


def log(message: str) -> None:
    print(f"[{datetime.now(timezone.utc).isoformat()}] [agent] {message}", flush=True)


def is_ssdv2_installed() -> bool:
    target = Path.home() / "seedbox-compose" / "ssddb"
    return target.exists()


def main() -> None:
    auth_data = authenticate()
    log(f"authenticated: machine_id={auth_data['machine_id']} status={auth_data['status']}")

    while True:
        try:
            ssdv2_installed = is_ssdv2_installed()

            hb = heartbeat(HOSTNAME, AGENT_VERSION, ssdv2_installed)
            log(
                f"heartbeat ok: last_seen_at={hb['last_seen_at']} "
                f"ssdv2_installed={ssdv2_installed}"
            )

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

    pre_commands = [
        f"cd ~/seedbox-compose && source profile.sh && manage_account_yml sub.{quote(app_slug)}.{quote(app_slug)} {quote(subdomain)}",
        f"cd ~/seedbox-compose && source profile.sh && manage_account_yml sub.{quote(app_slug)}.auth {quote(auth_type)}",
    ]

    for command in pre_commands:
        return_code, seq = run_logged_command(job_id, seq, command)
        if return_code != 0:
            send_log(job_id, seq, "error", f"command failed with return code={return_code}")
            seq += 1
            return False, seq, None, f"Preparation command failed with return code {return_code}"

    command = f"cd ~/seedbox-compose && source profile.sh && launch_service {quote(app_slug)}"
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


def run_install_ssdv2(job_id: str, payload: dict, seq: int) -> tuple[bool, int, dict | None, str | None]:
    required_keys = [
        "username",
        "email",
        "domain",
        "password",
        "cloudflare_login",
        "cloudflare_api_key",
    ]

    missing = [key for key in required_keys if not str(payload.get(key) or "").strip()]
    if missing:
        return False, seq, None, f"Missing required payload fields: {', '.join(missing)}"

    oauth_enabled = bool(payload.get("oauth_enabled"))

    if oauth_enabled:
        oauth_missing = [
            key
            for key in ["oauth_client", "oauth_secret", "oauth_mail"]
            if not str(payload.get(key) or "").strip()
        ]
        if oauth_missing:
            return False, seq, None, f"Missing required OAuth payload fields: {', '.join(oauth_missing)}"

    compose_dir = "~/seedbox-compose"
    profile_prefix = f"cd {compose_dir} && source profile.sh"

    pre_commands: list[tuple[str, str]] = [
        ("updating all.yml: username", f"{profile_prefix} && manage_account_yml username {quote(payload.get('username'))}"),
        ("updating all.yml: email", f"{profile_prefix} && manage_account_yml email {quote(payload.get('email'))}"),
        ("updating all.yml: domain", f"{profile_prefix} && manage_account_yml domain {quote(payload.get('domain'))}"),
        ("updating all.yml: password", f"{profile_prefix} && manage_account_yml password {quote(payload.get('password'))}"),
        ("updating all.yml: cloudflare_login", f"{profile_prefix} && manage_account_yml cloudflare_login {quote(payload.get('cloudflare_login'))}"),
        ("updating all.yml: cloudflare_api_key", f"{profile_prefix} && manage_account_yml cloudflare_api_key {quote(payload.get('cloudflare_api_key'))}"),
        ("updating all.yml: oauth_enabled", f"{profile_prefix} && manage_account_yml oauth_enabled {quote(str(oauth_enabled).lower())}"),
    ]

    if oauth_enabled:
        pre_commands.extend(
            [
                ("updating all.yml: oauth_client", f"{profile_prefix} && manage_account_yml oauth_client {quote(payload.get('oauth_client'))}"),
                ("updating all.yml: oauth_secret", f"{profile_prefix} && manage_account_yml oauth_secret {quote(payload.get('oauth_secret'))}"),
                ("updating all.yml: oauth_mail", f"{profile_prefix} && manage_account_yml oauth_mail {quote(payload.get('oauth_mail'))}"),
            ]
        )

    for label, command in pre_commands:
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

    command = f"cd {compose_dir} && source profile.sh && bash install.sh"
    return_code, seq = run_streaming_command(job_id, seq, command)

    if return_code == 0:
        result = {
            "message": "SSDv2 install finished",
            "domain": payload.get("domain"),
            "oauth_enabled": oauth_enabled,
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
        elif job_type == "install_ssdv2":
            success, seq, result, error_message = run_install_ssdv2(job_id, payload, seq)
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
systemctl enable ssd-agent
systemctl restart ssd-agent

echo "[bootstrap] Done."
echo "[bootstrap] Agent installed in ${INSTALL_DIR}"
echo "[bootstrap] Agent user: ${AGENT_USER}"
echo "[bootstrap] Compose dir: ${COMPOSE_DIR}"
echo "[bootstrap] Service status:"
systemctl --no-pager --full status ssd-agent || true