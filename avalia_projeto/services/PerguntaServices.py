from avalia_projeto.dao.PerguntaDAO import PerguntaDAO
from avalia_projeto.dto.PerguntaDTO import PerguntaDTO


class PerguntaServices:
    def __init__(self, pergunta_dao: PerguntaDAO) -> None:
        self.pergunta_dao = pergunta_dao

    def criar_pergunta(self, questao: str, peso: int, fk_evento: int) -> None:
        nova_pergunta = PerguntaDTO(
            questao=questao, peso=peso, fk_Evento_Pergunta=fk_evento
        )
        self.pergunta_dao.criar_pergunta(nova_pergunta)

    def alterar_pergunta(self, pergunta: PerguntaDTO) -> None:
        self.pergunta_dao.alterar_pergunta(pergunta)

    def deletar_pergunta(self, id_pergunta: int) -> None:
        self.pergunta_dao.deletar_pergunta(id_pergunta)

    def pesquisar_pergunta(self, busca: str, filtro: str) -> list[PerguntaDTO]:
        return self.pergunta_dao.get_perguntas_filtradas(busca, filtro)

    def listar_perguntas(self) -> list[PerguntaDTO]:
        return self.pergunta_dao.get_perguntas()

    def listar_perguntas_pelo_id_evento(
        self, id_evento: int
    ) -> list[PerguntaDTO]:
        return self.pergunta_dao.get_perguntas_pelo_id_evento(id_evento)

    def listar_nomes_colunas(self) -> list:
        return self.pergunta_dao.get_columns_names()
