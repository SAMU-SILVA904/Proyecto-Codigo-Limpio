from typing import List
from .models import Usuario, Producto, Rol, ItemCarrito
from .storage import JSONStorage
from .exceptions import (
    StockInsuficienteError, 
    PermisoDenegadoError, 
    ElementoNoEncontradoError,
    CarritoVacioError
)

class TiendaService:
    """
    Servicio para manejar la lógica de negocio de la tienda.
    """
    
    def __init__(self, storage_usuarios: JSONStorage, storage_productos: JSONStorage):
        self.storage_u = storage_usuarios
        self.storage_p = storage_productos

    def obtener_usuarios(self) -> List[Usuario]:
        """
        Trae y devuelve la lista de usuarios del almacenamiento (base de datos).
        """
        
        return self.storage_u.load()

    def obtener_productos(self) -> List[Producto]:
        """
        Trae y devuelve la lista de productos del almacenamiento (base de datos).
        """
        
        return self.storage_p.load()

    def agregar_al_carrito(self, id_usuario: int, id_producto_buscar: int, cantidad: int):
        """
        Agrega un producto en especifico al carrito de un usuario en específico, valida: los permisos y stock.
        """
        
        usuarios = self.obtener_usuarios()
        productos = self.obtener_productos()
        
        # 1. Validar Usuario
        usuario = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_usuario), None) #Next devuelve el primer elemento que cumple la condición o None si no encuentra nada
        if not usuario:
            raise ElementoNoEncontradoError(f"Usuario {id_usuario} no encontrado")
        if usuario.rol != Rol.EMPLEADO:
            raise PermisoDenegadoError("Solo los empleados pueden usar el carrito")
        
        producto = next((este_producto for este_producto in productos if este_producto.id == id_producto_buscar), None)
        if not producto:
            raise ElementoNoEncontradoError(f"Producto {id_producto_buscar} no existe")
        
        if producto.stock < cantidad:
            raise StockInsuficienteError(f"No hay suficiente stock de {producto.nombre}")
        
        item_existente = next(
            (este_item for este_item in usuario.carrito.items if este_item.id_producto == id_producto_buscar),
            None
        )
        
        if item_existente:
            item_existente.cantidad += cantidad
        else:
            nuevo_item = ItemCarrito(
                id_producto=producto.id,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=cantidad
            )
            usuario.carrito.items.append(nuevo_item)
        
        self.storage_u.save(usuarios)

    def facturar_carrito(self, id_usuario: int):
        """
        Se encarga de facturar el carrito de un usuario, valida el stock y actualiza el inventario.
        """
        
        usuarios = self.obtener_usuarios()
        productos = self.obtener_productos()

        usuario = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_usuario), None)
        if not usuario or not usuario.carrito.items:
            raise CarritoVacioError("El carrito está vacío o el usuario no existe")

        for item in usuario.carrito.items:
            prod_inventario = next((este_producto for este_producto in productos if este_producto.id == item.id_producto), None)
            if not prod_inventario or prod_inventario.stock < item.cantidad:
                raise StockInsuficienteError(f"Error en factura: {item.nombre} ya no tiene stock suficiente")

        for item in usuario.carrito.items:
            prod_inventario = next((este_producto for este_producto in productos if este_producto.id == item.id_producto), None)
            if not prod_inventario:
                raise ElementoNoEncontradoError(f"Producto {item.id_producto} no encontrado en inventario")
            prod_inventario.stock -= item.cantidad

        usuario.carrito.items = []

        self.storage_p.save(productos)
        self.storage_u.save(usuarios)

    def crear_producto(self, id_gerente: int, nombre: str, precio: float, stock: int):
        """
        Crea un nuevo producto y valida que el usuario sea gerente (permiso necesario).
        """
        
        usuarios = self.obtener_usuarios()
        gerente = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_gerente), None)

        if not gerente or gerente.rol != Rol.GERENTE:
            raise PermisoDenegadoError("Acceso denegado: Se requiere rol de Gerente")

        productos = self.obtener_productos()
        nuevo_id = max([este_producto.id for este_producto in productos], default=0) + 1
        nuevo_producto = Producto(id=nuevo_id, nombre=nombre, precio=precio, stock=stock)
        
        productos.append(nuevo_producto)
        self.storage_p.save(productos)