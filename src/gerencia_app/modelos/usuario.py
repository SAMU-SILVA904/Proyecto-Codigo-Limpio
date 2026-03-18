from dataclasses import dataclass, field
from .rol import Rol
from .carrito import Carrito
from src.gerencia_app.exepciones import (
    IdUsuarioInvalidoError,
    PermisoDenegadoError,
    NombreUsuarioInvalidoError,
)

@dataclass
class Usuario:
    """
    Modelo para representar un usuario de la tienda, con su rol y carrito de compras.
    """
    
    usuario_id: int
    nombre_usuario: str
    rol: Rol
    carrito: Carrito = field(default_factory=Carrito)

    def __post_init__(self):
        """
        Validación de atributos.
        """
        if self.usuario_id <= 0:
            raise IdUsuarioInvalidoError(self.usuario_id)
        if not self.nombre_usuario.strip():
            raise NombreUsuarioInvalidoError(self.nombre_usuario)
        if self.rol not in [Rol.GERENTE, Rol.EMPLEADO]:
            raise PermisoDenegadoError("El rol especificado no es válido. Debe ser 'gerente' o 'empleado'.")