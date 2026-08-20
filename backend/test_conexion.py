import asyncio
from src.database.conexion import client


async def probar_conexion():
    try:
        await client.admin.command("ping")
        print("✅ Conexión exitosa con MongoDB Atlas")
    except Exception as e:
        print("❌ Error de conexión:")
        print(e)
    finally:
        client.close()


asyncio.run(probar_conexion())