from pydantic import BaseModel
from datetime import datetime


class Session(BaseModel):
    id: int = None
    role: str = None
    expiration_timestamp: datetime = None
