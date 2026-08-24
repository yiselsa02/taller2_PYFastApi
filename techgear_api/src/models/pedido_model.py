from pydantic import BaseModel


class Pedido(BaseModel):
    producto_id: str
    cantidad: int
    cliente: str