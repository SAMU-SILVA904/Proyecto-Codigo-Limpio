# Carrito de Compras (`CarritoService`)

Maneja los flujos de compra temporales e interactúa con el inventario seleccionado por los empleados.

## Reglas Críticas de Negocio
* **Exclusión de Roles de Supervisión:** Debido a que el rol de Gerencia está diseñado exclusivamente para administración y control, los usuarios con `rol_id == 5` tienen **bloqueada** la inicialización de carritos. Intentar abrir un carrito para un Gerente levantará una excepción controlada del dominio.