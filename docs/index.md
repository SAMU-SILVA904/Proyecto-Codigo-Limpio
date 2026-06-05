# Sistema de Gestión de Supermercado 🛒

Bienvenido a la documentación oficial del **Sistema de Gestión de Supermercado**. Este proyecto ha sido diseñado aplicando principios de **Código Limpio** y **Arquitectura Limpia**, garantizando un desarrollo escalable, mantenible y altamente testable. ☯️

## Propósito del Sistema 
La aplicación tiene como objetivo principal la administración eficiente de:
* **Inventario y Catálogo de Productos:** Control estricto sobre existencias, precios y artículos en los estantes.
* **Roles de Empleados:** Gestión operativa segregando funciones críticas.
* **Carrito de Compras:** Flujo personal para que el personal operativo gestione la selección de productos.
!!! info "Usuarios"
    Actualmente la aplicación no cuenta con una entidad de usuario, está hecha unicamente para gerentes y empleados.

## Características de Calidad
* **Linter Estricto:** Cumplimiento de guías PEP 8 a través de `ruff`.
* **Complejidad Controlada:** Monitoreo de la complejidad ciclomática de las funciones con `radon`.
* **Pruebas Automatizadas:** Suite completa de pruebas unitarias aisladas de la base de datos mediante `pytest` y `unittest.mock`.