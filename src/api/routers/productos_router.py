"""Router de FastAPI para la gestión del catálogo de Productos."""

from fastapi import APIRouter, HTTPException, status
from src.services.producto_service import ProductoService
from src.Esquemas.producto import ProductoCreate, ProductoResponse
from src.core.excepciones import PermisoDenegadoError, StorageError

router = APIRouter(prefix="/productos", tags=["Productos"])
_service = ProductoService()


# ── [GET] Consultar Todo el Catálogo (Público) ────────────────────────────────
@router.get("/", response_model=list[ProductoResponse])
def listar_productos():
    """Retorna la lista completa de productos disponibles en el supermercado."""
    try:
        return _service.obtener_catalogo()
    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=exc.detail
        )


# ── [GET] Consultar Producto por ID ───────────────────────────────────────────
@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int):
    """Busca un producto específico mediante su producto_id."""
    try:
        return _service.obtener_producto(producto_id)
    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.detail
        )


# ── [POST] Crear un Nuevo Producto (Solo Gerente) ─────────────────────────────
@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(usuario_id: int, producto: ProductoCreate):
    """Permite registrar un producto en el inventario. Requiere ID de Gerente."""
    try:
        return _service.crear_producto(usuario_id, producto.model_dump())
    except PermisoDenegadoError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(exc)
        )
    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=exc.detail
        )


# ── [PATCH] Actualizar Producto Existente (Solo Gerente) ──────────────────────
@router.patch("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(usuario_id: int, producto_id: int, producto_data: dict):
    """Modifica de forma parcial o total las propiedades de un producto."""
    try:
        return _service.actualizar_producto(usuario_id, producto_id, producto_data)
    except PermisoDenegadoError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(exc)
        )
    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=exc.detail
        )


# ── [DELETE] Eliminar Producto (Solo Gerente) ─────────────────────────────────
@router.delete("/{producto_id}")
def eliminar_producto(usuario_id: int, producto_id: int):
    """Remueve físicamente un producto del inventario mediante su producto_id."""
    try:
        _service.eliminar_producto(usuario_id, producto_id)
        return {"status": "success", "message": f"Producto {producto_id} eliminado exitosamente."}
    except PermisoDenegadoError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail=str(exc)
        )
    except StorageError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=exc.detail
        )
