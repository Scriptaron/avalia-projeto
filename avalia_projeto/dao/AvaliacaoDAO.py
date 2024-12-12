from tkinter import messagebox

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from avalia_projeto.dto.AvaliacaoDTO import AvaliacaoDTO
from avalia_projeto.model.AvaliacaoVO import AvaliacaoVO
from avalia_projeto.model.PerguntaVO import PerguntaVO


class AvaliacaoDAO:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def avaliar_projeto(self, avaliacao_dto: AvaliacaoDTO):
        try:
            avaliacao_vo = AvaliacaoVO(
                nota=avaliacao_dto.nota,
                fk_Projeto_Avaliacao=avaliacao_dto.fk_Projeto_Avaliacao,
            )
            self.session.add(avaliacao_vo)
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao avaliar projeto',
                f'Erro ao avaliar projeto: Detalhes: {sqla_error}',
            )

    def get_peso_pergunta(self, questao: str) -> int:
        try:
            pergunta = (
                self.session.query(PerguntaVO)
                .filter_by(questao=questao)
                .first()
            )
            return pergunta.peso
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter pergunta',
                f'Erro ao obter pergunta: Detalhes: {sqla_error}',
            )
