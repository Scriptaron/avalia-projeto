from datetime import date

from avalia_projeto.dao.EventoDAO import EventoDAO
from avalia_projeto.dto.EventoDTO import EventoDTO


class EventoServices:
    def __init__(self, evento_dao: EventoDAO) -> None:
        self.evento_dao = evento_dao

    def criar_evento(
        self,
        nome: str,
        data_inicio: date,
        data_termino: date,
        descricao: str,
        avaliadores: list[int],
    ) -> None:

        novo_evento = EventoDTO(
            nome_evento=nome,
            data_inicio=data_inicio,
            data_termino=data_termino,
            descricao_evento=descricao,
        )

        self.evento_dao.criar_evento(novo_evento, avaliadores)

    def alterar_evento(self, evento: EventoDTO) -> None:
        self.evento_dao.alterar_evento(evento)

    def deletar_evento(self, id_evento: int) -> None:
        self.evento_dao.deletar_evento(id_evento)

    def pesquisar_eventos(self, busca: str, filtro: str) -> list[EventoDTO]:
        if filtro not in self.listar_nomes_colunas():
            return []

        eventos = self.evento_dao.get_eventos_filtrados(busca, filtro)
        return eventos

    def listar_eventos(self) -> list[EventoDTO]:
        return self.evento_dao.get_eventos()

    def listar_eventos_pelo_id_usuario(
        self, id_usuario: int
    ) -> list[EventoDTO]:
        return self.evento_dao.get_eventos_pelo_id_usuario(id_usuario)

    def listar_nomes_colunas(self) -> list[str]:
        return self.evento_dao.get_columns_names()
