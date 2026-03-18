from dataclasses import dataclass, field
from src.gerencia_app.exepciones import (
    CantidadInvalidaError,
    IdUsuarioInvalidoError,
    UsuarioNoEncontradoError,
    PermisoDenegadoError,
    UsuarioYaExisteError,
    NombreUsuarioInvalidoError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
    NombreProductoInvalidoError,
    IdProductoInvalidoError,
    CarritoVacioError,
    StockInsuficienteError
)


@dataclass
class ItemCarrito:
    """
    Modelo para representar un item dentro del carrito de compras y validar sus datos.
    """
    
    producto_id: int
    nombre: str
    precio_unitario: float
    cantidad: int

    def __post_init__(self):
        if self.producto_id <= 0:
            raise IdProductoInvalidoError(self.producto_id)
        if not self.nombre.strip():
            raise NombreProductoInvalidoError(self.nombre)
        if self.precio_unitario <= 0:
            raise CantidadInvalidaError(self.precio_unitario)