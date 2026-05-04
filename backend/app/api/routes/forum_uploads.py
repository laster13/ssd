import imghdr
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/forum/uploads", tags=["forum-uploads"])

BACKEND_ROOT = Path(__file__).resolve().parents[3]
UPLOADS_ROOT = BACKEND_ROOT / "uploads" / "forum"

ALLOWED_CONTENT_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
}

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


def _detect_extension(content_type: str, data: bytes) -> str:
    if content_type in ALLOWED_CONTENT_TYPES:
        return ALLOWED_CONTENT_TYPES[content_type]

    detected = imghdr.what(None, h=data)
    if detected == "png":
        return ".png"
    if detected in {"jpeg", "jpg"}:
        return ".jpg"
    if detected == "webp":
        return ".webp"
    if detected == "gif":
        return ".gif"

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Format d'image non supporté. Utilise PNG, JPG, WEBP ou GIF.",
    )


@router.post("/image")
async def upload_forum_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if image.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type de fichier non autorisé. Utilise PNG, JPG, WEBP ou GIF.",
        )

    data = await image.read()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier est vide.",
        )

    if len(data) > MAX_IMAGE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image trop lourde. Taille maximum : 5 MB.",
        )

    extension = _detect_extension(image.content_type or "", data)

    today = datetime.utcnow()
    relative_dir = Path(str(today.year), f"{today.month:02d}")
    target_dir = UPLOADS_ROOT / relative_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}{extension}"
    file_path = target_dir / file_name
    file_path.write_bytes(data)

    storage_path = f"forum/{today.year}/{today.month:02d}/{file_name}"
    public_url = f"/uploads/{storage_path}"

    return {
        "ok": True,
        "file_name": file_name,
        "content_type": image.content_type,
        "size_bytes": len(data),
        "storage_path": storage_path,
        "public_url": public_url,
        "markdown": f"![image]({public_url})",
        "uploaded_by": str(current_user.id),
    }