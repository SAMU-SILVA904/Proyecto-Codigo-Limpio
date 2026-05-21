"""Esquemas de validación Pydantic para la entidad Producto según el SQL real."""

from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., examples=["Leche Entera 1L"])
    precio: float = Field(..., gt=0, examples=[4200.0])
    stock: int = Field(..., ge=0, examples=[50])

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    producto_id: int
    model_config = {"from_attributes": True}

