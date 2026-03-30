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


load_env_file()


BACKEND_URL = os.environ["BACKEND_URL"].rstrip("/")
MACHINE_TOKEN = os.environ["MACHINE_TOKEN"]
HOSTNAME = os.environ.get("HOSTNAME", "unknown-host")
AGENT_VERSION = os.environ.get("AGENT_VERSION", "0.1.0")
POLL_INTERVAL = int(os.environ.get("POLL_INTERVAL", "5"))