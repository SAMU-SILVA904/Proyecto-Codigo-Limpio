"""Página de Streamlit: Gestión del Inventario de Productos (Exclusivo para Gerencia)."""

import streamlit as st
from src.app.api_client import ApiClient

client = ApiClient()

def _show_products_table() -> list[dict]:
    """Carga y despliega el catálogo comercial público."""
    productos, err = client.get("/productos/")
    if err:
        st.error(f"Error al cargar inventario: {err}")
        return []
    if not productos:
        st.info("No hay productos en inventario.")
        return []
    
    st.dataframe(
        productos,
        column_config={
            "id": st.column_config.NumberColumn("ID Producto", width="small"),
            "nombre": st.column_config.TextColumn("Nombre del Producto"),
            "precio": st.column_config.NumberColumn("Precio Unitario", format="$%.2f"),
            "stock": st.column_config.NumberColumn("Unidades Disponibles"),
        },
        use_container_width=True,
        hide_index=True
    )
    return productos

def _form_create(usuario_id: int) -> None:
    with st.form("form_create_prod", clear_on_submit=True):
        st.subheader("Añadir Producto al Inventario")
        nombre = st.text_input("Nombre de la mercancía")
        precio = st.number_input("Precio", min_value=0.0, step=50.0)
        stock = st.number_input("Stock Inicial", min_value=0, step=1)
        submitted = st.form_submit_button("Agregar a Góndola", type="primary")

    if submitted:
        if not nombre or precio <= 0:
            st.warning("Nombre requerido y precio mayor a 0.")
            return
        body = {"nombre": nombre, "precio": precio, "stock": stock}
        data, err = client.post(f"/productos/?usuario_id={usuario_id}", body=body)
        if err:
            st.error(f"Error: {err}")
        else:
            st.success(f"Producto **{data['nombre']}** registrado en stock.")
            st.rerun()

def _form_update(usuario_id: int, productos: list[dict]) -> None:
    if not productos: return
    st.subheader("Actualizar Parámetros de Producto")
    options = {f"[{p['id']}] {p['nombre']}": p for p in productos}
    selected_label = st.selectbox("Selecciona el artículo", list(options.keys()))
    selected = options[selected_label]

    with st.form("form_update_prod"):
        new_nombre = st.text_input("Modificar nombre", value=selected["nombre"])
        new_precio = st.number_input("Modificar precio", min_value=0.0, value=float(selected["precio"]))
        new_stock = st.number_input("Modificar stock", min_value=0, value=int(selected["stock"]))
        submitted = st.form_submit_button("Actualizar Stock", type="primary")

    if submitted:
        body = {"nombre": new_nombre, "precio": new_precio, "stock": new_stock}
        _, err = client.patch(f"/productos/{selected['id']}?usuario_id={usuario_id}", body=body)
        if err:
            st.error(f"Fallo al actualizar: {err}")
        else:
            st.success("Inventario sincronizado.")
            st.rerun()

def _form_delete(usuario_id: int, productos: list[dict]) -> None:
    if not productos: return
    st.subheader("Retirar del Catálogo")
    options = {f"[{p['id']}] {p['nombre']}": p for p in productos}
    selected_label = st.selectbox("Selecciona artículo a remover", list(options.keys()), key="del_prod_sel")
    prod_id = options[selected_label]["id"]

    confirm = st.checkbox(f"Confirmo que deseo destruir el registro del producto ID {prod_id}")
    if st.button("Eliminar del Catálogo", type="primary", disabled=not confirm):
        _, err = client.delete(f"/productos/{prod_id}?usuario_id={usuario_id}")
        if err:
            st.error(f"Error de eliminación: {err}")
        else:
            st.success("Producto purgado correctamente.")
            st.rerun()

def render() -> None:
    st.title("📦 Control de Inventario (Productos)")
    st.caption("Visualización del catálogo general y aprovisionamiento de stock.")
    st.divider()

    usuario_id = st.number_input("ID del Usuario Operador (Se requiere Rol Gerente para Crear/Editar/Eliminar)", min_value=36, value=36, step=1)
    st.divider()

    productos = _show_products_table()
    st.divider()

    tab_create, tab_edit, tab_delete = st.tabs(["Añadir Producto", "Modificar Datos", "Eliminar de Catálogo"])
    with tab_create: _form_create(usuario_id)
    with tab_edit: _form_update(usuario_id, productos)
    with tab_delete: _form_delete(usuario_id, productos)





