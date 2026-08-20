import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la URL de MongoDB Atlas
MONGODB_URL = os.getenv("MONGODB_URL")

# Verificar que exista la URL
if not MONGODB_URL:
    raise ValueError("No se encontró MONGODB_URL en el archivo .env")

# Crear conexión con MongoDB Atlas
client = AsyncIOMotorClient(MONGODB_URL)

# Seleccionar la base de datos
database = client.ambiente502

# Seleccionar las colecciones
productos_collection = database.productos
pedidos_collection = database.pedidos