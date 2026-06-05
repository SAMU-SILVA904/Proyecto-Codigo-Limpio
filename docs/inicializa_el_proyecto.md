# Inicialización del Proyecto

Sigue estos pasos para configurar y ejecutar el entorno de desarrollo de forma local.

!!! alert "Prerrequisitos"
    El proyecto gestiona sus dependencias utilizando **uv**, un gestor de paquetes de Python extremadamente rápido. Asegúrate de tenerlo instalado en tu sistema antes de continuar.

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

# Pasos para la Configuración

## Paso 1: Clonar repositorio 🎭

Abre tu terminal y descarga el proyecto ejecutando:
```bash
git clone <url-de-tu-repositorio>
cd proyecto_cod_limpio
```

## Paso 2: Instalar Dependencias 🧵

Utiliza `uv` para sincronizar el entorno virtual basado en el archivo lock e instalar de forma exacta todas las librerías necesarias:
```bash
uv sync
```

## Paso 3: Herramientas de Calidad 🚀

Puedes validar el estado del código ejecutando en tu terminal los siguientes comandos individuales:

* **Verificar Estilo (Linter):**
```bash
uv run ruff check
```

* **Analizar Complejidad Ciclomática:**
```bash
uv run radon cc src -a
```

* **Ejecutar Suite de Pruebas Unitarias:**
```bash
uv run pytest -v
```

4. **Ejecución del Sistema Completo** 🌎

Para poner en marcha la aplicación, debes levantar tanto el servidor de la API (backend) como la interfaz gráfica (frontend). Se recomienda abrir dos terminales independientes en la raíz del proyecto:

### a. Levantar Endpoints (FastAPI):
En la primera terminal, ejecuta el siguiente comando para activar el servidor local de la API y habilitar los endpoints de usuarios, productos y carritos:

```bash
uv run uvicorn src.api.main:app --reload
```

>* Adicionalmente, tambien puedes abrir una documentación de los endpoints automatica agregando `/docs` o `/redoc` al final del enlace que adjunta en la terminal.

### b.Levantar la Interfaz Gráfica (Streamlit):
En la segunda terminal, ejecuta el siguiente comando para iniciar la aplicación web de Streamlit que se conectará a los endpoints anteriores:
```bash
uv run streamlit run app.py
```