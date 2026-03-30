from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(tags=["bootstrap"])


@router.get("/bootstrap.sh")
def get_bootstrap_script():
    script_path = Path(__file__).resolve().parents[3] / "bootstrap.sh"

    if not script_path.exists():
        raise HTTPException(status_code=404, detail="bootstrap.sh not found")

    return FileResponse(
        path=script_path,
        media_type="text/x-shellscript",
        filename="bootstrap.sh",
    )
