from rich.table import Table
from rich.console import Console
from typing import List

from src.gerencia_app.modelos.usuario import Usuario
from src.gerencia_app.modelos.rol import Rol
from src.gerencia_app.modelos.producto import Producto
from src.gerencia_app.modelos.carrito import Carrito
from src.gerencia_app.modelos.item_carrito import ItemCarrito
from .almacenamiento import JSONStorage

from src.gerencia_app.exepciones import (
    StockInsuficienteError, 
    PermisoDenegadoError, 
    UsuarioNoEncontradoError,
    ProductoNoEncontradoError,
    CarritoVacioError,
    UsuarioYaExisteError,
    ProductoYaExisteError,
    CantidadInvalidaError,
    IdUsuarioInvalidoError,
    IdProductoInvalidoError
)

class TiendaServicios:
    """
    Servicio para manejar la lógica de negocio de la tienda.
    """
    
    def __init__(self, almacenamiento_usuarios: JSONStorage, almacenamiento_productos: JSONStorage):
        self.almacenamiento_usuarios = almacenamiento_usuarios
        self.almacenamiento_productos = almacenamiento_productos

    def obtener_usuarios(self) -> List[Usuario]:
        """
        Trae y devuelve la lista de usuarios del almacenamiento (base de datos).
        """
        
        return self.almacenamiento_usuarios.load()

    def obtener_productos(self) -> List[Producto]:
        """
        Trae y devuelve la lista de productos del almacenamiento (base de datos).
        """
        
        return self.almacenamiento_productos.load()


    def obtener_usuario_por_id(self, id_usuario: int) -> Usuario:
        """
        Trae y devuelve un usuario específico según su ID.
        Valida: el id del usuario.
        """
        
        if id_usuario <= 0:
            raise IdUsuarioInvalidoError(id_usuario)
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        usuario: Usuario = next((este_usuario for este_usuario in usuarios if este_usuario.usuario_id == id_usuario), None)
        
        if not usuario:
            raise UsuarioNoEncontradoError(id_usuario)
        
        return usuario

    def obtener_producto_por_id(self, id_producto: int) -> Producto:
        """
        Trae y devuelve un producto específico según su ID.
        Valida: el id del producto.
        """
        
        if id_producto <= 0:
            raise IdProductoInvalidoError(id_producto)
        
        productos: list[Producto] = self.obtener_productos()
        producto: Producto = next((este_producto for este_producto in productos if este_producto.producto_id == id_producto), None)
        
        if not producto:
            raise ProductoNoEncontradoError(id_producto)
        
        return producto

    def obtener_item_carrito_por_id(self, usuario: Usuario, id_producto: int) -> ItemCarrito:
        """
        Trae y devuelve un item específico del carrito de un usuario según el ID del producto.
        Valida: el id del usuario, el id del producto y si el producto está en el carrito.
        """
        
        item_carrito: ItemCarrito = next((este_item for este_item in usuario.carrito.items if este_item.producto_id == id_producto), None)
        
        return item_carrito


    def validar_usuario_gerente(self, usuario: Usuario) -> None:
        """
        Valida que un usuario específico tenga rol de gerente.
        """
        
        if usuario.rol != Rol.GERENTE:
            raise PermisoDenegadoError("Acceso denegado: Se requiere rol de Gerente")

    def validar_usuario_empleado(self, usuario: Usuario) -> None:
        """
        Valida que un usuario específico tenga rol de empleado.
        Valida: el id del usuario y su rol.
        """
        
        if usuario.rol != Rol.EMPLEADO:
            raise PermisoDenegadoError("Acceso denegado: Se requiere rol de Empleado")

    def validar_stock_suficiente(self, cantidad_solicitada: int, producto: Producto) -> None:
        """
        Valida que la cantidad solicitada de un producto no supere el stock disponible.
        Valida: la cantidad solicitada y el stock disponible.
        """
        
        if producto.stock < cantidad_solicitada:
            raise StockInsuficienteError(producto.producto_id, producto.stock) 

    def validar_carrito_no_vacio(self, lista: list[ItemCarrito]) -> None:
        """
        Valida que el carrito no esté vacío.
        """
        if not lista:
            raise CarritoVacioError() # Unica exepción que no recibe parámetros porque el mensaje de error es fijo ya que solo se da en un unico caso.

    def validar_lista_usuarios_no_vacia(self, usuarios: List[Usuario]) -> None:
        """
        Valida que la lista de usuarios no esté vacía antes de mostrarla.
        """
        if not usuarios:
            raise UsuarioNoEncontradoError("No hay usuarios en el sistema")

    def validar_lista_productos_no_vacia(self, productos: List[Producto]) -> None:
        """
        Valida que la lista de productos no esté vacía antes de mostrarla.
        """
        if not productos:
            raise ProductoNoEncontradoError("No hay productos en el inventario")

    def validar_cantidad_valida(self, cantidad: int) -> None:
        """
        Valida que la cantidad ingresada sea un número entero positivo.
        """
        if cantidad <= 0:
            raise CantidadInvalidaError(cantidad)


    def agregar_al_carrito(self, id_usuario: int, id_producto: int, cantidad: int) -> None:
        """
        Agrega un producto en especifico al carrito de un usuario en específico.
        Valida: Los permisos (solo empleados pueden usar el carrito) y stock.
        """
        
        self.validar_cantidad_valida(cantidad=cantidad)
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        
        usuario_actual: Usuario = self.obtener_usuario_por_id(id_usuario=id_usuario)
        self.validar_usuario_empleado(usuario = usuario_actual)
        
        producto: Producto = self.obtener_producto_por_id(id_producto=id_producto)
        self.validar_stock_suficiente(cantidad_solicitada=cantidad, producto=producto)
        
        item_existente: ItemCarrito = self.obtener_item_carrito_por_id(usuario=usuario_actual, id_producto=id_producto)
        
        if item_existente:
            item_existente.cantidad += cantidad
        else:
            nuevo_item: ItemCarrito = ItemCarrito(
                producto_id=producto.producto_id,
                nombre=producto.nombre,
                precio_unitario=producto.precio,
                cantidad=cantidad
            )
            usuario_actual.carrito.items.append(nuevo_item)
        
        self.almacenamiento_usuarios.save(usuarios)

    def facturar_carrito(self, id_usuario: int) -> None:
        """
        Se encarga de facturar el carrito de un usuario  y actualiza el inventario.
        Valida: el id del usuario, el stock y permiso de usuario (solo empleados pueden facturar).
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        productos: list[Producto] = self.obtener_productos()

        usuario_actual: Usuario = self.obtener_usuario_por_id(id_usuario=id_usuario)
        self.validar_usuario_empleado(usuario = usuario_actual)
        self.validar_carrito_no_vacio(lista = usuario_actual.carrito.items)

        for item in usuario_actual.carrito.items:
            producto_en_inventario: Producto = self.obtener_producto_por_id(id_producto=item.producto_id)
            self.validar_stock_suficiente(cantidad_solicitada=item.cantidad, producto=producto_en_inventario)
            producto_en_inventario.stock -= item.cantidad
        
        usuario_actual.carrito.items = []

        self.almacenamiento_productos.save(productos)
        self.almacenamiento_usuarios.save(usuarios)

    def quitar_producto_del_carrito(self, id_usuario: int, id_producto: int) -> None:
        """
        Elimina un producto específico del carrito de un usuario.
        Valida: el id del usuario, el id del producto, el permiso de usuario (solo empleados pueden usar el carrito) y si el producto está en el carrito.
        """

        usuarios: list[Usuario] = self.obtener_usuarios()
        usuario_actual: Usuario = self.obtener_usuario_por_id(id_usuario=id_usuario)
        self.validar_usuario_empleado(usuario = usuario_actual)
        
        
        item_a_eliminar: ItemCarrito = self.obtener_item_carrito_por_id(usuario=usuario_actual, id_producto=id_producto)
        
        usuario_actual.carrito.items.remove(item_a_eliminar)
        self.almacenamiento_usuarios.save(usuarios)

    def agregar_stock_producto(self, id_gerente: int, id_producto: int, cantidad_a_agregar: int) -> None:
        """
        Agrega stock a un producto específico en el inventario.
        Valida: el id del gerente, el id del producto, la cantidad a agregar y permiso de usuario (solo gerentes pueden ejecutar esta acción).
        """
        
        productos: list[Producto] = self.obtener_productos()
        
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)

        producto_a_actualizar: Producto = self.obtener_producto_por_id(id_producto=id_producto)
        self.validar_cantidad_valida(cantidad_a_agregar)

        producto_a_actualizar.stock += cantidad_a_agregar
        self.almacenamiento_productos.save(productos)

    def crear_producto(self, id_gerente: int, nombre_nuevo_producto: str, precio_nuevo_producto: float, stock_nuevo_producto: int) -> None:
        """
        Crea un nuevo producto.
        Valida: el id del gerente, nombre, precio, stock y permiso de usuario (solo gerentes pueden ejecutarla).
        """
        
        productos: list[Producto] = self.obtener_productos()
        
        
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)
        
        productos: list[Producto] = self.obtener_productos()
        
        if any(este_producto.nombre.lower() == nombre_nuevo_producto.lower() for este_producto in productos): #Any devuelve True si al menos un elemento del iterable cumple la condición
            raise ProductoYaExisteError(nombre_nuevo_producto)
        
        
        nuevo_id: int = max([este_producto.producto_id for este_producto in productos], default=0) + 1
        nuevo_producto: Producto = Producto(producto_id=nuevo_id, nombre=nombre_nuevo_producto, precio=precio_nuevo_producto, stock=stock_nuevo_producto)
        
        productos.append(nuevo_producto)
        self.almacenamiento_productos.save(productos)

    def crear_usuario(self, id_gerente: int, nombre_nuevo_usuario: str, rol_nuevo_usuario: Rol) -> None:
        """
        Crea un nuevo usuario.
        Valida: el id del gerente, nombre de usuario, rol y permiso de usuario (solo gerentes pueden ejecutarla).
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)

        if any(este_usuario.nombre_usuario.lower() == nombre_nuevo_usuario.lower() for este_usuario in usuarios):
            raise UsuarioYaExisteError(nombre_nuevo_usuario)
        
        nuevo_id: int = max([este_usuario.usuario_id for este_usuario in usuarios], default=0) + 1
        nuevo_usuario: Usuario = Usuario(usuario_id=nuevo_id, nombre_usuario=nombre_nuevo_usuario, rol=rol_nuevo_usuario)
        
        usuarios.append(nuevo_usuario)
        self.almacenamiento_usuarios.save(usuarios)

    def eliminar_producto(self, id_gerente: int, id_producto: int) -> None:
        """
        Elimina un producto del inventario.
        Valida: el id del gerente, el id del producto y permiso de usuario (solo gerentes pueden ejecutar esta acción).
        """
        
        if id_gerente <= 0:
            raise IdUsuarioInvalidoError(id_gerente)
        
        if id_producto <= 0:
            raise IdProductoInvalidoError(id_producto)
        
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)

        productos: list[Producto] = self.obtener_productos()
        producto_a_eliminar: Producto =self.obtener_producto_por_id(id_producto=id_producto)
        
        productos.remove(producto_a_eliminar)
        self.almacenamiento_productos.save(productos)

    def eliminar_usuario(self, id_gerente: int, id_usuario: int) -> None:
        """
        Elimina un usuario del sistema.
        Valida: el id del gerente, el id del usuario y permiso de usuario (solo gerentes pueden ejecutar esta acción).
        """
        
        usuarios: list[Usuario] = self.obtener_usuarios()
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)
        

        usuario_a_eliminar: Usuario = self.obtener_usuario_por_id(id_usuario=id_usuario)
        
        usuarios.remove(usuario_a_eliminar)
        self.almacenamiento_usuarios.save(usuarios)

    def mostrar_carrito(self, id_usuario: int) -> None:
        """
        Muestra el contenido del carrito de un usuario en forma de tabla usando Rich.
        Valida: Si el carrito está vacío.
        """
        
        console: Console = Console()
        
        usuario: Usuario = self.obtener_usuario_por_id(id_usuario=id_usuario)
        self.validar_carrito_no_vacio(usuario.carrito.items)
        
        tabla_carrito: Table = Table(title=f"Carrito de {usuario.nombre_usuario}", show_header=True, header_style="orange1") # show_header=True muestra el encabezado de la tabla y header_style le da estilo al encabezado
        tabla_carrito.add_column("ID Producto", style="cyan", width=12)
        tabla_carrito.add_column("Nombre", style="green", width=20)
        tabla_carrito.add_column("Precio Unitario", style="yellow", width=15)
        tabla_carrito.add_column("Cantidad", style="blue", width=10)
        tabla_carrito.add_column("Subtotal", style="red", width=15)
        
        total_carrito: float = 0
        for item in usuario.carrito.items:
            subtotal: float = item.precio_unitario * item.cantidad
            total_carrito += subtotal
            tabla_carrito.add_row(
                str(item.producto_id),
                item.nombre,
                f"${item.precio_unitario:.2f}", #El :.2f es para formatear el número a 2 decimales y si hay más de 2 decimales, los redondea.
                str(item.cantidad),
                f"${subtotal:.2f}"
            )
        
        console.print(tabla_carrito)
        console.print(f"\n[bold green]Total del carrito: ${total_carrito:.2f}[/bold green]")

    def mostrar_usuarios(self, id_gerente: int) -> None:
        """
        Muestra todos los usuarios del sistema en forma de tabla. 
        Valida: el id del gerente y permiso de usuario (solo gerentes pueden ejecutarla).
        """
        
        console: Console = Console()
        usuarios: list[Usuario] = self.obtener_usuarios()
        self.validar_lista_usuarios_no_vacia(usuarios=usuarios)
        
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)
        
        table: Table = Table(title="Lista de Usuarios", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Nombre de Usuario", style="green", width=20)
        table.add_column("Rol", style="yellow", width=15)
        table.add_column("Items en Carrito", style="blue", width=15)
        
        for usuario in usuarios:
            cantidad_items: int = len(usuario.carrito.items)
            table.add_row(
                str(usuario.usuario_id),
                usuario.nombre_usuario,
                usuario.rol.value,
                str(cantidad_items)
            )
        
        console.print(table)

    def mostrar_productos(self, id_gerente: int) -> None:
        """
        Muestra todos los productos del inventario en forma de tabla. 
        Valida: el id del gerente y permiso de usuario (solo gerentes pueden ejecutarla).
        """
        
        console: Console = Console()
        
        gerente: Usuario = self.obtener_usuario_por_id(id_usuario=id_gerente)
        self.validar_usuario_gerente(usuario = gerente)
        
        productos: Producto = self.obtener_productos()
        self.validar_lista_productos_no_vacia(productos=productos)
        
        table: Table = Table(title="Inventario de Productos", show_header=True, header_style="pink1")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Nombre", style="green", width=25)
        table.add_column("Precio", style="yellow", width=12)
        table.add_column("Stock", style="blue", width=10)
        table.add_column("Valor Total", style="red", width=15)
        
        valor_total_inventario: float = 0
        for producto in productos:
            valor_producto: float = producto.precio * producto.stock
            valor_total_inventario += valor_producto
            
            table.add_row(
                str(producto.producto_id),
                producto.nombre,
                f"${producto.precio:.2f}",
                str(producto.stock),
                f"${valor_producto:.2f}"
            )
        
        console.print(table)
        console.print(f"\n[bold green]Valor Total del Inventario: ${valor_total_inventario:.2f}[/bold green]")

