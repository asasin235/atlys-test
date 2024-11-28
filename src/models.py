from pydantic import BaseModel
from typing import Optional

class Settings(BaseModel):
    pages: Optional[int] = None
    proxy: Optional[str] = None

class Product(BaseModel):
    title: str
    price: float
    image_url: str
    image_path: str