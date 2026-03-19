class TiendaError(Exception):
    """Base para todas las excepciones del proyecto"""

    pass


class CantidadInvalidaError(TiendaError):
    def __init__(self, cantidad: float | int) -> None:
        self.cantidad = cantidad
        super().__init__(
            f"La cantidad '{cantidad}' es inválida. Debe ser un número positivo."
        )


class UsuarioError(TiendaError):
    """Base para todas las excepciones relacionadas con usuarios"""

    pass


class IdUsuarioInvalidoError(UsuarioError):
    def __init__(self, id_usuario: int) -> None:
        self.id_usuario = id_usuario
        super().__init__(
            f"El ID de usuario '{id_usuario}' es inválido. Debe ser un número entero positivo."
        )


class UsuarioNoEncontradoError(UsuarioError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"Usuario con el id: '{user_id}' no encontrado")


class PermisoDenegadoError(UsuarioError):
    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)


class UsuarioYaExisteError(UsuarioError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"Usuario con el id: '{user_id}' ya existe")


class NombreUsuarioInvalidoError(UsuarioError):
    def __init__(self, nombre_usuario: str) -> None:
        self.nombre_usuario = nombre_usuario
        super().__init__(
            f"El nombre de usuario '{nombre_usuario}' es inválido. No puede estar vacío o contener solo espacios."
        )


class ProductoError(TiendaError):
    """Base para todas las excepciones relacionadas con productos"""

    pass


class ProductoNoEncontradoError(ProductoError):
    def __init__(self, producto_id: int) -> None:
        self.producto_id = producto_id
        super().__init__(f"Producto con id '{producto_id}' no encontrado")


class ProductoYaExisteError(ProductoError):
    def __init__(self, producto_id: int) -> None:
        self.producto_id = producto_id
        super().__init__(f"Producto con id '{producto_id}' ya existe")


class NombreProductoInvalidoError(ProductoError):
    def __init__(self, nombre_producto: str) -> None:
        self.nombre_producto = nombre_producto
        super().__init__(
            f"El nombre del producto '{nombre_producto}' es inválido. No puede estar vacío o contener solo espacios."
        )


class IdProductoInvalidoError(ProductoError):
    def __init__(self, id_producto: int) -> None:
        self.id_producto = id_producto
        super().__init__(
            f"El ID de producto '{id_producto}' es inválido. Debe ser un número entero positivo."
        )


class CarritoError(TiendaError):
    """Base para todas las excepciones relacionadas con el carrito de compras"""

    pass


class CarritoVacioError(CarritoError):
    def __init__(self) -> None:
        super().__init__("El carrito está vacío, agrega productos antes de prodceder con el comando")


class StockInsuficienteError(CarritoError):
    def __init__(self, producto_id: int, stock_disponible: int) -> None:
        self.producto_id = producto_id
        self.stock_disponible = stock_disponible
        super().__init__(
            f"Stock insuficiente para el producto con id '{producto_id}'. Stock disponible: {stock_disponible}"
        )
