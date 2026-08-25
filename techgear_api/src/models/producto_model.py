from pydantic import BaseModel
from typing import Optional


class Producto(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria: str
    imagen: Optional[str] = None