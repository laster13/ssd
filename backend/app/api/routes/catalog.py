from fastapi import APIRouter

from app.catalog.apps import list_catalog_apps
from app.schemas.catalog import CatalogAppItem

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get("/apps", response_model=list[CatalogAppItem])
def get_catalog():
    return [CatalogAppItem(**app) for app in list_catalog_apps()]
