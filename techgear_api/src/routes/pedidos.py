from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError

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

    # Verificar que la cantidad sea mayor que cero
    if pedido.cantidad <= 0:
        raise HTTPException(
            status_code=400,
            detail="La cantidad debe ser mayor que cero"
        )

    try:
        # Buscar el producto
        producto = await productos_collection.find_one(
            {"_id": ObjectId(pedido.producto_id)}
        )

        # Verificar que el producto exista
        if not producto:
            raise HTTPException(
                status_code=404,
                detail="El producto no existe"
            )

        # Verificar que haya stock suficiente
        if producto.get("stock", 0) <= 0:
            raise HTTPException(
                status_code=400,
                detail="El producto no tiene stock disponible"
            )

        if pedido.cantidad > producto["stock"]:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente. Stock disponible: {producto['stock']}"
            )

        # Convertir el modelo a diccionario
        pedido_dict = pedido.model_dump()

        # Insertar pedido
        resultado = await pedidos_collection.insert_one(
            pedido_dict
        )

        # Descontar el stock
        await productos_collection.update_one(
            {"_id": ObjectId(pedido.producto_id)},
            {
                "$inc": {
                    "stock": -pedido.cantidad
                }
            }
        )

        # Obtener el pedido recién creado
        pedido_creado = await pedidos_collection.find_one(
            {"_id": resultado.inserted_id}
        )

        # Convertir ObjectId a string
        pedido_creado["id"] = str(
            pedido_creado["_id"]
        )

        # Eliminar ObjectId original
        del pedido_creado["_id"]

        return {
            "mensaje": "Pedido registrado correctamente",
            "pedido": pedido_creado
        }

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con la base de datos"
        )


# READ - Obtener pedidos
@router.get("/")
async def obtener_pedidos():

    try:
        pedidos = []

        cursor = pedidos_collection.find()

        async for pedido in cursor:

            pedido["id"] = str(
                pedido["_id"]
            )

            del pedido["_id"]

            pedidos.append(pedido)

        return pedidos

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la base de datos"
        )