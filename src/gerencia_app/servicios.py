from rich.table import Table
from rich.console import Console
from typing import List
from .models import Usuario, Producto, Rol, ItemCarrito
from .storage import JSONStorage
from .exceptions import (
    StockInsuficienteError, 
    PermisoDenegadoError, 
    UsuarioNoEncontradoError,
    ProductoNoEncontradoError,
    CarritoVacioError
)

class TiendaService:
    """
    Servicio para manejar la lógica de negocio de la tienda.
    """
    
    def __init__(self, storage_usuarios: JSONStorage, storage_productos: JSONStorage):
        self.storage_usuarios = storage_usuarios
        self.storage_productos = storage_productos

    def obtener_usuarios(self) -> List[Usuario]:
        """
        Trae y devuelve la lista de usuarios del almacenamiento (base de datos).
        """
        
        return self.storage_usuarios.load()

    def obtener_productos(self) -> List[Producto]:
        """
        Trae y devuelve la lista de productos del almacenamiento (base de datos).
        """
        
        return self.storage_productos.load()

    def agregar_al_carrito(self, id_usuario: int, id_producto_buscar: int, cantidad: int) -> None:
        """
        Agrega un producto en especifico al carrito de un usuario en específico, valida: los permisos y stock.
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        productos: list[Producto] = self.obtener_productos()
        
        usuario: Usuario = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_usuario), None) #Next devuelve el primer elemento que cumple la condición o None si no encuentra nada
        if not usuario:
            raise UsuarioNoEncontradoError(id_usuario)
        if usuario.rol != Rol.EMPLEADO:
            raise PermisoDenegadoError("Solo los empleados pueden usar el carrito")
        
        producto: Producto = next((este_producto for este_producto in productos if este_producto.id == id_producto_buscar), None)
        if not producto:
            raise ProductoNoEncontradoError(id_producto_buscar)
        
        if producto.stock < cantidad:
            raise StockInsuficienteError(f"No hay suficiente stock de {producto.nombre}")
        
        item_existente: ItemCarrito = next((este_item for este_item in usuario.carrito.items if este_item.id_producto == id_producto_buscar),None)
        
        if item_existente:
            item_existente.cantidad += cantidad
        else:
            nuevo_item: ItemCarrito = ItemCarrito(
                id_producto=producto.id,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=cantidad
            )
            usuario.carrito.items.append(nuevo_item)
        
        self.storage_usuarios.save(usuarios)

    def facturar_carrito(self, id_usuario: int) -> None:
        """
        Se encarga de facturar el carrito de un usuario, valida el stock, permiso de usuario y actualiza el inventario.
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        productos: list[Producto] = self.obtener_productos()

        usuario: Usuario = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_usuario), None)
        if not usuario:
            raise UsuarioNoEncontradoError(id_usuario)
        if usuario.rol != Rol.EMPLEADO:
            raise PermisoDenegadoError("Solo los empleados pueden facturar el carrito")
        if not usuario.carrito.items:
            raise CarritoVacioError("El carrito está vacío, no se puede facturar")

        for item in usuario.carrito.items:
            producto_en_inventario: Producto = next((este_producto for este_producto in productos if este_producto.id == item.id_producto), None)
            if not producto_en_inventario or producto_en_inventario.stock < item.cantidad:
                raise StockInsuficienteError(f"Error en factura: {item.nombre} ya no tiene stock suficiente")

        for item in usuario.carrito.items:
            producto_en_inventario: Producto = next((este_producto for este_producto in productos if este_producto.id == item.id_producto), None)
            if not producto_en_inventario:
                raise ElementoNoEncontradoError(f"Producto {item.id_producto} no encontrado en inventario")
            producto_en_inventario.stock -= item.cantidad

        usuario.carrito.items = []

        self.storage_productos.save(productos)
        self.storage_usuarios.save(usuarios)

    def crear_producto(self, id_gerente: int, nombre: str, precio: float, stock: int) -> None:
        """
        Crea un nuevo producto y valida que el usuario sea gerente (permiso necesario).
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        gerente: Usuario = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_gerente), None)

        if not gerente or gerente.rol != Rol.GERENTE:
            raise PermisoDenegadoError("Acceso denegado: Se requiere rol de Gerente")

        productos: list[Producto] = self.obtener_productos()
        nuevo_id: int = max([este_producto.id for este_producto in productos], default=0) + 1
        nuevo_producto: Producto = Producto(id=nuevo_id, nombre=nombre, precio=precio, stock=stock)
        
        productos.append(nuevo_producto)
        self.storage_productos.save(productos)
        
    def crear_usuario(self, id_gerente: int, nombre_usuario: str, rol: Rol) -> None:
        """
        Crea un nuevo usuario y valida que el usuario que realiza la acción sea gerente (permiso necesario).
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        gerente: Usuario = next((este_usuario for este_usuario in usuarios if este_usuario.id == id_gerente), None)

        if not gerente or gerente.rol != Rol.GERENTE:
            raise PermisoDenegadoError("Acceso denegado: Se requiere rol de Gerente")

        nuevo_id: int = max([este_usuario.id for este_usuario in usuarios], default=0) + 1
        nuevo_usuario: Usuario = Usuario(id=nuevo_id, nombre_usuario=nombre_usuario, rol=rol)
        
        usuarios.append(nuevo_usuario)
        self.storage_usuarios.save(usuarios)
        