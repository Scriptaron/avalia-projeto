from typing import Optional

from pydantic import BaseModel


class UsuarioDTO(BaseModel):
    id_usuario: Optional[int] = None
    nome_usuario: str
    login: str
    senha: str

    fk_Perfil_Usuario: int

    class Config:
        orm_mode = True
