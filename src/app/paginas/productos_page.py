"""Página de Streamlit: Gestión del Inventario de Productos (Exclusivo para Gerencia)."""

import streamlit as st
from src.app.api_client import ApiClient

client = ApiClient()

def _show_products_table(productos: list[dict]) -> None:
    st.markdown("### 📦 Inventario Actual")
    
    tabla_limpia = [
        {
            "ID Producto": p["producto_id"], 
            "Descripción": p["nombre"],
            "Precio Unitario": f"${p['precio']:,}",
            "Unidades en Stock": p["stock"]
        }
        for p in productos
    ]
    st.dataframe(tabla_limpia, use_container_width=True)

def _form_create(usuario_id: int) -> None:
    st.subheader("➕ Registrar Nuevo Producto")
    
    with st.form("form_nuevo_producto", clear_on_submit=True):
        nombre_input = st.text_input("Nombre o Descripción del Producto:")
        precio_input = st.number_input("Precio de Venta ($):", min_value=0.0, step=50.0)
        stock_input = st.number_input("Cantidad Inicial en Stock:", min_value=0, step=1)
        
        enviado = st.form_submit_button("Guardar en Inventario")
        
        if enviado:
            if not nombre_input.strip():
                st.error("El nombre del producto es obligatorio.")
                return
                
            nuevo_producto_payload = {
                "nombre": nombre_input.strip(), 
                "precio": float(precio_input),  
                "stock": int(stock_input)      
            }
            
            try:
                response, err = client.post(f"/productos/?usuario_id={usuario_id}", body=nuevo_producto_payload)
                
                if err:
                    st.error(f"Fallo en el backend: {err}")
                else:
                    st.success(f"¡Producto **{response['nombre']}** creado con éxito con el ID {response['producto_id']}!")
                    st.rerun() # Recarga la vista para mostrar el nuevo producto en la tabla
            except Exception as e:
                st.error(f"Error de conexión: {str(e)}")
            st.rerun()

def _form_update(usuario_id: int, productos: list[dict]) -> None:
    if not productos:
        return
        
    st.subheader("🔄 Actualizar / Cambiar Producto")
    
    options = {f"ID: [{p['producto_id']}] | Nombre: '{p['nombre']}'": p for p in productos}
    selected_label = st.selectbox("Selecciona el artículo a modificar", list(options.keys()))
    producto_seleccionado = options[selected_label]
    
    with st.form(f"form_actualizar_{producto_seleccionado['producto_id']}"):
        st.markdown(f"**Modificando:** {producto_seleccionado['nombre']} (ID: {producto_seleccionado['producto_id']})")
        
        nuevo_nombre = st.text_input(
            "Nuevo Nombre / Descripción:", 
            value=producto_seleccionado["nombre"]
        )
        
        nuevo_precio = st.number_input(
            "Nuevo Precio ($):", 
            min_value=0.0, 
            value=float(producto_seleccionado["precio"]), 
            step=50.0
        )
        
        nuevo_stock = st.number_input(
            "Nuevo Stock en Inventario:", 
            min_value=0, 
            value=int(producto_seleccionado["stock"]), 
            step=1
        )
        
        enviado = st.form_submit_button("Aplicar Cambios")
        
        if enviado:
            if not nuevo_nombre.strip():
                st.error("El nombre del producto no puede quedar vacío.")
                return
            producto_data_payload = {
                "nombre": nuevo_nombre.strip(),
                "precio": float(nuevo_precio),
                "stock": int(nuevo_stock)
            }
            
            try:
                endpoint = f"/productos/{producto_seleccionado['producto_id']}?usuario_id={usuario_id}"
                response, err = client.patch(endpoint, body=producto_data_payload)
                
                if err:
                    st.error(f"Fallo al actualizar en el backend: {err}")
                else:
                    st.success(f"¡Producto **[{producto_seleccionado['producto_id']}]** actualizado con éxito!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error de comunicación: {str(e)}")
    

def _form_delete(usuario_id: int, productos: list[dict]) -> None:
    if not productos: return
    st.subheader("🗑️ Eliminar Producto del Catálogo")
    
    options = {f"Id: [{p['producto_id']}] | Nombre: '{p['nombre']}'": p for p in productos}
    selected_label = st.selectbox("Selecciona el artículo a remover", list(options.keys()), key="del_prod_sel")
    selected = options[selected_label]
    
    if st.button("Confirmar Eliminación Permanente", type="primary"):
        try:
            client.delete(f"/productos/{selected['producto_id']}?usuario_id={usuario_id}")
            st.success(f"Producto [{selected['producto_id']}] eliminado correctamente.")
            st.rerun()
        except Exception as e:
            st.error(f"Error al eliminar: {str(e)}")

def render() -> None:
    st.title("📦 Control de Inventario (Productos)")
    st.caption("Visualización del catálogo general y aprovisionamiento de stock.")
    st.divider()

    usuario_id = st.number_input("ID del Usuario Operador (Se requiere Rol Gerente)", min_value=1, value=31, step=1)
    st.divider()
    res_data, err = client.get("/productos/")
    if err:
        st.error(f"No se pudo cargar el catálogo de productos: {err}")
        productos = []  
    else:
        productos = res_data
    
    _show_products_table(productos)
    st.divider()
    
    tab_create, tab_edit, tab_delete = st.tabs(["Añadir Producto", "Modificar Producto", "Eliminar Producto"])
    with tab_create:
        _form_create(usuario_id)
        
    with tab_edit:
        _form_update(usuario_id, productos)
        
    with tab_delete:
        _form_delete(usuario_id, productos)





