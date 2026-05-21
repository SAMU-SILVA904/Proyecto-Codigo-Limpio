"""Repositorio de almacenamiento para la entidad Producto."""

from src.almacenamiento.base import BaseRepository


class ProductoRepository(BaseRepository):
    """Manejo directo de la tabla 'producto' en Supabase."""

    def __init__(self) -> None:
        super().__init__()
        self._table = "producto"

    def listar_todos(self) -> list[dict]:
        """Retorna todo el catálogo de productos disponibles."""
        op = "listar_todos_los_productos"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).select("*").execute()
        )
        return self._require_data(response, op)

    def obtener_por_id(self, producto_id: int) -> dict | None:
        """Busca una mercancía mediante su producto_id."""
        op = f"obtener_producto_por_id_{producto_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).select("*").eq("producto_id", producto_id).execute()
        )
        data = getattr(response, "data", [])
        return data[0] if data else None

    def crear(self, datos_producto: dict) -> dict:
        """Registra un nuevo producto en el inventario."""
        op = "crear_producto"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).insert(datos_producto).execute()
        )
        return self._require_data(response, op)[0]

    def actualizar(self, producto_id: int, datos_producto: dict) -> dict:
        """Actualiza el precio, stock o nombre de un artículo."""
        op = f"actualizar_producto_{producto_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).update(datos_producto).eq("producto_id", producto_id).execute()
        )
        return self._require_data(response, op)[0]

    def eliminar(self, producto_id: int) -> bool:
        """Remueve de forma permanente un producto del catálogo."""
        op = f"eliminar_producto_{producto_id}"
        response = self._execute(
            op,
            lambda: self.client.table(self._table).delete().eq("producto_id", producto_id).execute()
        )
        data = getattr(response, "data", [])
        return len(data) > 0