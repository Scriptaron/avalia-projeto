from avalia_projeto.dao.AvaliacaoDAO import AvaliacaoDAO
from avalia_projeto.dto.AvaliacaoDTO import AvaliacaoDTO


class AvaliacaoServices:
    def __init__(self, avaliacao_dao: AvaliacaoDAO):
        self.avaliacao_dao = avaliacao_dao

    def avaliar_projeto(self, notas: dict, id_projeto: int):
        total_peso = 0
        total_ponderado = 0

        for questao, nota in notas.items():
            peso = self.get_peso_questao(questao)

            total_ponderado += nota * peso
            total_peso += peso

        media_ponderada = (
            total_ponderado / total_peso if total_peso != 0 else 0
        )

        # Arredondando a média ponderada para o valor inteiro mais próximo
        media_ponderada = round(media_ponderada)

        avaliacao_dto = AvaliacaoDTO(
            nota=media_ponderada, fk_Projeto_Avaliacao=id_projeto
        )

        return self.avaliacao_dao.avaliar_projeto(avaliacao_dto)

    def get_peso_questao(self, questao: str) -> int:
        return self.avaliacao_dao.get_peso_pergunta(questao)
