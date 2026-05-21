"""
Punto de entrada principal de la API en FastAPI.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routers.usuarios_router import router as usuarios_router
from src.api.routers.productos_router import router as productos_router
from src.api.routers.carritos_router import router as carritos_router

app = FastAPI(
    title="API de Supermercado",
    description="Backend en FastAPI para la gestión de inventario y carritos de compras",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de Enrutadores
app.include_router(usuarios_router)
app.include_router(productos_router)
app.include_router(carritos_router)

@app.get("/")
def read_root():
    return {"status": "Running", "proyecto": "Sistema de Supermercado - UdeM"}


