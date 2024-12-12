from base64 import b64decode
from tkinter import messagebox

from bcrypt import checkpw
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from avalia_projeto.dto.UsuarioDTO import UsuarioDTO
from avalia_projeto.model.PerfilVO import PerfilVO
from avalia_projeto.model.UsuarioVO import UsuarioVO


class UsuarioDAO:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def autenticar(
        self, login: str, senha: str, perfil: int
    ) -> list[UsuarioDTO]:
        try:
            usuario = (
                self.session.query(UsuarioVO)
                .filter_by(login=login, fk_Perfil_Usuario=perfil)
                .first()
            )
            if usuario:
                if checkpw(senha.encode('utf-8'), b64decode(usuario.senha)):
                    return UsuarioDTO(
                        id_usuario=usuario.id_usuario,
                        nome_usuario=usuario.nome_usuario,
                        login=login,
                        senha=usuario.senha,
                        fk_Perfil_Usuario=usuario.fk_Perfil_Usuario,
                    )
                else:
                    return None
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao autenticar',
                f'Erro ao autenticar: Detalhes: {sqla_error}',
            )

    def criar_usuario(self, novo_usuario: UsuarioDTO) -> None:
        try:
            novo_usuario = UsuarioVO(
                nome_usuario=novo_usuario.nome_usuario,
                login=novo_usuario.login,
                senha=novo_usuario.senha,
                fk_Perfil_Usuario=novo_usuario.fk_Perfil_Usuario,
            )
            self.session.add(novo_usuario)
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao criar usuario',
                f'Erro ao criar usuario: Detalhes: {sqla_error}',
            )
            return

    def alterar_usuario(self, usuario: UsuarioDTO) -> None:
        try:
            self.session.query(UsuarioVO).filter_by(
                id_usuario=usuario.id_usuario
            ).update(
                {
                    'nome_usuario': usuario.nome_usuario,
                    'login': usuario.login,
                    'senha': usuario.senha,
                    'fk_Perfil_Usuario': usuario.fk_Perfil_Usuario,
                }
            )
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao alterar usuario',
                f'Erro ao alterar usuario: Detalhes: {sqla_error}',
            )
            return

    def deletar_usuario(self, id_usuario: int) -> None:
        try:
            usuario = self.session.query(UsuarioVO).get(id_usuario)
            if usuario:
                self.session.delete(usuario)
                self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao deletar usuario',
                f'Erro ao deletar usuario: Detalhes: {sqla_error}',
            )
            return

    def get_usuarios(self) -> list[UsuarioDTO]:
        try:
            usuarios = self.session.query(UsuarioVO).all()

            usuarios_dto = [
                UsuarioDTO(
                    id_usuario=usuario.id_usuario,
                    nome_usuario=usuario.nome_usuario,
                    login=usuario.login,
                    senha=usuario.senha,
                    fk_Perfil_Usuario=usuario.fk_Perfil_Usuario,
                )
                for usuario in usuarios
            ]
            return usuarios_dto
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter usuarios',
                f'Erro ao obter usuarios: Detalhes: {sqla_error}',
            )
            return []

    def get_usuarios_pelo_perfil(self, busca: str) -> list[UsuarioDTO]:
        usuarios = (
            self.session.query(UsuarioVO)
            .join(PerfilVO)
            .filter(PerfilVO.nome_perfil.ilike(f'%{busca}%'))
            .all()
        )
        return usuarios

    def get_usuarios_filtrados(
        self, busca: str, filtro: str
    ) -> list[UsuarioDTO]:
        try:
            usuarios = (
                self.session.query(UsuarioVO)
                .filter(text(f'{filtro} like :busca'))
                .params(busca=f'%{busca}%')
                .all()
            )

            usuarios_dto = [
                UsuarioDTO(
                    id_usuario=usuario.id_usuario,
                    nome_usuario=usuario.nome_usuario,
                    login=usuario.login,
                    senha=usuario.senha,
                    fk_Perfil_Usuario=usuario.fk_Perfil_Usuario,
                )
                for usuario in usuarios
            ]
            return usuarios_dto
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter usuarios',
                f'Erro ao obter usuarios: Detalhes: {sqla_error}',
            )
            return []

    def get_column_names(self) -> list:
        return [c.name for c in UsuarioVO.__table__.columns]
