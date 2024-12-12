from typing import Optional

from pydantic import BaseModel


class PerguntaDTO(BaseModel):
    id_pergunta: Optional[int] = None
    questao: str
    peso: int

    fk_Evento_Pergunta: int

    class Config:
        orm_mode = True
