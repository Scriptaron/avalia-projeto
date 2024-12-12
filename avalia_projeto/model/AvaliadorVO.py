from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship

from avalia_projeto.persistence.database import Base


class AvaliadorVO(Base):
    __tablename__ = 'avaliador'

    fk_Usuario = Column(
        INTEGER(unsigned=True),
        ForeignKey('usuario.id_usuario'),
        primary_key=True,
    )
    fk_Evento = Column(
        INTEGER(unsigned=True),
        ForeignKey('evento.id_evento'),
        primary_key=True,
    )

    usuario_posts = relationship('UsuarioVO', back_populates='avaliador_posts')
    evento_posts = relationship(
        'EventoVO',
        back_populates='avaliador_posts',
        order_by='EventoVO.id_evento',
    )
