import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_supabase_client():
    """Fixture que simula el comportamiento del cliente de Supabase."""
    mock_client = MagicMock()
    # Simulamos el encadenamiento de métodos comunes: client.table().update().eq()
    mock_client.table.return_value = mock_client
    mock_client.update.return_value = mock_client
    mock_client.select.return_value = mock_client
    mock_client.eq.return_value = mock_client
    return mock_client

@pytest.fixture
def mock_usuario_repo(mock_supabase_client):
    """Fixture para el repositorio de usuarios con el cliente mockeado."""
    # Importamos acá para evitar problemas de paths al iniciar pytest
    from src.almacenamiento.usuario_repository import UsuarioRepository
    
    repo = UsuarioRepository()
    repo.client = mock_supabase_client  # Reemplazamos el cliente real por el mock
    return repo
