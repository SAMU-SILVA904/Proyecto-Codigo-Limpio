"""Página de Streamlit: Gestión de Usuarios (Exclusivo para Gerencia)."""

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
    
    # Formateo del Rol ID para que se vea legible en la tabla
    tabla_limpia = [
        {
            "ID": u["id"],
            "Nombre": u["nombre"],
            "Email": u["email"],
            "Rol": "Gerente" if u["rol_id"] == 5 else "Empleado"
        }
        for u in users
    ]
    st.dataframe(tabla_limpia, use_container_width=True, hide_index=True)
    return users

def _form_create(solicitante_id: int) -> None:
    """Formulario para registrar un nuevo trabajador."""
    with st.form("form_create_user", clear_on_submit=True):
        st.subheader("Registrar Nuevo Usuario")
        nombre = st.text_input("Nombre completo")
        email = st.text_input("Correo electrónico")
        rol = st.selectbox("Rol asignado", ["Empleado (Rol 6)", "Gerente (Rol 5)"])
        submitted = st.form_submit_button("Guardar Registro", type="primary")

    if submitted:
        if not nombre or not email:
            st.warning("Todos los campos son obligatorios.")
            return
        rol_id = 5 if "Gerente" in rol else 6
        body = {"nombre": nombre, "email": email, "rol_id": rol_id}
        
        data, err = client.post(f"/usuarios/?solicitante_id={solicitante_id}", body=body)
        if err:
            st.error(f"Error de privilegios o datos: {err}")
        else:
            st.success(f"Usuario **{data['nombre']}** creado exitosamente.")
            st.rerun()

def _form_update(solicitante_id: int, users: list[dict]) -> None:
    """Formulario para editar datos de una cuenta."""
    if not users: return
    st.subheader("Modificar Usuario")
    options = {f"[{u['id']}] {u['nombre']}": u for u in users}
    selected_label = st.selectbox("Selecciona usuario a editar", list(options.keys()), key="edit_user_sel")
    selected = options[selected_label]

    with st.form("form_update_user"):
        new_nombre = st.text_input("Nuevo nombre", value=selected["nombre"])
        new_rol = st.selectbox("Cambiar Rol", ["Empleado (Rol 6)", "Gerente (Rol 5)"], index=0 if selected["rol_id"] == 6 else 1)
        submitted = st.form_submit_button("Guardar Cambios", type="primary")

    if submitted:
        rol_id = 5 if "Gerente" in new_rol else 6
        body = {"nombre": new_nombre, "rol_id": rol_id}
        data, err = client.patch(f"/usuarios/{selected['id']}?solicitante_id={solicitante_id}", body=body)
        if err:
            st.error(f"No se pudo actualizar: {err}")
        else:
            st.success("Cambios aplicados con éxito.")
            st.rerun()

def _form_delete(solicitante_id: int, users: list[dict]) -> None:
    """Formulario de eliminación con la función corregida eliminar_usuario y confirmación."""
    if not users: return
    st.subheader("Eliminar Cuenta del Sistema")
    options = {f"[{u['id']}] {u['nombre']}": u for u in users}
    selected_label = st.selectbox("Selecciona usuario a dar de baja", list(options.keys()), key="del_user_sel")
    user_id = options[selected_label]["id"]

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
    
    # Simulador de sesión para cumplir las reglas de negocio
    solicitante_id = st.number_input("ID del Gerente Operativo (Ej: 36 si es Gerente, o un ID de Empleado para simular bloqueo)", min_value=36, value=36, step=1)
    st.divider()

    users = _show_users_table(solicitante_id)
    st.divider()

    tab_create, tab_edit, tab_delete = st.tabs(["Registrar", "Editar", "Eliminar"])
    with tab_create: _form_create(solicitante_id)
    with tab_edit: _form_update(solicitante_id, users)
    with tab_delete: _form_delete(solicitante_id, users)







