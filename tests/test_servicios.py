import pytest
from unittest.mock import MagicMock

from gerencia_app.modelos.rol import Usuario, Rol, Producto
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


# Pruebas de casos exitosos


def test_agregar_al_carrito_exitoso():
    """
    Prueba que un empleado pueda agregar un producto al carrito correctamente.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    mock_almacenamiento_usuarios.save.assert_called_once()

def test_facturar_carrito_exitoso():
    """
    Prueba que un empleado pueda facturar su carrito correctamente, actualizando el stock del producto y vaciando el carrito.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    servicio.facturar_carrito(id_usuario=2)
    mock_almacenamiento_productos.save.assert_called()
    mock_almacenamiento_usuarios.save.assert_called()

def test_quitar_producto_del_carrito_exitoso():
    """
    Prueba que un empleado pueda quitar un producto de su carrito correctamente, actualizando el carrito y el stock del producto.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    servicio.quitar_producto_del_carrito(id_usuario=2, id_producto=1)
    mock_almacenamiento_usuarios.save.assert_called()

def test_agregar_stock_exitoso():
    """
    Prueba que un gerente pueda agregar stock a un producto correctamente, actualizando el stock del producto en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.agregar_stock_producto(id_gerente=1, id_producto=1, cantidad_a_agregar=50)
    mock_almacenamiento_productos.save.assert_called_once()

def test_crear_producto_exitoso():
    """
    Prueba que un gerente pueda crear un nuevo producto correctamente, y que el producto se guarde en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.crear_producto(id_gerente=1, nombre_nuevo_producto="Producto de prueba", precio_nuevo_producto=10.0, stock_nuevo_producto=100)
    mock_almacenamiento_productos.save.assert_called_once()

def test_crear_usuario_exitoso():
    """
    Prueba que un gerente pueda crear un nuevo usuario correctamente, y que el usuario se guarde en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol= Rol.GERENTE)
    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.crear_usuario(id_gerente=1, nombre_nuevo_usuario="nuevo_empleado", rol_nuevo_usuario= Rol.EMPLEADO)
    mock_almacenamiento_usuarios.save.assert_called_once()

def test_eliminar_producto_exitoso():
    """
    Prueba que un gerente pueda eliminar un producto correctamente, y que el producto se elimine del almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    producto_a_eliminar = Producto(producto_id=1, nombre="Producto a eliminar", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto_a_eliminar]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.eliminar_producto(id_gerente=1, id_producto=1)
    mock_almacenamiento_productos.save.assert_called_once()

def test_eliminar_usuario_exitoso():
    """
    Prueba que un gerente pueda eliminar un usuario correctamente, y que el usuario se elimine del almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    usuario_a_eliminar = Usuario(usuario_id=2, nombre_usuario="usuario_a_eliminar", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente, usuario_a_eliminar]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.eliminar_usuario(id_gerente=1, id_usuario=2)
    mock_almacenamiento_usuarios.save.assert_called_once()

def test_mostrar_carrito_exitoso():
    """
    Prueba que un empleado pueda mostrar su carrito correctamente.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    servicio.mostrar_carrito(id_usuario=2)

def test_mostrar_usuarios_exitoso():
    """
    Prueba que un gerente pueda mostrar la lista de usuarios correctamente.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente, empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.mostrar_usuarios(id_gerente=1)

