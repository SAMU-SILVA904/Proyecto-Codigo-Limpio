"""Página de Streamlit: Gestión de Carritos de Compra (Exclusivo Empleados)."""

import streamlit as st
from src.app.api_client import ApiClient

client = ApiClient()

def _show_cart_section() -> None:
    st.subheader("Mi Carrito Personal")
    usuario_id = st.number_input("Ingresa tu ID de Empleado", min_value=31, value=31, step=1, key="cart_uid")
    
    if st.button("Sincronizar mi Carrito", type="primary"):
        carrito, err = client.get(f"/carritos/{usuario_id}")
        if err:
            st.error(f"Operación no válida: {err}")
        elif not carrito or not carrito.get("items"):
            st.info("Tu carrito personal está vacío actualmente.")
        else:
            st.success(f"¡Carrito cargado con éxito para el usuario {usuario_id}!")
            tabla_items = [
                {
                    "Ítem ID": item["id"],
                    "Producto ID": item["producto_id"],
                    "Cantidad": item["cantidad"],
                }
                for item in carrito["items"]
            ]
            st.dataframe(tabla_items, use_container_width=True, hide_index=True)

def _form_add_item() -> None:
    st.subheader("Añadir Ítems al Carrito")
    with st.form("form_add_cart"):
        uid = st.number_input("Mi ID de Empleado", min_value=31, step=1)
        pid = st.number_input("ID del Producto a comprar", min_value=1, step=1)
        qty = st.number_input("Cantidad de unidades", min_value=1, value=1, step=1)
        submitted = st.form_submit_button("Agregar al Carrito", type="primary")
        
    if submitted:
        _, err = client.post(f"/carritos/{uid}/agregar?producto_id={pid}&cantidad={qty}")
        if err:
            st.error(f"No se pudo añadir: {err}")
        else:
            st.success("Producto sumado al carrito.")
            st.rerun()

def _form_remove_item() -> None:
    st.subheader("Remover Ítem por Completo")
    with st.form("form_del_cart"):
        uid = st.number_input("Mi ID de Empleado", min_value=31, step=1, key="del_c_uid")
        pid = st.number_input("ID del Producto a quitar", min_value=1, step=1, key="del_c_pid")
        submitted = st.form_submit_button("Eliminar del Carrito", type="primary")

    if submitted:
        _, err = client.delete(f"/carritos/{uid}/remover/{pid}")
        if err:
            st.error(f"Fallo al remover artículo: {err}")
        else:
            st.success(f"Producto {pid} extraído de tu carrito personal.")
            st.rerun()

def render() -> None:
    st.title("🛒 Carritos de Compra")
    st.caption("Espacio personal de abastecimiento para empleados.")
    st.divider()

    tab_view, tab_add, tab_remove = st.tabs(["Ver mi Carrito", "Agregar Artículos", "Quitar Artículos"])
    with tab_view: _show_cart_section()
    with tab_add: _form_add_item()
    with tab_remove: _form_remove_item()
    
    
    


