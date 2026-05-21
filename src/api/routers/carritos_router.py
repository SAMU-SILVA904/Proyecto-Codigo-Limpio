"""Router de FastAPI para la gestión de Carritos de Compras."""

from fastapi import APIRouter, HTTPException, status
from src.services.carrito_service import CarritoService
from src.Esquemas.carrito import CarritoResponse
from src.core.excepciones import PermisoDenegadoError, StorageError

router = APIRouter(prefix="/carritos", tags=["Carritos"])
_service = CarritoService()


# ── [GET] Consultar Carrito de un Usuario ─────────────────────────────────────
@router.get("/{usuario_id}", response_model=CarritoResponse)
def obtener_carrito(usuario_id: int):
    """Obtiene el contenido relacional del carrito único de un empleado.
    
    Lanza un error 403 controlado si el usuario consultado posee rol de Gerente (Rol 5).
    """
    try:
        return _service.obtener_o_inicializar_carrito(usuario_id)
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


# ── [POST] Añadir / Sumar Ítem al Carrito ──────────────────────────────────────
@router.post("/{usuario_id}/agregar")
def agregar_item(usuario_id: int, producto_id: int, cantidad: int = 1):
    """Añade o incrementa las unidades de un producto específico en el carrito."""
    try:
        data = _service.agregar_producto_a_carrito(usuario_id, producto_id, cantidad)
        return {"status": "success", "message": "Producto gestionado en el carrito", "data": data}
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


# ── [DELETE] Remover Producto Completo del Carrito ────────────────────────────
@router.delete("/{usuario_id}/remover/{producto_id}")
def remover_item(usuario_id: int, producto_id: int):
    """Elimina físicamente un producto (toda su cantidad) del carrito personal."""
    try:
        _service.eliminar_producto_de_carrito(usuario_id, producto_id)
        return {"status": "success", "message": f"Producto {producto_id} removido del carrito."}
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