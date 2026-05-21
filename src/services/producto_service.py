"""
Servicio de negocio para la gestión de Productos.
Implementa el control de acceso: Solo el Gerente puede mutar el inventario.
"""

from src.almacenamiento.producto_repository import ProductoRepository
from src.almacenamiento.usuario_repository import UsuarioRepository
from src.core.excepciones import PermisoDenegadoError, StorageError


class ProductoService:
    """Capa de lógica de negocio para interactuar con el catálogo de productos."""

    def __init__(self) -> None:
        self.producto_repo = ProductoRepository()
        self.usuario_repo = UsuarioRepository()

    def _validar_permiso_gerente(self, usuario_id: int) -> None:
        """Helper privado que verifica si el usuario operativo es un Gerente."""
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise PermisoDenegadoError(f"El usuario con ID {usuario_id} no existe en el sistema.")
        
        # Regla de negocio: Rol ID 5 = Gerente, Rol ID 6 = Empleado
        if usuario.get("rol_id") != 5:
            raise PermisoDenegadoError("Acción no autorizada. Solo el personal de Gerencia puede modificar el inventario.")

    def obtener_catalogo(self) -> list[dict]:
        """Permite a cualquier usuario del sistema listar los productos disponibles."""
        return self.producto_repo.listar_todos()

    def obtener_producto(self, producto_id: int) -> dict:
        """Busca un producto por su identificador único."""
        producto = self.producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise StorageError(operation="obtener_producto", detail=f"El producto {producto_id} no existe.")
        return producto

    def crear_producto(self, usuario_id: int, datos_producto: dict) -> dict:
        """Valida permisos e inserta un nuevo producto en Supabase."""
        self._validar_permiso_gerente(usuario_id)
        return self.producto_repo.crear(datos_producto)

    def actualizar_producto(self, usuario_id: int, producto_id: int, datos_producto: dict) -> dict:
        """Valida permisos y actualiza las propiedades de un producto existente."""
        self._validar_permiso_gerente(usuario_id)
        # Verificamos existencia previa
        self.obtener_producto(producto_id)
        return self.producto_repo.actualizar(producto_id, datos_producto)

    def eliminar_producto(self, usuario_id: int, producto_id: int) -> bool:
        """Valida permisos y remueve físicamente el producto del inventario."""
        self._validar_permiso_gerente(usuario_id)
        self.obtener_producto(producto_id)
        return self.producto_repo.eliminar(producto_id)



