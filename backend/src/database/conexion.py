import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la URL de MongoDB Atlas
MONGODB_URL = os.getenv("MONGODB_URL")

# Verificar que exista la URL
if not MONGODB_URL:
    raise ValueError(
        "No se encontró MONGODB_URL. "
        "Verifica que tengas el archivo .env"
    )

# Crear el cliente de MongoDB Atlas
client = AsyncIOMotorClient(MONGODB_URL)

# Seleccionar la base de datos
database = client["techgear"]

# Seleccionar la colección
collection = database["productos"]


# Función para probar la conexión
async def test_connection():
    try:
        # Comprobar conexión con MongoDB Atlas
        await client.admin.command("ping")

        print("✅ Conexión a MongoDB Atlas exitosa")
        print("📦 Base de datos: techgear")
        print("📁 Colección: productos")

        # Documento de prueba
        producto = {
            "nombre": "Teclado mecánico",
            "precio": 150000,
            "categoria": "Periféricos",
            "stock": 10
        }

        # Insertar producto
        print("📥 Guardando producto...")

        resultado = await collection.insert_one(producto)

        print(
            f"✅ Producto guardado con ID: "
            f"{resultado.inserted_id}"
        )

        # Buscar producto
        producto_encontrado = await collection.find_one(
            {"_id": resultado.inserted_id}
        )

        print("📄 Producto encontrado:")
        print(producto_encontrado)

    except Exception as error:
        print(f"❌ Error al conectar a MongoDB: {error}")

    finally:
        client.close()
        print("🔌 Conexión cerrada")


# Ejecutar prueba
if __name__ == "__main__":
    asyncio.run(test_connection())