def test_mostrar_productos_exitoso():
    """
    Prueba que un gerente pueda mostrar la lista de productos correctamente.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    servicio.mostrar_productos(id_gerente=1)


# Pruebas de validación de errores


def test_cantidad_invalida():
    """
    Prueba que agregar una cantidad negativa de un producto al carrito lance una excepción de CantidadInvalidaError, y que no se guarden cambios en el almacenamiento.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(CantidadInvalidaError):
        servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=-5)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_idUsuario_invalido():
    """
    Prueba que agregar un producto al carrito con un ID de usuario negativo lance una excepción de IdUsuarioInvalidoError, y que no se guarden cambios en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(IdUsuarioInvalidoError):
        servicio.agregar_al_carrito(id_usuario=-1, id_producto=1, cantidad=1)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_usuario_no_encontrado():
    """
    Prueba que mostrar el carrito de un usuario que no existe lance una excepción de UsuarioNoEncontradoError, y que no se guarden cambios en el almacenamiento.
    """
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(UsuarioNoEncontradoError):
        servicio.mostrar_carrito(id_usuario=999)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_permiso_denegado():
    """
    Prueba que un empleado intente crear un nuevo usuario y lance una excepción de PermisoDenegadoError, y que no se guarden cambios en el almacenamiento.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(PermisoDenegadoError):
        servicio.crear_usuario(id_gerente=2, nombre_nuevo_usuario="nuevo_empleado", rol_nuevo_usuario=Rol.GERENTE)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_usuario_ya_existe():
    """
    Prueba que un gerente intente crear un nuevo usuario con un nombre de usuario que ya existe y lance una excepción de UsuarioYaExisteError, y que no se guarden cambios en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    empleado_existente = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente, empleado_existente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(UsuarioYaExisteError):
        servicio.crear_usuario(id_gerente=1, nombre_nuevo_usuario="empleado_unico", rol_nuevo_usuario=Rol.EMPLEADO)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_nombre_usuario_invalido():
    """
    Prueba que un gerente intente crear un nuevo usuario con un nombre de usuario vacío o solo espacios y lance una excepción de NombreUsuarioInvalidoError, y que no se guarden cambios en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(NombreUsuarioInvalidoError):
        servicio.crear_usuario(id_gerente=1, nombre_nuevo_usuario="   ", rol_nuevo_usuario=Rol.EMPLEADO)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_producto_no_encontrado():
    """
    Prueba que agregar un producto al carrito con un ID de producto que no existe lance una excepción de ProductoNoEncontradoError, y que no se guarden cambios en el almacenamiento.
    """
    
    empleado = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(ProductoNoEncontradoError):
        servicio.agregar_al_carrito(id_usuario=1, id_producto=999, cantidad=1)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_producto_ya_existe():
    """
    Prueba que un gerente intente crear un nuevo producto con un nombre de producto que ya existe, lance una excepción de ProductoYaExisteError, y que no se guarden cambios en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)
    producto_existente = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=100)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto_existente]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(ProductoYaExisteError):
        servicio.crear_producto(id_gerente=1, nombre_nuevo_producto="Producto de prueba", precio_nuevo_producto=10.0, stock_nuevo_producto=100)
    mock_almacenamiento_productos.save.assert_not_called()

def test_nombre_producto_invalido():
    """
    Prueba que un gerente intente crear un nuevo producto con un nombre de producto vacío o solo espacios y lance una excepción de NombreProductoInvalidoError, y que no se guarden cambios en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(NombreProductoInvalidoError):
        servicio.crear_producto(id_gerente=1, nombre_nuevo_producto="   ", precio_nuevo_producto=10.0, stock_nuevo_producto=100)
    mock_almacenamiento_productos.save.assert_not_called()

def test_id_producto_invalido():
    """
    Prueba que agregar un producto al carrito con un ID de producto negativo lance una excepción de IdProductoInvalidoError, y que no se guarden cambios en el almacenamiento.
    """
    
    gerente = Usuario(usuario_id=1, nombre_usuario="gerente_unico", rol=Rol.GERENTE)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [gerente]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(IdProductoInvalidoError):
        servicio.agregar_al_carrito(id_usuario=1, id_producto=-1, cantidad=1)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_carrito_vacio():
    """
    Prueba que facturar el carrito de un usuario que no tiene productos en el carrito lance una excepción de CarritoVacioError, y que no se guarden cambios en el almacenamiento.
    """
    
    empleado = Usuario(usuario_id=1, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = []
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(CarritoVacioError):
        servicio.facturar_carrito(id_usuario=1)
    mock_almacenamiento_usuarios.save.assert_not_called()

def test_agregar_al_carrito_stock_insuficiente():
    """
    Prueba que agregar una cantidad de un producto al carrito que exceda el stock disponible lance una excepción de StockInsuficienteError, y que no se guarden cambios en el almacenamiento.
    """
    
    empleado = Usuario(usuario_id=2, nombre_usuario="empleado_unico", rol=Rol.EMPLEADO)
    producto = Producto(producto_id=1, nombre="Producto de prueba", precio=10.0, stock=3)

    mock_almacenamiento_usuarios = MagicMock()
    mock_almacenamiento_usuarios.load.return_value = [empleado]
    mock_almacenamiento_usuarios.save = MagicMock()

    mock_almacenamiento_productos = MagicMock()
    mock_almacenamiento_productos.load.return_value = [producto]
    mock_almacenamiento_productos.save = MagicMock()

    servicio = TiendaServicios(almacenamiento_usuarios=mock_almacenamiento_usuarios, almacenamiento_productos=mock_almacenamiento_productos)
    
    with pytest.raises(StockInsuficienteError):
        servicio.agregar_al_carrito(id_usuario=2, id_producto=1, cantidad=5)
    mock_almacenamiento_usuarios.save.assert_not_called()

