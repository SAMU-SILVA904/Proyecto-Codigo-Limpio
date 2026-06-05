import pytest
from unittest.mock import MagicMock, patch
from src.services.carrito_service import CarritoService
from src.core.excepciones import PermisoDenegadoError

def test_obtener_carrito_empleado_exitoso():
    """Prueba que un Empleado (Rol 6) puede obtener su carrito correctamente."""
    
    # Parcheamos los tres repositorios que usa el constructor de CarritoService
    with patch("src.services.carrito_service.CarritoRepository"), \
         patch("src.services.carrito_service.UsuarioRepository"), \
         patch("src.services.carrito_service.ProductoRepository"):
         
        # Instanciamos los mocks individuales
        mock_carrito = MagicMock()
        mock_usuario = MagicMock()
        mock_producto = MagicMock()
        
        # 1. Configuramos el mock de usuarios para simular un Empleado (Rol 6)
        mock_usuario.obtener_por_id.return_value = {
            "usuario_id": 42,
            "nombre_usuario": "Juan Empleado",
            "rol_id": 6
        }
        
        # 2. Configuramos el mock de carrito para retornar un carrito simulado existente
        carrito_esperado = {
            "carrito_id": 100,
            "usuario_id": 42,
            "items": [{"producto_id": 1, "cantidad": 3}]
        }
        mock_carrito.obtener_carrito_con_items.return_value = carrito_esperado
        
        # Instanciamos el servicio e inyectamos los mocks en sus respectivos atributos
        service = CarritoService()
        service.carrito_repo = mock_carrito
        service.usuario_repo = mock_usuario
        service.producto_repo = mock_producto
        
        # Act: Ejecutamos la acción
        resultado = service.obtener_o_inicializar_carrito(usuario_id=42)
        
        # Assert: Verificamos que todo se haya llamado y devuelto como corresponde
        assert resultado["carrito_id"] == 100
        assert len(resultado["items"]) == 1
        mock_usuario.obtener_por_id.assert_called_once_with(42)
        mock_carrito.obtener_carrito_con_items.assert_called_once_with(42)


def test_obtener_carrito_gerente_bloqueado():
    """Prueba que un Gerente (Rol 5) tiene bloqueado el uso de carritos."""
    
    with patch("src.services.carrito_service.CarritoRepository"), \
         patch("src.services.carrito_service.UsuarioRepository"), \
         patch("src.services.carrito_service.ProductoRepository"):
         
        mock_carrito = MagicMock()
        mock_usuario = MagicMock()
        mock_producto = MagicMock()
        
        # Configuramos el mock para simular un Gerente (Rol 5)
        mock_usuario.obtener_por_id.return_value = {
            "usuario_id": 31,
            "nombre_usuario": "Carlos Gerente",
            "rol_id": 5
        }
        
        service = CarritoService()
        service.carrito_repo = mock_carrito
        service.usuario_repo = mock_usuario
        service.producto_repo = mock_producto
        
        # Act & Assert: Validamos que lance la excepción de negocio esperada
        with pytest.raises(PermisoDenegadoError) as exc_info:
            service.obtener_o_inicializar_carrito(usuario_id=31)
            
        # Opcional: Validamos que el mensaje de error sea el correcto
        assert "El usuario no contiene carrito por ser gerente." in str(exc_info.value)
        
        # Verificamos que por seguridad jamás se haya consultado a la tabla de carritos
        mock_carrito.obtener_carrito_con_items.assert_not_called()