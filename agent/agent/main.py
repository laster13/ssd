import time

from agent.api import authenticate, fetch_job, heartbeat
from agent.config import AGENT_VERSION, HOSTNAME, POLL_INTERVAL
from agent.runner import run_job


def main() -> None:
    auth_data = authenticate()
    print(f"[agent] authenticated: machine_id={auth_data['machine_id']} status={auth_data['status']}")

    while True:
        try:
            hb = heartbeat(HOSTNAME, AGENT_VERSION)
            print(f"[agent] heartbeat ok: last_seen_at={hb['last_seen_at']}")

            job_response = fetch_job()

            if job_response.get("has_job"):
                print(f"[agent] received job: {job_response['job_id']} type={job_response['type']}")
                run_job(job_response)
                print(f"[agent] finished job: {job_response['job_id']}")
            else:
                print("[agent] no job")

        except Exception as exc:
            print(f"[agent] error: {exc}")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()