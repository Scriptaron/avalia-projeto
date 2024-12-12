from pydantic import BaseModel


class AvaliadorDTO(BaseModel):
    fk_Usuario: int
    fk_Evento: int

    class Config:
        orm_mode = True
