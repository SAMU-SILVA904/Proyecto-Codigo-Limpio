# Catálogo de Productos (`ProductoService`)

Administra las operaciones de lectura, inserción y eliminación física de productos dentro del catálogo comercial del supermercado.

## Reglas Críticas de Negocio
* **Mutaciones Restringidas:** Solo los Gerentes pueden realizar mutaciones sobre el catálogo (`crear_producto`, `actualizar_producto`, `eliminar_producto`). Cualquier intento por parte de un rol no autorizado disparará inmediatamente una excepción de tipo `PermisoDenegadoError`.