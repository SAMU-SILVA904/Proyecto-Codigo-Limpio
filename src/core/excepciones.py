"""
Definición de excepciones de negocio del sistema.
"""

class StorageError(Exception):
    """Error general al conectar con la base de datos Supabase."""
    def __init__(self, message: str = "Error de comunicación con el almacenamiento"):
        self.message = message
        super().__init__(self.message)

class PermisoDenegadoError(Exception):
    """Error cuando un usuario con rol Gerente intenta modificar el carrito."""
    def __init__(self, message: str = "Acceso denegado: El rol 'gerente' no puede realizar operaciones de compra"):
        self.message = message
        super().__init__(self.message)

class ProductoNoEncontradoError(Exception):
    def __init__(self, producto_id: int):
        self.message = f"El producto con ID {producto_id} no existe en el catálogo de Supabase"
        super().__init__(self.message)

class UsuarioNoEncontradoError(Exception):
    def __init__(self, usuario_id: int):
        self.message = f"El usuario con ID {usuario_id} no se encuentra registrado en el sistema"
        super().__init__(self.message)

class CantidadInvalidaError(Exception):
    def __init__(self, message: str = "La cantidad ingresada debe ser mayor a cero"):
        self.message = message
        super().__init__(self.message)
        
        
        
