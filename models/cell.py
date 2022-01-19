from pydantic import BaseModel


class OutCell(BaseModel):
    ix: int
    iy: int
    is_live: int
