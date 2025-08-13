from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    name : str
    price : float
    description : Optional[str]
    stock : int
    image_url: Optional[str]
    category: Optional[str]
    rating: Optional[float] = 0.0
    
class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    description: Optional[str]
    stock: Optional[int]
    image_url: Optional[str]
    category: Optional[str]
    rating: Optional[float]
    
class ProductSearch(BaseModel):
    query : str
    
    
class ProductFilter(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_rating: Optional[float] = None