#!/usr/bin/env bash
set -euo pipefail

PAIRING_CODE=""
BACKEND_URL=""
INSTALL_DIR="/opt/ssd-agent"
AGENT_USER="root"

usage() {
  echo "Usage:"
  echo "  bootstrap.sh --pairing-code XXXX-XXXX --backend-url http://IP:8000"
  exit 1
}

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
    *)
      echo "Unknown argument: $1"
      usage
      ;;
  esac
done

if [[ -z "${PAIRING_CODE}" || -z "${BACKEND_URL}" ]]; then
  usage
fi

echo "[bootstrap] Installing prerequisites..."
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y python3 python3-venv python3-pip curl ca-certificates

echo "[bootstrap] Creating install directory..."
mkdir -p "${INSTALL_DIR}/agent"
mkdir -p "${INSTALL_DIR}/logs"

echo "[bootstrap] Creating virtualenv..."
python3 -m venv "${INSTALL_DIR}/.venv"
"${INSTALL_DIR}/.venv/bin/pip" install --upgrade pip
"${INSTALL_DIR}/.venv/bin/pip" install requests

echo "[bootstrap] Verifying pairing code..."
VERIFY_RESPONSE="$(curl -fsSL -X POST "${BACKEND_URL}/pairing/verify" \
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

cat > "${INSTALL_DIR}/agent/config.py" <<'PY'
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


load_env_file("/opt/ssd-agent/.env")

BACKEND_URL = os.environ["BACKEND_URL"].rstrip("/")
MACHINE_TOKEN = os.environ["MACHINE_TOKEN"]
HOSTNAME = os.environ.get("HOSTNAME", "unknown-host")
AGENT_VERSION = os.environ.get("AGENT_VERSION", "0.1.0")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))
PY

cat > "${INSTALL_DIR}/agent/api.py" <<'PY'
import requests

from agent.config import BACKEND_URL, MACHINE_TOKEN


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


def run_job(job: dict) -> None:
    job_id = job["job_id"]
    job_type = job["type"]
    payload = job.get("payload") or {}

    seq = 1

    try:
        if job_type != "install_app":
            send_log(job_id, seq, "error", f"unsupported job type={job_type}")
            complete_job(job_id, error_message=f"Unsupported job type: {job_type}")
            return

        app_slug = payload.get("app_slug")
        subdomain = payload.get("subdomain")
        auth_type = payload.get("auth_type")

        if not app_slug:
            send_log(job_id, seq, "error", "missing app_slug in payload")
            complete_job(job_id, error_message="Missing app_slug in payload")
            return

        if not subdomain:
            send_log(job_id, seq, "error", "missing subdomain in payload")
            complete_job(job_id, error_message="Missing subdomain in payload")
            return

        if not auth_type:
            send_log(job_id, seq, "error", "missing auth_type in payload")
            complete_job(job_id, error_message="Missing auth_type in payload")
            return

        pre_commands = [
            f"cd ~/seedbox-compose && source profile.sh && manage_account_yml sub.{app_slug}.{app_slug} {subdomain}",
            f"cd ~/seedbox-compose && source profile.sh && manage_account_yml sub.{app_slug}.auth {auth_type}",
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
                return

        command = f"cd ~/seedbox-compose && source profile.sh && launch_service {app_slug}"

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

        if return_code == 0:
            send_log(job_id, seq, "info", f"job finished successfully for app={app_slug}")
            complete_job(
                job_id,
                result={
                    "message": "install finished",
                    "app_slug": app_slug,
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
MACHINE_ID=${MACHINE_ID}
MACHINE_UUID=${MACHINE_UUID}
EOF

chmod 600 "${INSTALL_DIR}/.env"

echo "[bootstrap] Creating systemd service..."

cat > /etc/systemd/system/ssd-agent.service <<EOF
[Unit]
Description=SSD Agent
After=network.target

[Service]
Type=simple
User=${AGENT_USER}
WorkingDirectory=${INSTALL_DIR}
Environment=PYTHONUNBUFFERED=1
ExecStart=${INSTALL_DIR}/.venv/bin/python -m agent.main
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ssd-agent
systemctl restart ssd-agent

echo "[bootstrap] Done."
echo "[bootstrap] Agent installed in ${INSTALL_DIR}"
echo "[bootstrap] Service status:"
systemctl --no-pager --full status ssd-agent || true