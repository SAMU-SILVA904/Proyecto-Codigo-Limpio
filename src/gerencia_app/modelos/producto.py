from dataclasses import dataclass, field

@dataclass
class Producto:
    """
    Modelo para representar un producto en el inventario de la tienda.
    """
    
    producto_id: int
    nombre: str
    precio: float
    stock: int