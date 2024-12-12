from avalia_projeto.dao.PerfilDAO import PerfilDAO
from avalia_projeto.dto.PerfilDTO import PerfilDTO


class PerfilServices:
    def __init__(self, perfil_dao: PerfilDAO) -> None:
        self.perfil_dao = perfil_dao

    def buscar_todos_perfis(self) -> list[PerfilDTO]:
        """
        Busca todos os perfis

        Returns:
            list[PerfilDTO]: Lista de perfis
        """
        return self.perfil_dao.get_todos_perfis()
