from tkinter import messagebox

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from avalia_projeto.dto.ProjetoDTO import ProjetoDTO
from avalia_projeto.model.EventoVO import EventoVO
from avalia_projeto.model.ProjetoVO import ProjetoVO


class ProjetoDAO:
    def __init__(self, session: sessionmaker) -> None:
        self.session = session

    def criar_projeto(self, novo_projeto: ProjetoDTO) -> None:
        try:
            novo_projeto = ProjetoVO(
                nome_projeto=novo_projeto.nome_projeto,
                integrantes=novo_projeto.integrantes,
                descricao_projeto=novo_projeto.descricao_projeto,
                fk_Evento_Projeto=novo_projeto.fk_Evento_Projeto,
            )
            self.session.add(novo_projeto)
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao criar projeto',
                f'Erro ao criar projeto: Detalhes: {sqla_error}',
            )

    def alterar_projeto(self, projeto: ProjetoDTO):
        try:
            self.session.query(ProjetoVO).filter_by(
                id_projeto=projeto.id_projeto
            ).update(
                {
                    'nome_projeto': projeto.nome_projeto,
                    'integrantes': projeto.integrantes,
                    'descricao_projeto': projeto.descricao_projeto,
                    'fk_Evento_Projeto': projeto.fk_Evento_Projeto,
                }
            )
            self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao alterar projeto',
                f'Erro ao alterar projeto: Detalhes: {sqla_error}',
            )

    def deletar_projeto(self, id_projeto: int) -> None:
        try:
            projeto = self.session.query(ProjetoVO).get(id_projeto)
            if projeto:
                self.session.delete(projeto)
                self.session.commit()
        except SQLAlchemyError as sqla_error:
            self.session.rollback()
            messagebox.showerror(
                'Erro ao deletar projeto',
                f'Erro ao deletar projeto: Detalhes: {sqla_error}',
            )

    def get_projetos(self) -> list[ProjetoDTO]:
        try:
            projetos = self.session.query(ProjetoVO).all()

            projeto_dto = [
                ProjetoDTO(
                    id_projeto=projeto.id_projeto,
                    nome_projeto=projeto.nome_projeto,
                    integrantes=projeto.integrantes,
                    descricao_projeto=projeto.descricao_projeto,
                    fk_Evento_Projeto=projeto.fk_Evento_Projeto,
                )
                for projeto in projetos
            ]
            return projeto_dto
        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter projetos',
                f'Erro ao obter projetos: Detalhes: {sqla_error}',
            )
            return []

    def get_projetos_filtrados(
        self, busca: str, filtro: str
    ) -> list[ProjetoDTO]:
        try:
            projetos = (
                self.session.query(ProjetoVO)
                .filter(text(f'{filtro} like :busca'))
                .params(busca=f'%{busca}%')
                .all()
            )

            projetos_dto = [
                ProjetoDTO(
                    id_projeto=projeto.id_projeto,
                    nome_projeto=projeto.nome_projeto,
                    descricao_projeto=projeto.descricao_projeto,
                    fk_Evento_Projeto=projeto.fk_Evento_Projeto,
                )
                for projeto in projetos
            ]
            return projetos_dto

        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter projetos',
                f'Erro ao obter projetos: Detalhes: {sqla_error}',
            )
            return []

    def get_evento_pelo_nome(self, busca: str) -> list[ProjetoDTO]:
        projetos = (
            self.session.query(ProjetoVO)
            .join(EventoVO)
            .filter(EventoVO.nome.ilike(f'%{busca}%'))
            .all()
        )
        return projetos

    def get_projetos_pelo_id_evento(self, id_evento: int) -> list[ProjetoDTO]:
        try:
            with self.session as session:
                projetos = (
                    session.query(ProjetoVO)
                    .join(EventoVO)
                    .filter(EventoVO.id_evento == id_evento)
                    .all()
                )
            return projetos

        except SQLAlchemyError as sqla_error:
            messagebox.showerror(
                'Erro ao obter projetos',
                f'Erro ao obter projetos: Detalhes: {sqla_error}',
            )
            return []

    def get_columns_names(self) -> list:
        return [c.name for c in ProjetoVO.__table__.columns]
