import pytest
from unittest.mock import MagicMock, patch
from src.services.usuario_service import UsuarioService
from src.core.excepciones import PermisoDenegadoError

def test_actualizar_usuario_exitoso():
    """Prueba que un Gerente (Rol 5) puede actualizar los datos de un usuario."""
    
    with patch("src.services.usuario_service.UsuarioRepository"):
        mock_repo = MagicMock()
        
        # 1. Simular la obtención del solicitante (Gerente)
        mock_repo.obtener_por_id.return_value = {
            "usuario_id": 31,
            "nombre_usuario": "Carlos Gerente",
            "rol_id": 5
        }
        
        # 2. CORREGIDO: Cambiamos 'actualizar_usuario' por 'actualizar' para tu repositorio
        datos_retorno = {"usuario_id": 40, "nombre_usuario": "Dani", "rol_id": 5}
        mock_repo.actualizar.return_value = datos_retorno
        
        service = UsuarioService()
        service.usuario_repo = mock_repo
        
        # Act
        resultado = service.actualizar_usuario(
            solicitante_id=31,
            usuario_id=40,
            datos_usuario={"nombre_usuario": "Dani", "rol_id": 5}
        )
        
        # Assert
        assert resultado["nombre_usuario"] == "Dani"
        assert resultado["rol_id"] == 5


def test_actualizar_usuario_permiso_denegado():
    """Prueba que un Empleado común (Rol 6) no tiene permisos y lanza la excepción."""
    
    with patch("src.services.usuario_service.UsuarioRepository"):
        mock_repo = MagicMock()
        
        mock_repo.obtener_por_id.return_value = {
            "usuario_id": 42,
            "nombre_usuario": "Juan Empleado",
            "rol_id": 6
        }
        
        service = UsuarioService()
        service.usuario_repo = mock_repo
        
        with pytest.raises(PermisoDenegadoError):
            service.actualizar_usuario(
                solicitante_id=42,
                usuario_id=40,
                datos_usuario={"nombre_usuario": "Dani Hack"}
            )