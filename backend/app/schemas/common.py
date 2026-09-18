from pydantic import BaseModel, Field


class PageMeta(BaseModel):
    page: int = Field(ge=1)
    limit: int = Field(ge=1, le=200)
    total: int | None = None
    has_more: bool = False


class HealthStatus(BaseModel):
    status: str
    detail: str | None = None
