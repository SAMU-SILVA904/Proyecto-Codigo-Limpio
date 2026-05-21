"""Esquemas de validación Pydantic para la estructura relacional del Carrito."""

from pydantic import BaseModel
from src.Esquemas.producto import ProductoResponse

class ItemCarritoResponse(BaseModel):
    item_id: int
    carrito_id: int
    producto_id: int
    nombre: str
    precio_unitario: float
    cantidad: int
    producto: ProductoResponse | None = None 
    model_config = {"from_attributes": True}

class CarritoResponse(BaseModel):
    carrito_id: int
    usuario_id: int
    item_carrito: list[ItemCarritoResponse] = []
    model_config = {"from_attributes": True}
