from tkinter import messagebox

from sqlalchemy.orm import sessionmaker

from avalia_projeto.dto.PerfilDTO import PerfilDTO
from avalia_projeto.model.PerfilVO import PerfilVO


class PerfilDAO:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def get_todos_perfis(self) -> list[PerfilDTO]:
        """
        Obtém todos os perfis

        Returns:
            list[PerfilDTO]: Lista de perfis

        Raises:
            Exception: Erro ao obter perfis
        """
        try:
            perfis = (
                self.session.query(PerfilVO).order_by(PerfilVO.id_perfil).all()
            )
            return [
                PerfilDTO(
                    id_perfil=perfil.id_perfil, nome_perfil=perfil.nome_perfil
                )
                for perfil in perfis
            ]
        except Exception as e:
            messagebox.showerror(
                'Erro ao obter perfis', f'Erro ao obter perfis: {e}'
            )
            return []
