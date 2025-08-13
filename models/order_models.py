from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, UTC

class Order(BaseModel):
    products : List[str]
    total : float
    user_id: str
    shipping_address: str
    status: Optional[str] = "Pending"
    created_at: Optional[datetime] = datetime.now(UTC)