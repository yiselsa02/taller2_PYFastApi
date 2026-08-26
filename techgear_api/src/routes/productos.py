from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError

from src.database.conexion import productos_collection
from src.models.producto_model import Producto


router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


# CREATE - Crear producto
@router.post("/")
async def crear_producto(producto: Producto):

    try:
        producto_dict = producto.model_dump()

        resultado = await productos_collection.insert_one(producto_dict)

        producto_creado = await productos_collection.find_one(
            {"_id": resultado.inserted_id}
        )

        producto_creado["id"] = str(producto_creado["_id"])
        del producto_creado["_id"]

        return {
            "mensaje": "Producto creado correctamente",
            "producto": producto_creado
        }

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar con la base de datos"
        )


# READ - Obtener todos los productos
@router.get("/")
async def obtener_productos():

    try:
        productos = []

        cursor = productos_collection.find()

        async for producto in cursor:
            producto["id"] = str(producto["_id"])
            del producto["_id"]

            productos.append(producto)

        return productos

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la base de datos"
        )


# READ - Obtener un producto por ID
@router.get("/{producto_id}")
async def obtener_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    try:
        producto = await productos_collection.find_one(
            {"_id": ObjectId(producto_id)}
        )

        if not producto:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        producto["id"] = str(producto["_id"])
        del producto["_id"]

        return producto

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo consultar la base de datos"
        )


# UPDATE - Actualizar producto
@router.put("/{producto_id}")
async def actualizar_producto(
    producto_id: str,
    producto: Producto
):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    try:
        resultado = await productos_collection.update_one(
            {"_id": ObjectId(producto_id)},
            {"$set": producto.model_dump()}
        )

        if resultado.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        producto_actualizado = await productos_collection.find_one(
            {"_id": ObjectId(producto_id)}
        )

        producto_actualizado["id"] = str(
            producto_actualizado["_id"]
        )

        del producto_actualizado["_id"]

        return {
            "mensaje": "Producto actualizado correctamente",
            "producto": producto_actualizado
        }

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo actualizar el producto"
        )


# DELETE - Eliminar producto
@router.delete("/{producto_id}")
async def eliminar_producto(producto_id: str):

    if not ObjectId.is_valid(producto_id):
        raise HTTPException(
            status_code=400,
            detail="El ID del producto no es válido"
        )

    try:
        resultado = await productos_collection.delete_one(
            {"_id": ObjectId(producto_id)}
        )

        if resultado.deleted_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Producto no encontrado"
            )

        return {
            "mensaje": "Producto eliminado correctamente"
        }

    except HTTPException:
        raise

    except PyMongoError:
        raise HTTPException(
            status_code=503,
            detail="No se pudo eliminar el producto"
        )