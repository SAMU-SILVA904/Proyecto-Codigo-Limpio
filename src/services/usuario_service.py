"""
Servicio de negocio para la gestión de Usuarios.
Asegura que el mantenimiento de cuentas sea potestad exclusiva de la Gerencia.
"""

from src.almacenamiento.usuario_repository import UsuarioRepository
from src.core.excepciones import PermisoDenegadoError, StorageError


class UsuarioService:
    """Capa de lógica de negocio para la administración de usuarios y roles."""

    def __init__(self) -> None:
        self.usuario_repo = UsuarioRepository()

    def _validar_permiso_gerente(self, usuario_id: int) -> None:
        """Verifica si el solicitante es administrador/gerente."""
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario or usuario.get("rol_id") != 5:  # Rol ID 5 = Gerente
            raise PermisoDenegadoError("Operación denegada. Se requieren privilegios de Gerente.")

    def obtener_todos_los_usuarios(self, solicitante_id: int) -> list[dict]:
        """Retorna la nómina completa de usuarios del supermercado."""
        self._validar_permiso_gerente(solicitante_id)
        return self.usuario_repo.listar_todos()

    def obtener_usuario_por_id(self, solicitante_id: int, usuario_id: int) -> dict:
        """Busca un usuario específico validando credenciales de auditoría."""
        self._validar_permiso_gerente(solicitante_id)
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise StorageError(operation="obtener_usuario", detail=f"El usuario {usuario_id} no fue encontrado.")
        return usuario

    def registrar_usuario(self, solicitante_id: int, datos_usuario: dict) -> dict:
        """Da de alta a un nuevo trabajador en la base de datos."""
        self._validar_permiso_gerente(solicitante_id)
        return self.usuario_repo.crear(datos_usuario)

    def actualizar_usuario(self, solicitante_id: int, usuario_id: int, datos_usuario: dict) -> dict:
        """Modifica los parámetros o el rol de un usuario."""
        self._validar_permiso_gerente(solicitante_id)
        self.obtener_usuario_por_id(solicitante_id, usuario_id)
        return self.usuario_repo.actualizar(usuario_id, datos_usuario)

    def eliminar_usuario(self, solicitante_id: int, usuario_id: int) -> bool:
        """Elimina la cuenta de un usuario del sistema."""
        self._validar_permiso_gerente(solicitante_id)
        self.obtener_usuario_por_id(solicitante_id, usuario_id)
        return self.usuario_repo.eliminar(usuario_id)









