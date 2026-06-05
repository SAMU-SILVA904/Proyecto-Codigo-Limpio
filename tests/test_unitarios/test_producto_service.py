import pytest
from unittest.mock import MagicMock, patch
from src.services.producto_service import ProductoService
from src.core.excepciones import PermisoDenegadoError

def test_crear_producto_exitoso():
    """Prueba que un Gerente (Rol 5) puede registrar un producto en el inventario."""
    
    # Parcheamos los dos repositorios que inicializa el constructor del servicio
    with patch("src.services.producto_service.ProductoRepository"), \
         patch("src.services.producto_service.UsuarioRepository"):
         
        # Creación de mocks limpios
        mock_prod = MagicMock()
        mock_user = MagicMock()
        
        # Simular que el usuario operativo es un Gerente (Rol 5)
        mock_user.obtener_por_id.return_value = {
            "usuario_id": 10,
            "nombre_usuario": "Joaquin Gerente",
            "rol_id": 5
        }
        
        # Simular la respuesta del repositorio al crear el producto
        producto_creado = {"id": 1, "nombre": "Leche Entera", "precio": 3500, "stock": 50}
        mock_prod.crear.return_value = producto_creado
        
        # Instanciar servicio e inyectar mocks manualmente en sus atributos reales
        service = ProductoService()
        service.producto_repo = mock_prod
        service.usuario_repo = mock_user
        
        # Ejecutar la acción (Act)
        resultado = service.crear_producto(
            usuario_id=10,
            datos_producto={"nombre": "Leche Entera", "precio": 3500, "stock": 50}
        )
        
        # Verificaciones (Assert)
        assert resultado["nombre"] == "Leche Entera"
        assert resultado["stock"] == 50
        mock_user.obtener_por_id.assert_called_once_with(10)
        mock_prod.crear.assert_called_once_with({"nombre": "Leche Entera", "precio": 3500, "stock": 50})


def test_eliminar_producto_permiso_denegado():
    """Prueba que un Empleado (Rol 6) no puede eliminar productos del supermercado."""
    
    with patch("src.services.producto_service.ProductoRepository"), \
         patch("src.services.producto_service.UsuarioRepository"):
        
        mock_prod = MagicMock()
        mock_user = MagicMock()
        
        # Simular que el usuario operativo es un Empleado (Rol 6)
        mock_user.obtener_por_id.return_value = {
            "usuario_id": 11,
            "nombre_usuario": "Andres Empleado",
            "rol_id": 6
        }
        
        service = ProductoService()
        service.producto_repo = mock_prod
        service.usuario_repo = mock_user
        
        # Evaluar que se dispare la excepción de seguridad de dominio
        with pytest.raises(PermisoDenegadoError):
            service.eliminar_producto(usuario_id=11, producto_id=1)
            
        # Bloqueo de seguridad: Validar que jamás se haya llamado al método de la base de datos
        mock_prod.eliminar.assert_not_called()