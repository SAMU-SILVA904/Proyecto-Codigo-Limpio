"""
Dependencias globales para la API de FastAPI.
"""

from fastapi import Depends
from src.services.usuario_service import UsuarioService
from src.services.producto_service import ProductoService
from src.services.carrito_service import CarritoService

def get_usuario_service() -> UsuarioService:
    """Provee la instancia del servicio de usuarios."""
    return UsuarioService()

def get_producto_service() -> ProductoService:
    """Provee la instancia del servicio de productos."""
    return ProductoService()

def get_carrito_service() -> CarritoService:
    """Provee la instancia del servicio de carritos de compras."""
    return CarritoService()

