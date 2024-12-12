from sqlalchemy import Column, Date, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from avalia_projeto.persistence.database import Base


class EventoVO(Base):
    __tablename__ = 'evento'

    id_evento = Column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    nome_evento = Column(String(60), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_termino = Column(Date)
    descricao_evento = Column(Text)

    avaliador_posts = relationship(
        'AvaliadorVO', back_populates='evento_posts'
    )

    def __repr__(self):
        return f'<EventoVO(id_evento={self.id_evento}, nome_evento={self.nome_evento}, data_inicio={self.data_inicio}, data_termino={self.data_termino}, descricao_evento={self.descricao_evento})>'
