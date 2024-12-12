from avalia_projeto.dao.ProjetoDAO import ProjetoDAO
from avalia_projeto.dto.ProjetoDTO import ProjetoDTO


class ProjetoServices:
    def __init__(self, projeto_dao: ProjetoDAO) -> None:
        self.projeto_dao = projeto_dao

    def criar_projeto(
        self, nome: str, integrantes: str, descricao: str, fk_evento: int
    ) -> None:
        novo_projeto = ProjetoDTO(
            nome_projeto=nome,
            integrantes=integrantes,
            descricao_projeto=descricao,
            fk_Evento_Projeto=fk_evento,
        )

        self.projeto_dao.criar_projeto(novo_projeto)

    def alterar_projeto(self, projeto: ProjetoDTO) -> None:
        self.projeto_dao.alterar_projeto(projeto)

    def deletar_projeto(self, id_projeto: int) -> None:
        self.projeto_dao.deletar_projeto(id_projeto)

    def pesquisar_projetos(self, busca: str, filtro: str) -> list[ProjetoDTO]:
        return self.projeto_dao.get_projetos_filtrados(busca, filtro)

    def pesquisar_pelo_evento(self, evento: int) -> list:
        return self.projeto_dao.get_evento_pelo_nome(evento)

    def listar_projetos(self) -> list[ProjetoDTO]:
        return self.projeto_dao.get_projetos()

    def listar_projetos_pelo_id_evento(
        self, id_evento: int
    ) -> list[ProjetoDTO]:
        return self.projeto_dao.get_projetos_pelo_id_evento(id_evento)

    def listar_nomes_colunas(self) -> list[str]:
        return self.projeto_dao.get_columns_names()
