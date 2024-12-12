from typing import Optional

from pydantic import BaseModel


class AvaliacaoDTO(BaseModel):
    id_avaliacao: Optional[int] = None
    nota: int

    fk_Projeto_Avaliacao: int

    class Config:
        orm_mode = True
