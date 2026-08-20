from fastapi import APIRouter, HTTPException
from bson import ObjectId

from src.database.conexion import (
    pedidos_collection,
    productos_collection
)

from src.models.pedido_model import Pedido


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


# CREATE - Registrar pedido
@router.post("/")
async def crear_pedido(pedido: Pedido):

    # Verificar que el ID tenga formato válido
    if not ObjectId.is_valid(pedido.producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    # Verificar que el producto exista
    producto = await productos_collection.find_one(
        {"_id": ObjectId(pedido.producto_id)}
    )

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="El producto no existe"
        )

    # Convertir el modelo a diccionario
    pedido_dict = pedido.model_dump()

    # Insertar pedido
    resultado = await pedidos_collection.insert_one(
        pedido_dict
    )

    # Obtener el pedido recién creado
    pedido_creado = await pedidos_collection.find_one(
        {"_id": resultado.inserted_id}
    )

    # Convertir ObjectId a string
    pedido_creado["id"] = str(
        pedido_creado["_id"]
    )

    # Eliminar el ObjectId original
    del pedido_creado["_id"]

    return {
        "mensaje": "Pedido registrado correctamente",
        "pedido": pedido_creado
    }


# READ - Obtener pedidos
@router.get("/")
async def obtener_pedidos():

    pedidos = []

    cursor = pedidos_collection.find()

    async for pedido in cursor:

        pedido["id"] = str(
            pedido["_id"]
        )

        del pedido["_id"]

        pedidos.append(pedido)

    return pedidos