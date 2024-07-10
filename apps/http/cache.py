from pydantic import BaseModel, Field

from src.shared.domain.date_utils import DateUtils
from datetime import datetime


class Cache(BaseModel):
    data: dict
    created_at: datetime = Field(default_factory=lambda: DateUtils.utc_now())
