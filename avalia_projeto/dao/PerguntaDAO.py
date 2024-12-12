from tkinter import messagebox

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from avalia_projeto.dto.PerguntaDTO import PerguntaDTO
from avalia_projeto.model.PerguntaVO import PerguntaVO


class PerguntaDAO:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def criar_pergunta(self, nova_pergunta: PerguntaDTO) -> None:
        try:
            nova_pergunta = PerguntaVO(
                questao=nova_pergunta.questao,
                peso=nova_pergunta.peso,
                fk_Evento_Pergunta=nova_pergunta.fk_Evento_Pergunta,
            )
            self.session.add(nova_pergunta)
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao criar pergunta',
                f'Erro ao criar pergunta: Detalhes: {sqla_error}',
            )

    def alterar_pergunta(self, pergunta: PerguntaDTO):
        try:
            self.session.query(PerguntaDTO).filter_by(
                id_pergunta=pergunta.id_pergunta
            ).update(
                {
                    'questao': pergunta.questao,
                    'peso': pergunta.peso,
                    'fk_Evento_Pergunta': pergunta.fk_Evento_Pergunta,
                }
            )
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao alterar pergunta',
                f'Erro ao alterar pergunta: Detalhes: {sqla_error}',
            )

    def deletar_pergunta(self, id_pergunta: int) -> None:
        try:
            pergunta = self.session.query(PerguntaDTO).get(id_pergunta)
            if pergunta:
                self.session.delete(pergunta)
                self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao deletar pergunta',
                f'Erro ao deletar pergunta: Detalhes: {sqla_error}',
            )

    def get_perguntas(self) -> list[PerguntaDTO]:
        try:
            perguntas = self.session.query(PerguntaVO).all()

            pergunta_dto = [
                PerguntaDTO(
                    id_pergunta=pergunta.id_pergunta,
                    questao=pergunta.questao,
                    peso=pergunta.peso,
                    fk_Evento_Pergunta=pergunta.fk_Evento_Pergunta,
                )
                for pergunta in perguntas
            ]
            return pergunta_dto
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter perguntas',
                f'Erro ao obter perguntas: Detalhes: {sqla_error}',
            )
            return []

    def get_perguntas_filtradas(
        self, busca: str, filtro: str
    ) -> list[PerguntaDTO]:
        try:
            perguntas = (
                self.session.query(PerguntaVO)
                .filter(text(f'{filtro} like :busca'))
                .params(busca=f'%{busca}%')
                .all()
            )

            perguntas_dto = [
                PerguntaDTO(
                    id_pergunta=pergunta.id_pergunta,
                    questao=pergunta.questao,
                    peso=pergunta.peso,
                    fk_Evento_Pergunta=pergunta.fk_Evento_Pergunta,
                )
                for pergunta in perguntas
            ]
            return perguntas_dto

        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter perguntas',
                f'Erro ao obter perguntas: Detalhes: {sqla_error}',
            )
            return []

    def get_perguntas_pelo_id_evento(
        self, id_evento: int
    ) -> list[PerguntaDTO]:
        try:
            with self.session as session:
                perguntas = (
                    session.query(PerguntaVO)
                    .filter_by(fk_Evento_Pergunta=id_evento)
                    .all()
                )
            perguntas_dto = [
                PerguntaDTO(
                    id_pergunta=pergunta.id_pergunta,
                    questao=pergunta.questao,
                    peso=pergunta.peso,
                    fk_Evento_Pergunta=pergunta.fk_Evento_Pergunta,
                )
                for pergunta in perguntas
            ]
            return perguntas_dto

        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter perguntas',
                f'Erro ao obter perguntas: Detalhes: {sqla_error}',
            )
            return []

    def get_columns_names(self) -> list:
        return [c.name for c in PerguntaVO.__table__.columns]
