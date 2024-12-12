from avalia_projeto.persistence.database import SessionLocal


class DAOFactory:
    def __init__(self):
        self.session = SessionLocal()

    def get_avaliacao_dao(self):
        from avalia_projeto.services.AvaliacaoServices import AvaliacaoDAO

        return AvaliacaoDAO(self.session)

    def get_evento_dao(self):
        from avalia_projeto.services.EventoServices import EventoDAO

        return EventoDAO(self.session)

    def get_perfil_dao(self):
        from avalia_projeto.services.PerfilServices import PerfilDAO

        return PerfilDAO(self.session)

    def get_pergunta_dao(self):
        from avalia_projeto.services.PerguntaServices import PerguntaDAO

        return PerguntaDAO(self.session)

    def get_projeto_dao(self):
        from avalia_projeto.services.ProjetoServices import ProjetoDAO

        return ProjetoDAO(self.session)

    def get_usuario_dao(self):
        from avalia_projeto.services.UsuarioServices import UsuarioDAO

        return UsuarioDAO(self.session)
