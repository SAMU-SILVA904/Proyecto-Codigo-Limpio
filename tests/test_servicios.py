import pytest
from rich.console import Console
from unittest.mock import MagicMock
from src.gerencia_app.modelos import Usuario, Rol, Producto
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

def test_agregar_al_carrito_exitoso():
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    mock_almacenamiento_usuarios.save.assert_called_once()

def test_facturar_carrito_exitoso():
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    servicio.facturar_carrito(id_usuario=2)
    mock_almacenamiento_productos.save.assert_called()
    mock_almacenamiento_usuarios.save.assert_called()

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

def test_eliminar_producto_exitoso():
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    producto_a_eliminar = Producto(producto_id=1, nombre="Producto a eliminar", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto_a_eliminar]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.eliminar_producto(id_gerente=1, id_producto=1)
    mock_almacenamiento_productos.save.assert_called_once()

def test_eliminar_usuario_exitoso():
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    usuario_a_eliminar = Usuario(usuario_id=2, nombre_usuario="usuario_a_eliminar", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente, usuario_a_eliminar]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.eliminar_usuario(id_gerente=1, id_usuario=2)
    mock_almacenamiento_usuarios.save.assert_called_once()

def test_mostrar_carrito_exitoso():
    console: Console = Console()
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    servicio.mostrar_carrito(id_usuario=2)

def test_mostrar_usuarios_exitoso():
    console: Console = Console()
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente, empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.mostrar_usuarios(id_gerente=1)

def test_mostrar_productos_exitoso():
    console: Console = Console()
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(storage_usuarios=mock_almacenamiento_usuarios, storage_productos=mock_almacenamiento_productos)
    
    servicio.mostrar_productos(id_gerente=1)
