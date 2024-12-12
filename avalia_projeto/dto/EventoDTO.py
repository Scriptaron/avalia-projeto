from datetime import date
from typing import Optional

from pydantic import BaseModel


class EventoDTO(BaseModel):
    id_evento: Optional[int] = None
    nome_evento: str
    data_inicio: date
    data_termino: Optional[date] = None
    descricao_evento: str

    class Config:
        orm_mode = True
