from dataclasses import dataclass, field
from src.gerencia_app.exepciones import (
    CantidadInvalidaError,
    NombreProductoInvalidoError,
    IdProductoInvalidoError
)

@dataclass
class Producto:
    """
    Modelo para representar un producto en el inventario de la tienda.
    """
    
    producto_id: int
    nombre: str
    precio: float
    stock: int
    
    def __post_init__(self):
        if self.producto_id <= 0:
            raise IdProductoInvalidoError(self.producto_id)
        if not self.nombre.strip():
            raise NombreProductoInvalidoError(self.nombre)
        if self.precio <= 0:
            raise CantidadInvalidaError(self.precio)
        if self.stock < 0:
            raise CantidadInvalidaError(self.stock)