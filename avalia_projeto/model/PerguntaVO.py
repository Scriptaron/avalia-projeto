from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from avalia_projeto.persistence.database import Base


class PerguntaVO(Base):
    __tablename__ = 'pergunta'

    id_pergunta = Column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    questao = Column(Text, nullable=False)
    peso = Column(TINYINT, nullable=False)
    fk_Evento_Pergunta = Column(
        INTEGER(unsigned=True), ForeignKey('evento.id_evento'), nullable=False
    )

    evento_posts = relationship('EventoVO', backref='pergunta_posts')

    def __repr__(self):
        return f'<PerguntaVO(id_pergunta={self.id_pergunta}, questao={self.questao}, peso={self.peso}, fk_Evento_Pergunta={self.fk_Evento_Pergunta})>'
