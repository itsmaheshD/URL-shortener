from sqlmodel import Field,SQLModel
from datetime import datetime

class UrlRecord(SQLModel):
    id:int |None = Field(default=None, primary_key=True)

    original_url:str|None =Field(default=None)

    short_code_url:str = Field(
        index=True,
        unique=True
    )

    created_at:datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


