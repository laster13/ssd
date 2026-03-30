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