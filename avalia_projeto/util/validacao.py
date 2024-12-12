from datetime import datetime


class Utils:
    @staticmethod
    def validar_datas(data_inicial, data_final=None):
        formato = '%d/%m/%Y'

        try:

            data_inicial = datetime.strptime(data_inicial, formato).date()

            data_atual = datetime.now().date()

            if data_inicial < data_atual:
                return False

            if data_final:
                data_final = datetime.strptime(data_final, formato).date()
                if data_final < data_inicial:
                    return False

            return True

        except ValueError:
            return False
