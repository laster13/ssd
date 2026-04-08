from pydantic import BaseModel, ConfigDict


class CatalogAppItem(BaseModel):
    model_config = ConfigDict(extra="ignore")

    slug: str
    name: str
    category: str
    tagline: str
    description: str
    status: str
    enabled: bool
    install_profile: str
    allowed_auth_types: list[str]

    docs_status: str | None = None
    docs_repo_path: str | None = None
    docs_url: str | None = None

    variant_of: str | None = None
    aliases: list[str] = []