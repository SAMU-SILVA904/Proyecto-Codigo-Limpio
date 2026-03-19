# Sistema de Gestión de Supermercado 🛒

**Gerencia App — Arquitectura de Código Limpio** **Estudiante:** Samuel Silva Cortés
**Institución:** Universidad de Medellín

---

!!! info "Propósito del Proyecto"
    Este sistema está diseñado para centralizar la administración de un supermercado, permitiendo el control total sobre el inventario y la gestión del personal operativo. El enfoque principal es la integridad de los datos y la separación de responsabilidades mediante roles definidos.

## 1. Alcance del Sistema

El sistema permite la administración técnica de dos frentes principales:

1.  **Gestión de Talento Humano:** Registro y control de acceso para Gerentes y Empleados.
2.  **Control de Existencias:** Gestión de stock, precios y flujo de productos en el inventario.

## 2. Caracteristicas

A diferencia de un sistema comercial abierto, este software es de **uso interno**, enfocado en:

| Actor | Responsabilidad Principal |
| --- | --- |
| **Gerente** | Administrador total. Controla la    creación de usuarios, eliminación de productos y supervisión global. |
| **Empleado** | Operador de punto de venta. Gestiona el carrito de compras y realiza la facturación de productos. |

!!! danger "Nota importante"
    Actualmente, el sistema **no contempla el rol de Cliente**. Todas las transacciones de venta son ejecutadas por el **Empleado**.

