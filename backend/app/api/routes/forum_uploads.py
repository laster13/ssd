import imghdr
import mimetypes
import re
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/forum/uploads", tags=["forum-uploads"])

BACKEND_ROOT = Path(__file__).resolve().parents[3]
UPLOADS_ROOT = BACKEND_ROOT / "uploads" / "forum"

ALLOWED_IMAGE_CONTENT_TYPES = {
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
}

MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

ALLOWED_FILE_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".csv",
    ".json",
    ".zip",
    ".rar",
    ".7z",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
}

ALLOWED_FILE_CONTENT_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "text/csv",
    "application/json",
    "application/zip",
    "application/x-zip-compressed",
    "application/vnd.rar",
    "application/x-rar-compressed",
    "application/x-7z-compressed",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "application/octet-stream",
}

MAX_FILE_SIZE_BYTES = 20 * 1024 * 1024  # 20 MB


def _detect_image_extension(content_type: str, data: bytes) -> str:
    if content_type in ALLOWED_IMAGE_CONTENT_TYPES:
        return ALLOWED_IMAGE_CONTENT_TYPES[content_type]

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


def _slugify_file_stem(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "fichier"


def _detect_file_extension(upload: UploadFile) -> str:
    filename = upload.filename or ""
    suffix = Path(filename).suffix.lower()

    if suffix in ALLOWED_FILE_EXTENSIONS:
        return suffix

    guessed = mimetypes.guess_extension(upload.content_type or "")
    if guessed:
        guessed = guessed.lower()
        if guessed in ALLOWED_FILE_EXTENSIONS:
            return guessed

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=(
            "Type de fichier non autorisé. "
            "Formats acceptés : PDF, TXT, MD, CSV, JSON, ZIP, RAR, 7Z, DOC, DOCX, XLS, XLSX, PPT, PPTX."
        ),
    )


@router.post("/image")
async def upload_forum_image(
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if image.content_type not in ALLOWED_IMAGE_CONTENT_TYPES:
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

    extension = _detect_image_extension(image.content_type or "", data)

    today = datetime.utcnow()
    relative_dir = Path("images", str(today.year), f"{today.month:02d}")
    target_dir = UPLOADS_ROOT / relative_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{uuid.uuid4().hex}{extension}"
    file_path = target_dir / file_name
    file_path.write_bytes(data)

    storage_path = f"forum/images/{today.year}/{today.month:02d}/{file_name}"
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


@router.post("/file")
async def upload_forum_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    if (file.content_type or "") not in ALLOWED_FILE_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Type de fichier non autorisé. "
                "Formats acceptés : PDF, TXT, MD, CSV, JSON, ZIP, RAR, 7Z, DOC, DOCX, XLS, XLSX, PPT, PPTX."
            ),
        )

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le fichier est vide.",
        )

    if len(data) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Fichier trop lourd. Taille maximum : 20 MB.",
        )

    extension = _detect_file_extension(file)

    original_name = Path(file.filename or "fichier").stem
    safe_stem = _slugify_file_stem(original_name)

    today = datetime.utcnow()
    relative_dir = Path("files", str(today.year), f"{today.month:02d}")
    target_dir = UPLOADS_ROOT / relative_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"{safe_stem}-{uuid.uuid4().hex[:10]}{extension}"
    file_path = target_dir / file_name
    file_path.write_bytes(data)

    storage_path = f"forum/files/{today.year}/{today.month:02d}/{file_name}"
    public_url = f"/uploads/{storage_path}"
    markdown = f"[{file.filename or file_name}]({public_url})"

    return {
        "ok": True,
        "file_name": file_name,
        "original_name": file.filename or file_name,
        "content_type": file.content_type,
        "size_bytes": len(data),
        "storage_path": storage_path,
        "public_url": public_url,
        "markdown": markdown,
        "uploaded_by": str(current_user.id),
    }