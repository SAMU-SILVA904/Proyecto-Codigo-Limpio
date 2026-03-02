class TiendaError(Exception):
    """Base para todas las excepciones del proyecto"""
    pass

class CarritoVacioError(TiendaError):
    def __init__(self) -> None:
        super().__init__("El carrito está vacío, no se puede facturar")

class StockInsuficienteError(TiendaError):
    pass

class PermisoDenegadoError(TiendaError):
    def __init__(self, mensaje: str) -> None:
        self.mensaje = mensaje
        super().__init__(mensaje)

class UsuarioNoEncontradoError(TiendaError):
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        super().__init__(f"Usuario con el id: '{user_id}' no encontrado")
        
class ProductoNoEncontradoError(TiendaError):
    def __init__(self, producto_id: int) -> None:
        self.producto_id = producto_id
        super().__init__(f"Producto con id '{producto_id}' no encontrado")