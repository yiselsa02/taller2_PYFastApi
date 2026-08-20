from fastapi import FastAPI

from src.routes.productos import router as productos_router
from src.routes.pedidos import router as pedidos_router


app = FastAPI(
    title="TechGear API",
    description="API REST para productos y pedidos de TechGear",
    version="1.0.0"
)


# Registrar rutas
app.include_router(productos_router)
app.include_router(pedidos_router)


@app.get("/")
async def inicio():
    return {
        "mensaje": "Bienvenido a la API de TechGear",
        "estado": "API funcionando"
    }