from pydantic import BaseModel


class CatalogAppItem(BaseModel):
    slug: str
    name: str
    category: str
    tagline: str
    description: str
    status: str
    enabled: bool
    install_profile: str
    allowed_auth_types: list[str]