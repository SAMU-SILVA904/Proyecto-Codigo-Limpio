"""
Servicio de negocio para la gestión del Carrito de Compras.
Aplica las reglas de negocio de negocio: Bloqueo de Gerentes y persistencia de ítems.
"""

from src.almacenamiento.carrito_repository import CarritoRepository
from src.almacenamiento.usuario_repository import UsuarioRepository
from src.almacenamiento.producto_repository import ProductoRepository
from src.core.excepciones import PermisoDenegadoError, StorageError


class CarritoService:
    """Capa de lógica de negocio para gestionar los carritos personales de empleados."""

    def __init__(self) -> None:
        self.carrito_repo = CarritoRepository()
        self.usuario_repo = UsuarioRepository()
        self.producto_repo = ProductoRepository()

    def _verificar_usuario_es_empleado(self, usuario_id: int) -> None:
        """Garantiza que el usuario existe y que NO es un gerente."""
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise PermisoDenegadoError(f"El usuario con ID {usuario_id} no existe en el sistema.")
        
        if usuario.get("rol_id") == 5:  # Rol ID 5 = Gerente
            raise PermisoDenegadoError("El usuario no contiene carrito por ser gerente.")

    def obtener_o_inicializar_carrito(self, usuario_id: int) -> dict:
        """Retorna el carrito relacional del empleado. Si no tiene uno, lo crea."""
        self._verificar_usuario_es_empleado(usuario_id)
        
        carrito = self.carrito_repo.obtener_carrito_con_items(usuario_id)
        
        if not carrito:
            self.carrito_repo.crear_carrito_vacio(usuario_id)
            carrito = self.carrito_repo.obtener_carrito_con_items(usuario_id)
            
        return carrito

    def agregar_producto_a_carrito(self, usuario_id: int, producto_id: int, cantidad: int) -> dict:
        """Agrega una cantidad determinada de un producto al carrito personal."""
        if cantidad <= 0:
            raise StorageError(operation="agregar_item", detail="La cantidad a agregar debe ser mayor a cero.")
            
        self._verificar_usuario_es_empleado(usuario_id)
        
        producto = self.producto_repo.obtener_por_id(producto_id)
        if not producto:
            raise StorageError(operation="agregar_item", detail=f"El producto con ID {producto_id} no existe.")
            
        carrito_base = self.obtener_o_inicializar_carrito(usuario_id)
        carrito_id = carrito_base["id"]
        
        return self.carrito_repo.agregar_o_actualizar_item(carrito_id, producto_id, cantidad)

    def eliminar_producto_de_carrito(self, usuario_id: int, producto_id: int) -> bool:
        """Remueve por completo un producto del carrito del empleado (Operación DELETE)."""
        self._verificar_usuario_es_empleado(usuario_id)
        
        carrito_base = self.obtener_o_inicializar_carrito(usuario_id)
        carrito_id = carrito_base["id"]
        
        exito = self.carrito_repo.eliminar_item_directo(carrito_id, producto_id)
        if not exito:
            raise StorageError(operation="eliminar_item", detail="El producto no se encontraba en el carrito.")
        return exito





