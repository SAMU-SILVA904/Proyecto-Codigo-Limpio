# Gestión de Usuarios (`UsuarioService`)

Controla el ciclo de vida de los usuarios dentro de la plataforma y centraliza las validaciones de identidad requeridas por el negocio.

## Reglas Críticas de Negocio
* **Validación de Permisos de Gerente:** Solo los perfiles que cuenten con el `rol_id == 5` (Gerente) tienen permitido registrar o modificar los datos de otras cuentas de usuario en el sistema. Los empleados comunes (`rol_id == 6`) tienen denegada esta acción de forma automática.