from base64 import b64encode
from tkinter import messagebox

from bcrypt import gensalt, hashpw

from avalia_projeto.dao.UsuarioDAO import UsuarioDAO
from avalia_projeto.dto.UsuarioDTO import UsuarioDTO


class UsuarioServices:
    def __init__(self, usuario_dao: UsuarioDAO) -> None:
        self.usuario_dao = usuario_dao

    def autenticar_usuario(
        self, login: str, senha: str, perfil: int
    ) -> UsuarioDTO:
        try:
            usuario_dto = self.usuario_dao.autenticar(
                login=login, senha=senha, perfil=perfil
            )
            return usuario_dto if usuario_dto else None
        except Exception as e:
            messagebox.showerror(
                'Erro ao autenticar', f'Erro ao autenticar: {e}'
            )

    def criar_usuario(
        self, nome: str, login: str, senha: str, perfil: int
    ) -> None:
        try:
            if not all([nome, login, senha, perfil]):
                raise ValueError('Todos os campos são obrigatórios')

            hash_senha = hashpw(senha.encode('utf-8'), gensalt())
            hash_senha_str = b64encode(hash_senha).decode('utf-8')

            usuario_dto = UsuarioDTO(
                nome_usuario=nome,
                login=login,
                senha=hash_senha_str,
                fk_Perfil_Usuario=perfil,
            )

            self.usuario_dao.criar_usuario(usuario_dto)

        except ValueError as ve:
            messagebox.showerror(
                'Erro de validação',
                f'Erro de validação: {ve}',
            )
        except Exception as e:
            messagebox.showerror(
                'Erro ao criar o usuário',
                f'Erro ao criar o usuário: {e}',
            )

    def alterar_usuario(
        self, usuario_dto: UsuarioDTO, usuario_logado: int
    ) -> None:
        if usuario_dto.id_usuario == usuario_logado:
            messagebox.showerror(
                'Erro ao alterar usuario',
                'Nao é possivel alterar o proprio usuario',
            )
        else:
            hash_senha = hashpw(usuario_dto.senha.encode('utf-8'), gensalt())
            hash_senha_str = b64encode(hash_senha).decode('utf-8')
            usuario_dto.senha = hash_senha_str

            self.usuario_dao.alterar_usuario(usuario_dto)

    def deletar_usuario(self, id_usuario: int, usuario_logado: int) -> None:
        try:
            if id_usuario == usuario_logado:
                messagebox.showerror(
                    'Erro ao deletar usuario',
                    'Nao é possivel deletar o proprio usuario',
                )
            else:
                self.usuario_dao.deletar_usuario(id_usuario)
        except Exception as e:
            messagebox.showerror(
                'Erro ao deletar o usuário',
                f'Erro ao deletar o usuário: {e}',
            )

    def pesquisar_usuarios(self, busca: str, filtro: str):

        if filtro not in self.listar_nomes_colunas():
            return []

        usuarios = self.usuario_dao.get_usuarios_filtrados(busca, filtro)
        return usuarios

    def pesquisar_pelo_perfil(self, busca: str) -> list[UsuarioDTO]:
        return self.usuario_dao.get_usuarios_pelo_perfil(busca)

    def listar_usuarios(self) -> list[UsuarioDTO]:
        return self.usuario_dao.get_usuarios()

    def listar_nomes_colunas(self) -> list[str]:
        return self.usuario_dao.get_column_names()
