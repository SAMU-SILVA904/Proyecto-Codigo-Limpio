import streamlit as st
from pathlib import Path
from gerencia_app.modelos.rol import Usuario, Producto
from src.gerencia_app.almacenamiento import JSONStorage

"""from src.gerencia_app.servicios import TiendaServicios"""

almacenamiento_usuarios = JSONStorage(base_a_guardar=Path("data/database_usuarios.json"), modelo_clase=Usuario)
almacenamiento_productos = JSONStorage(base_a_guardar=Path("data/database_productos.json"), modelo_clase=Producto)

st.title("App gerencia.")
