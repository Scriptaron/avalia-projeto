from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import TINYINT

from avalia_projeto.persistence.database import Base


class PerfilVO(Base):
    __tablename__ = 'perfil'

    id_perfil = Column(TINYINT(unsigned=True), primary_key=True)
    nome_perfil = Column(String(25), nullable=False, unique=True)

    def __repr__(self):
        return f'<PerfilVO(id_perfil={self.id_perfil}, nome_perfil={self.nome_perfil})>'
