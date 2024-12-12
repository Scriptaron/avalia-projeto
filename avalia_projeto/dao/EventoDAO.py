from tkinter import messagebox

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from avalia_projeto.dto.EventoDTO import EventoDTO
from avalia_projeto.model.AvaliadorVO import AvaliadorVO
from avalia_projeto.model.EventoVO import EventoVO


class EventoDAO:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def criar_evento(
        self, novo_evento: EventoDTO, avaliadores: list[int]
    ) -> None:
        try:
            novo_evento_vo = EventoVO(
                nome_evento=novo_evento.nome_evento,
                data_inicio=novo_evento.data_inicio,
                data_termino=novo_evento.data_termino,
                descricao_evento=novo_evento.descricao_evento,
            )

            self.session.add(novo_evento_vo)
            self.session.flush()

            for avaliador_id in avaliadores:
                avaliador_vo = AvaliadorVO(
                    fk_Usuario=avaliador_id, fk_Evento=novo_evento_vo.id_evento
                )
                self.session.add(avaliador_vo)

            self.session.commit()

        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao criar evento',
                f'Erro ao criar evento: Detalhes: {sqla_error}',
            )
            return

    def alterar_evento(self, evento: EventoDTO):
        try:
            self.session.query(EventoVO).filter_by(
                id_evento=evento.id_evento
            ).update(
                {
                    'nome_evento': evento.nome_evento,
                    'data_inicio': evento.data_inicio,
                    'data_termino': evento.data_termino,
                    'descricao_evento': evento.descricao_evento,
                }
            )
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao alterar evento',
                f'Erro ao alterar evento: Detalhes: {sqla_error}',
            )
            return

    def deletar_evento(self, id_evento):
        try:
            evento = self.session.query(EventoVO).get(id_evento)
            if evento:
                self.session.delete(evento)
                self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao deletar evento',
                f'Erro ao deletar evento: Detalhes: {sqla_error}',
            )
            return

    def get_eventos(self) -> list[EventoDTO]:
        try:
            eventos = self.session.query(EventoVO).all()

            eventos_dto = [
                EventoDTO(
                    id_evento=evento.id_evento,
                    nome_evento=evento.nome_evento,
                    data_inicio=evento.data_inicio,
                    data_termino=evento.data_termino,
                    descricao_evento=evento.descricao_evento,
                )
                for evento in eventos
            ]
            return eventos_dto
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter eventos',
                f'Erro ao obter eventos: Detalhes: {sqla_error}',
            )
            return []

    def get_eventos_filtrados(
        self, busca: str, filtro: str
    ) -> list[EventoDTO]:
        try:
            eventos = (
                self.session.query(EventoVO)
                .filter(text(f'{filtro} like :busca'))
                .params(busca=f'%{busca}%')
                .all()
            )

            eventos_dto = [
                EventoDTO(
                    id_evento=evento.id_evento,
                    nome_evento=evento.nome_evento,
                    data_inicio=evento.data_inicio,
                    data_termino=evento.data_termino,
                    descricao_evento=evento.descricao_evento,
                )
                for evento in eventos
            ]
            return eventos_dto

        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter eventos',
                f'Erro ao obter eventos: Detalhes: {sqla_error}',
            )
            return []

    def get_eventos_pelo_id_usuario(self, id_usuario: int) -> list[EventoDTO]:
        try:
            with self.session as session:
                eventos = (
                    session.query(EventoVO)
                    .join(
                        AvaliadorVO,
                        AvaliadorVO.fk_Evento == EventoVO.id_evento,
                    )
                    .filter(AvaliadorVO.fk_Usuario == id_usuario)
                    .all()
                )
                return eventos

        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter eventos',
                f'Erro ao obter eventos: Detalhes: {sqla_error}',
            )
            return []

    def get_columns_names(self) -> list:
        return [c.name for c in EventoVO.__table__.columns]
