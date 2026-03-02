from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List

class Rol(Enum):
    GERENTE = "gerente"
    EMPLEADO = "empleado"

@dataclass
class ItemCarrito:
    producto_id: int
    nombre: str
    precio_unitario: float
    cantidad: int

@dataclass
class Carrito:
    items: List[ItemCarrito] = field(default_factory=list)

@dataclass
class Usuario:
    id: int
    username: str
    rol: Rol
    carrito: Carrito = field(default_factory=Carrito)

@dataclass
class Producto:
    id: int
    nombre: str
    precio: float
    stock: int