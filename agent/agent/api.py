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
        timeout=15,
    )


def get(path: str) -> requests.Response:
    return requests.get(
        f"{BACKEND_URL}{path}",
        headers=auth_headers(),
        timeout=15,
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