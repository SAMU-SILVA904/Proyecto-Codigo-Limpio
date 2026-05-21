"""Router de FastAPI para la gestión y administración de Usuarios."""

from fastapi import APIRouter, HTTPException, status
from src.services.usuario_service import UsuarioService
from src.Esquemas.usuario import UsuarioCreate, UsuarioResponse
from src.core.excepciones import PermisoDenegadoError, StorageError

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])
_service = UsuarioService()


# ── [GET] Listar todos los usuarios (Solo Gerente) ───────────────────────────
@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(solicitante_id: int):
    """Retorna la lista completa de usuarios del supermercado. Requiere ID de Gerente."""
    try:
        return _service.obtener_todos_los_usuarios(solicitante_id)
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


# ── [POST] Crear un nuevo usuario (Solo Gerente) ──────────────────────────────
@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(solicitante_id: int, usuario: UsuarioCreate):
    """Registra un nuevo empleado o gerente en el sistema. Requiere ID de Gerente."""
    try:
        return _service.registrar_usuario(solicitante_id, usuario.model_dump())
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

# ── [PATCH] Actualizar usuario existente (Solo Gerente) ───────────────────────
@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(solicitante_id: int, usuario_id: int, usuario_data: dict):
    """Modifica de forma parcial o total las propiedades de una cuenta de usuario."""
    try:
        return _service.actualizar_usuario(solicitante_id, usuario_id, usuario_data)
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

# ── [DELETE] Eliminar usuario (Solo Gerente) ──────────────────────────────────
@router.delete("/{usuario_id}")
def eliminar_usuario(solicitante_id: int, usuario_id: int):
    """Elimina físicamente una cuenta de usuario usando el método corregido."""
    try:
        _service.eliminar_usuario(solicitante_id, usuario_id)
        return {"status": "success", "message": f"Usuario {usuario_id} eliminado correctamente."}
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
