""""Página de Streamlit: Gestión de Usuarios (Exclusivo para Gerencia)."""

import streamlit as st
from src.app.api_client import ApiClient

client = ApiClient()

def _show_users_table(solicitante_id: int) -> list[dict]:
    """Carga y muestra la tabla de usuarios autorizados."""
    users, err = client.get(f"/usuarios/?solicitante_id={solicitante_id}")
    if err:
        st.error(f"Error al cargar usuarios: {err}")
        return []
    if not users:
        st.info("No hay usuarios registrados todavía.")
        return []
    
    tabla_limpia = [
        {
            "ID": u["usuario_id"],          
            "Nombre": u["nombre_usuario"],  
            "Rol": "Gerente" if u["rol_id"] == 5 else "Empleado" 
        }
        for u in users
    ]
    st.dataframe(tabla_limpia, use_container_width=True, hide_index=True)
    return users

def _form_create(solicitante_id: int) -> None:
    """Formulario modular para registrar un nuevo trabajador en el sistema."""
    st.markdown("### ➕ Registrar Nuevo Usuario")
    
    with st.form("form_registro_usuario", clear_on_submit=True):
        nombre_usuario = st.text_input("Nombre Completo del Trabajador:")
        
        rol_seleccionado = st.selectbox(
            "Rol asignado en el sistema:",
            options=["Empleado", "Gerente"]
        )
        
        rol_id = 5 if rol_seleccionado == "Gerente" else 6
        
        enviado = st.form_submit_button("Crear Usuario")
        
        if enviado:
            if not nombre_usuario.strip():
                st.error("El nombre del usuario no puede estar vacío.")
                return
            
            nuevo_usuario_payload = {
                "nombre_usuario": nombre_usuario.strip(),
                "rol_id": rol_id
            }
            
            data, err = client.post(f"/usuarios/?solicitante_id={solicitante_id}", body=nuevo_usuario_payload)
            
            if err:
                st.error(f"Fallo al registrar en el backend: {err}")
            else:
                st.success(f"¡Usuario **{data['nombre_usuario']}** registrado con éxito con Rol ID {rol_id}!")
                st.rerun() 

def _form_update(solicitante_id: int, users: list[dict]) -> None:
    """Formulario para editar datos de una cuenta."""
    if not users: 
        return
    st.subheader("Modificar Usuario")
    options = {f"Id: [{u['usuario_id']}] | Nombre: '{u['nombre_usuario']}'": u for u in users}
    selected_label = st.selectbox("Selecciona usuario a editar", list(options.keys()), key="edit_user_sel")
    selected = options[selected_label]

    with st.form("form_update_user"):
        new_nombre = st.text_input("Nuevo nombre", value=selected["nombre_usuario"])
        new_rol = st.selectbox("Cambiar Rol", ["Empleado (Rol 6)", "Gerente (Rol 5)"], index=0 if selected["rol_id"] == 6 else 1)
        submitted = st.form_submit_button("Guardar Cambios", type="primary")

    if submitted:
        rol_id = 5 if "Gerente" in new_rol else 6
        
        body = {
            "nombre_usuario": new_nombre.strip(), 
            "rol_id": rol_id
        }
        
        data, err = client.patch(
            f"/usuarios/{selected['usuario_id']}?solicitante_id={solicitante_id}", 
            data=body,
            body=body
        )
        if err:
            st.error(f"No se pudo actualizar: {err}")
        else:
            st.success("¡Cambios aplicados con éxito!")
            st.rerun()

def _form_delete(solicitante_id: int, users: list[dict]) -> None:
    """Formulario de eliminación con la función corregida eliminar_usuario y confirmación."""
    if not users: 
        return
    st.subheader("Eliminar Cuenta del Sistema")
    options = {f"Id: [{u['usuario_id']}] | Nombre: '{u['nombre_usuario']}'": u for u in users}
    selected_label = st.selectbox("Selecciona usuario a dar de baja", list(options.keys()), key="del_user_sel")
    user_id = options[selected_label]["usuario_id"]

    confirm = st.checkbox(f"Confirmo que deseo eliminar permanentemente al usuario ID {user_id}")
    if st.button("Eliminar Usuario", type="primary", disabled=not confirm):
        _, err = client.delete(f"/usuarios/{user_id}?solicitante_id={solicitante_id}")
        if err:
            st.error(f"Operación denegada: {err}")
        else:
            st.success(f"Usuario ID {user_id} removido del sistema.")
            st.rerun()

def render() -> None:
    st.title("👥 Panel de Usuarios")
    st.caption("Administración de roles y credenciales del personal.")
    st.divider()
    
    solicitante_id = st.number_input("ID del Gerente Operativo (Ej: 31 si es Gerente, o un ID de Empleado para simular bloqueo)", min_value=1, value=31, step=1)
    st.divider()

    users = _show_users_table(solicitante_id)
    st.divider()

    tab_create, tab_edit, tab_delete = st.tabs(["Registrar", "Editar", "Eliminar"])
    with tab_create:
        _form_create(solicitante_id)
    with tab_edit:
        _form_update(solicitante_id, users)
    with tab_delete:
        _form_delete(solicitante_id, users)