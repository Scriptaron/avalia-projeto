from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from avalia_projeto.persistence.database import Base


class ProjetoVO(Base):
    __tablename__ = 'projeto'

    id_projeto = Column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    nome_projeto = Column(String(60), nullable=False)
    integrantes = Column(Text, nullable=False)
    descricao_projeto = Column(Text)

    fk_Evento_Projeto = Column(
        INTEGER, ForeignKey('evento.id_evento'), nullable=False
    )

    evento_posts = relationship('EventoVO', backref='projeto_posts')

    def __repr__(self):
        return f'<ProjetoVO(id_projeto={self.id_projeto}, nome_projeto={self.nome_projeto}, integrantes={self.integrantes}, descricao_projeto={self.descricao_projeto})>'
