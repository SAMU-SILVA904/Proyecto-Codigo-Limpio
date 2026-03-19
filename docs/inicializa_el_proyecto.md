# Guía de Inicio: Sistema de Gestión de Supermercado 🛒

Bienvenido a la documentación oficial del **Sistema de Gestión de Inventario**. Este proyecto ha sido diseñado bajo estándares de **Código Limpio** y arquitectura por capas para garantizar un entorno administrativo robusto y profesional.

---

## 🚀 Configuración del Entorno

Sigue estos pasos para desplegar el proyecto en tu máquina local:

# 🛠️ Configuración del Entorno: De la Terminal al Primer Proyecto

Esta guía asume que ya has habilitado **WSL2** en tu sistema. Si no lo has hecho, el primer paso es seguir la documentación oficial.

## 1. Preparación de WSL (Windows Subsystem for Linux)

Antes de continuar, asegúrate de tener instalada una distribución de Linux (recomendamos **Ubuntu 22.04 LTS** o superior).

- [Guía de Instalación oficial de Microsoft](https://learn.microsoft.com/en-us/windows/wsl/install)


> **⚠️ Importante:** Todos los comandos que verás a continuación **DEBEN** ser ejecutados dentro de tu terminal de Ubuntu (la ventana negra de Linux), **no** en el PowerShell ni en el CMD de Windows.

---

## 2. Instalación de Git

Git es esencial para el control de versiones y es un requisito para que `uv` gestione algunas dependencias. En tu terminal de Ubuntu, ejecuta:

```Bash
sudo apt update
sudo apt install git -y
```

>*Puedes verificar la instalación con `git --version`.*

---

## 3. Instalación de `uv`

`uv` será nuestro gestor de paquetes y versiones de Python. Es extremadamente rápido y eficiente.

1. **Instalador:**

```Bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Configuración del entorno:** Para que el comando `uv` funcione de inmediato, reinicia la terminal:

---

## 4. Gestión de Python con `uv`

A diferencia de las instalaciones tradicionales, con `uv` no necesitas instalar Python globalmente en tu sistema. Vamos a descargar la última versión estable (3.12 o superior) para nuestras clases:

```Bash
# Descarga e instala la última versión de Python
uv python install 3.12
```
---

Una vez tenemos ``git`` , ``uv`` y ``python3`` lo que haremos es:

### 1. Clonar el repositorio
```bash
git clone https://github.com/SAMU-SILVA904/Proyecto-Codigo-Limpio.git
```

### 2. Instalación de dependencias
El proyecto utiliza uv para la gestión de paquetes. Instala todo lo necesario con:

```Bash
uv sync
uv run main.py --help
```

Esto desplegará las opciones que tienes de CLI para ejecutar la aplicación.

Recuerda que puedes consultar la [Guía de Comandos](Guia_usuario/comandos.md) para aprender a usar la CLI.

