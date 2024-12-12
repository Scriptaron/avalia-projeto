from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship

from avalia_projeto.persistence.database import Base


class UsuarioVO(Base):
    __tablename__ = 'usuario'

    id_usuario = Column(
        INTEGER(unsigned=True), primary_key=True, autoincrement=True
    )
    nome_usuario = Column(String(50), nullable=False)
    login = Column(String(25), nullable=False)
    senha = Column(String(255), nullable=False)

    fk_Perfil_Usuario = Column(
        TINYINT, ForeignKey('perfil.id_perfil'), nullable=False
    )

    perfil_posts = relationship(
        'PerfilVO', backref='posts', order_by='PerfilVO.nome_perfil'
    )

    avaliador_posts = relationship(
        'AvaliadorVO', back_populates='usuario_posts'
    )

    def __repr__(self):
        return f'<UsuarioVO(id_usuario={self.id_usuario}, nome_usuario={self.nome_usuario}, login={self.login}, senha={self.senha}, fk_Perfil_Usuario={self.fk_Perfil_Usuario})>'
