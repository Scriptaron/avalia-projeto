from typing import Optional

from pydantic import BaseModel


class ProjetoDTO(BaseModel):
    id_projeto: Optional[int] = None
    nome_projeto: str
    integrantes: str
    descricao_projeto: str

    fk_Evento_Projeto: int

    class Config:
        orm_mode = True
