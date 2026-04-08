from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(tags=["bootstrap"])


def _backend_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _serve_shell_script(filename: str) -> FileResponse:
    script_path = _backend_root() / filename

    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"{filename} not found")

    return FileResponse(
        path=script_path,
        media_type="text/x-shellscript",
        filename=filename,
    )


@router.get("/bootstrap.sh")
def get_bootstrap_script():
    return _serve_shell_script("bootstrap.sh")


@router.get("/install-ssd-local.sh")
def get_install_ssd_local_script():
    return _serve_shell_script("install-ssd-local.sh")