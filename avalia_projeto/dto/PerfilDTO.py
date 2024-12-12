from typing import Optional

from pydantic import BaseModel


class PerfilDTO(BaseModel):
    id_perfil: Optional[int] = None
    nome_perfil: str

    class Config:
        orm_mode = True
