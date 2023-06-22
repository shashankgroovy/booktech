from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class LiveData(BaseModel):
    id: int
    uuid: UUID
    price: float
    currency: str
    last_seen: datetime
    
