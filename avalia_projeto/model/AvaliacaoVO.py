from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from avalia_projeto.persistence.database import Base


class AvaliacaoVO(Base):
    __tablename__ = 'avaliacao'

    id_avaliacao = Column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    nota = Column(TINYINT, nullable=False)

    fk_Projeto_Avaliacao = Column(
        INTEGER, ForeignKey('projeto.id_projeto'), nullable=False
    )
