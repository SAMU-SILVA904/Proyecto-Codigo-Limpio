"""Entrypoint de Streamlit para el Sistema de Gestión de Supermercado."""

import streamlit as st

from src.app.paginas.usuarios_page import render as render_usuarios
from src.app.paginas.productos_page import render as render_productos
from src.app.paginas.carritos_page import render as render_carritos


def main():
    st.set_page_config(
        page_title="Gestión Supermercado UdeM", page_icon="🏪", layout="wide"
    )

    st.sidebar.title("🏪 Menú Principal")
    st.sidebar.caption("Sistemas de Inventario y Roles")
    st.sidebar.divider()

    opcion = st.sidebar.radio(
        "Módulos del Sistema:",
        ["Dashboard", "Usuarios", "Productos", "Gestión de Carritos"],
    )

    st.sidebar.divider()
    st.sidebar.info("Sesión activa: Administrador de Sistemas")

    if opcion == "Dashboard":
        st.title("📊 Panel de Control General")
        st.write(
            "Bienvenido al sistema de administración de supermercado. "
            "Use el menú lateral de la izquierda para navegar de forma fluida entre los módulos disponibles."
        )

    elif opcion == "Usuarios":
        render_usuarios()

    elif opcion == "Productos":
        render_productos()

    elif opcion == "Gestión de Carritos":
        render_carritos()


if __name__ == "__main__":
    main()