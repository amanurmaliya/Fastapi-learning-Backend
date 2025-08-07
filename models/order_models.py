from pydantic import BaseModel
from typing import List

class Order(BaseModel):
    products : List[str]
    total : float
