from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CatalogAppFieldOption(BaseModel):
    value: str
    label: str


class CatalogAppField(BaseModel):
    name: str
    label: str
    type: str = "text"
    required: bool = False
    secret: bool = False
    placeholder: str | None = None
    default: Any | None = None
    options: list[CatalogAppFieldOption] = Field(default_factory=list)


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
    aliases: list[str] = Field(default_factory=list)
    form_fields: list[CatalogAppField] = Field(default_factory=list)