from dataclasses import dataclass, field
from enum import Enum
from typing import List

class Rol(Enum):
    """
    Enum para definir los roles de los usuarios en la tienda.
    """
    
    GERENTE = "gerente"
    EMPLEADO = "empleado"

@dataclass
class ItemCarrito:
    """
    Modelo para representar un item dentro del carrito de compras.
    """
    
    id_producto: int
    nombre: str
    precio_unitario: float
    cantidad: int

@dataclass
class Carrito:
    """
    Modelo para representar el carrito de compras de un usuario, contiene una lista de items.
    """
    
    items: List[ItemCarrito] = field(default_factory=list)

@dataclass
class Usuario:
    """
    Modelo para representar un usuario de la tienda, con su rol y carrito de compras.
    """
    
    id: int
    nombre_usuario: str
    rol: Rol
    carrito: Carrito = field(default_factory=Carrito)

@dataclass
class Producto:
    """
    Modelo para representar un producto en el inventario de la tienda.
    """
    
    id: int
    nombre: str
    precio: float
    stock: int