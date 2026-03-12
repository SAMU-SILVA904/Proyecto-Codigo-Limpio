from dataclasses import dataclass, field
from.item_carrito import ItemCarrito
from typing import List


@dataclass
class Carrito:
    """
    Modelo para representar el carrito de compras de un usuario, contiene una lista de items.
    """
    
    items: List[ItemCarrito] = field(default_factory=list)
