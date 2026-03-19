import typer
from pathlib import Path
from rich.console import Console

from src.gerencia_app.modelos.usuario import Usuario
from src.gerencia_app.modelos.rol import Rol
from src.gerencia_app.modelos.producto import Producto
from src.gerencia_app.servicios import TiendaServicios
from src.gerencia_app.almacenamiento import JSONStorage

from src.gerencia_app.exepciones import TiendaError

app = typer.Typer()
console = Console()


@app.callback(invoke_without_command=True)# Este callback se ejecuta cada vez que se llama a la aplicación, incluso si no se especifica un comando. Es útil para inicializar recursos compartidos como el almacenamiento y los servicios.
def main_callback():
    console.print("\n[bold green]Bienvenido a la tienda[/bold green]\n")
    console.print("Cargando datos...")

    global almacenamiento_usuarios, almacenamiento_productos, servicios
    almacenamiento_usuarios = JSONStorage(base_a_guardar=Path("data/database_usuarios.json"), modelo_clase=Usuario)
    almacenamiento_productos = JSONStorage(base_a_guardar=Path("data/database_productos.json"), modelo_clase=Producto)

    usuarios = almacenamiento_usuarios.load()
    productos = almacenamiento_productos.load()

    console.print("\n[bold blue]Datos cargados exitosamente[/bold blue]\n")
    console.print(f"Usuarios: {len(usuarios)}")
    console.print(f"Productos: {len(productos)}")

    servicios = TiendaServicios(almacenamiento_usuarios=almacenamiento_usuarios, almacenamiento_productos=almacenamiento_productos)


@app.command()
def mostrar_carrito(id_usuario: int):
    """
    Comando para mostrar el carrito de un usuario específico.
    """
    try:
        servicios.mostrar_carrito(id_usuario=id_usuario)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def mostrar_usuarios(id_usuario: int):
    """
    Comando para mostrar el listado de usuarios.
    """
    try:
        servicios.mostrar_usuarios(id_gerente=id_usuario)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def mostrar_productos(id_usuario: int):
    """
    Comando para mostrar el listado de productos en el inventario.
    """
    try:
        servicios.mostrar_productos(id_gerente=id_usuario)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def agregar_al_carrito(id_usuario: int, id_producto: int, cantidad: int):
    """
    Comando para agregar un producto al carrito de un usuario.
    """
    try:
        console.print(f"Agregando producto {id_producto} al carrito del usuario {id_usuario} con cantidad {cantidad}...")
        servicios.agregar_al_carrito(id_usuario=id_usuario, id_producto=id_producto, cantidad=cantidad)
        console.print("[bold green]Producto agregado al carrito exitosamente[/bold green]")
        servicios.mostrar_carrito(id_usuario=id_usuario)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def facturar_carrito(id_usuario: int):
    """
    Comando para facturar el carrito de un usuario, mostrando el total a pagar y vaciando el carrito.
    """
    try:
        servicios.facturar_carrito(id_usuario=id_usuario)
        console.print("[bold green]Carrito facturado exitosamente[/bold green]")
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def quitar_producto_del_carrito(id_usuario: int, id_producto: int):
    """
    Comando para quitar un producto del carrito de un usuario.
    """
    try:
        servicios.quitar_producto_del_carrito(id_usuario=id_usuario, id_producto=id_producto)
        console.print("[bold green]Producto quitado del carrito exitosamente[/bold green]")
        servicios.mostrar_carrito(id_usuario=id_usuario)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def agregar_stock(id_gerente: int, id_producto: int, cantidad: int):
    """
    Comando para que un gerente agregue stock a un producto existente en el inventario.
    """
    try:
        servicios.agregar_stock_producto(id_gerente=id_gerente, id_producto=id_producto, cantidad_a_agregar=cantidad)
        console.print("[bold green]Stock agregado exitosamente[/bold green]")
        servicios.mostrar_productos(id_gerente=id_gerente)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def crear_producto(id_gerente: int, nombre_producto: str, precio_producto: float, stock_producto: int):
    """
    Comando para que un gerente cree un nuevo producto en el inventario.
    """
    try:
        servicios.crear_producto(id_gerente=id_gerente, nombre_nuevo_producto=nombre_producto, precio_nuevo_producto=precio_producto, stock_nuevo_producto=stock_producto)
        console.print("[bold green]Producto creado exitosamente[/bold green]")
        servicios.mostrar_productos(id_gerente=id_gerente)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def crear_usuario(id_gerente: int, nombre_usuario: str, rol_usuario: str):
    """
    Comando para que un gerente cree un nuevo usuario en el sistema.
    """
    try:
        rol_usuario = Rol(rol_usuario) # Convertir el string ingresado a un valor del enum Rol.
        servicios.crear_usuario(id_gerente=id_gerente, nombre_nuevo_usuario=nombre_usuario, rol_nuevo_usuario=rol_usuario)
        console.print("[bold green]Usuario creado exitosamente[/bold green]")
        servicios.mostrar_usuarios(id_gerente=id_gerente)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def eliminar_producto(id_gerente: int, id_producto_a_eliminar: int):
    """
    Comando para que un gerente elimine un producto existente en el inventario.
    """
    try:
        servicios.eliminar_producto(id_gerente=id_gerente, id_producto=id_producto_a_eliminar)
        console.print("[bold green]Producto eliminado exitosamente[/bold green]")
        servicios.mostrar_productos(id_gerente=id_gerente)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)

@app.command()
def eliminar_usuario(id_gerente: int, id_usuario_a_eliminar: int):
    """
    Comando para que un gerente elimine un usuario existente en el sistema.
    """
    try:
        servicios.eliminar_usuario(id_gerente=id_gerente, id_usuario=id_usuario_a_eliminar)
        console.print("[bold green]Usuario eliminado exitosamente[/bold green]")
        servicios.mostrar_usuarios(id_gerente=id_gerente)
    except TiendaError as error_unico:
        typer.secho(str(error_unico), fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()