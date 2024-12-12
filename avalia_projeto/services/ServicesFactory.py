from avalia_projeto.dao.DAOFactory import DAOFactory
from avalia_projeto.services.AvaliacaoServices import AvaliacaoServices
from avalia_projeto.services.EventoServices import EventoServices
from avalia_projeto.services.PerfilServices import PerfilServices
from avalia_projeto.services.PerguntaServices import PerguntaServices
from avalia_projeto.services.ProjetoServices import ProjetoServices
from avalia_projeto.services.UsuarioServices import UsuarioServices


class ServicesFactory:
    def __init__(self) -> None:
        self.dao_factory = DAOFactory()

    def get_avaliacao_services(self) -> AvaliacaoServices:
        return AvaliacaoServices(self.dao_factory.get_avaliacao_dao())

    def get_evento_services(self) -> EventoServices:
        return EventoServices(self.dao_factory.get_evento_dao())

    def get_perfil_services(self) -> PerfilServices:
        return PerfilServices(self.dao_factory.get_perfil_dao())

    def get_pergunta_services(self) -> PerguntaServices:
        return PerguntaServices(self.dao_factory.get_pergunta_dao())

    def get_projeto_services(self) -> ProjetoServices:
        return ProjetoServices(self.dao_factory.get_projeto_dao())

    def get_usuario_services(self) -> UsuarioServices:
        return UsuarioServices(self.dao_factory.get_usuario_dao())
