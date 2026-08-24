import os
from pathlib import Path

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv


# Buscar el archivo .env en la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parents[3]
ENV_FILE = BASE_DIR / ".env"

# Cargar las variables del archivo .env
load_dotenv(ENV_FILE)


# Obtener la URL de MongoDB Atlas
MONGODB_URL = os.getenv("MONGODB_URL")


# Verificar que exista la URL
if not MONGODB_URL:
    raise ValueError(
        f"No se encontró MONGODB_URL en: {ENV_FILE}"
    )


# Crear conexión con MongoDB Atlas
client = AsyncIOMotorClient(MONGODB_URL)


# Seleccionar la base de datos
database = client["techgear"]


# Seleccionar las colecciones
productos_collection = database["productos"]
pedidos_collection = database["pedidos"]