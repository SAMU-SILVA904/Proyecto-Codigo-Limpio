import pytest
from unittest.mock import MagicMock
from pathlib import Path
from src.gerencia_app.modelos import Usuario, Rol, Producto
from src.gerencia_app.almacenamiento import JSONStorage
from src.gerencia_app.servicios import TiendaServicios
from src.gerencia_app.exepciones import (
    CantidadInvalidaError,
    IdUsuarioInvalidoError,
    UsuarioNoEncontradoError,
    PermisoDenegadoError,
    UsuarioYaExisteError,
    NombreUsuarioInvalidoError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
    NombreProductoInvalidoError,
    IdProductoInvalidoError,
    CarritoVacioError,
    StockInsuficienteError
)

def test_crear_usuario_exitoso():
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol= Rol.GERENTE)
    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.crear_usuario(id_gerente=1, nombre_nuevo_usuario="nuevo_empleado", rol_nuevo_usuario= Rol.EMPLEADO)
    mock_almacenamiento_usuarios.save.assert_called_once()

def test_crear_producto_exitoso():
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.crear_producto(id_gerente=1, nombre_nuevo_producto="Producto de prueba", precio_nuevo_producto=10.0, stock_nuevo_producto=100)
    mock_almacenamiento_productos.save.assert_called_once()

