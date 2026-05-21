from pydantic import BaseModel, Field
from typing import List, Optional

class ItemCarritoBase(BaseModel):
    carrito_id: int
    producto_id: int
    nombre: str = Field(..., max_length=150)
    precio_unitario: float = Field(..., ge=0)
    cantidad: int = Field(..., gt=0)

class ItemCarrito(ItemCarritoBase):
    item_id: int

    class Config:
        from_attributes = True
