"""Repositorio de almacenamiento para la entidad Usuario."""

from src.almacenamiento.base import BaseRepository


class UsuarioRepository(BaseRepository):
    """Manejo directo de la tabla 'usuario' en Supabase."""

    def __init__(self) -> None:
        super().__init__()
        self._table = "usuario"

    def listar_todos(self) -> list[dict]:
        """Retorna la lista completa de usuarios registrados."""
        op = "listar_todos_los_usuarios"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).select("*").execute()
        )
        return self._require_data(response, op)

    def obtener_por_id(self, usuario_id: int) -> dict | None:
        """Busca un usuario específico mediante su usuario_id."""
        op = f"obtener_usuario_por_id_{usuario_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).select("*").eq("usuario_id", usuario_id).execute()
        )
        data = getattr(response, "data", [])
        return data[0] if data else None

    def crear(self, datos_usuario: dict) -> dict:
        """Inserta un nuevo usuario en el sistema."""
        op = "crear_usuario"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).insert(datos_usuario).execute()
        )
        return self._require_data(response, op)[0]

    def actualizar(self, usuario_id: int, datos_usuario: dict) -> dict:
        """Modifica los parámetros de un usuario existente."""
        op = f"actualizar_usuario_{usuario_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).update(datos_usuario).eq("usuario_id", usuario_id).execute()
        )
        return self._require_data(response, op)[0]

    def eliminar(self, usuario_id: int) -> bool:
        """Elimina físicamente un registro de usuario."""
        op = f"eliminar_usuario_{usuario_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).delete().eq("usuario_id", usuario_id).execute()
        )
        data = getattr(response, "data", [])
        return len(data) > 0