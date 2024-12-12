from tkinter import messagebox
from tkinter.ttk import Treeview

import customtkinter as ctk

from avalia_projeto.dto.UsuarioDTO import UsuarioDTO
from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUIManuUsuario(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int):
        super().__init__()
        self.root = root
        self.usuario_logado = usuario_logado
        self.services_factory = ServicesFactory()

        self._load_ui()
        self._load_controller()

    def _load_ui(self):
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self):
        self.carregar_perfil()
        self.carregar_tabela()

        self.entry_busca.bind('<KeyRelease>', self.on_search)
        self.tree.bind('<<TreeviewSelect>>', self.on_treeview_select)

    def alterar_usuario(self) -> None:
        id_usuario = int(self.tree.item(self.tree.selection())['values'][-1])
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        perfil = self.perfis[self.combobox_perfil.get()]

        usuario_dto = UsuarioDTO(
            id_usuario=id_usuario,
            nome_usuario=nome,
            login=login,
            senha=senha,
            fk_Perfil_Usuario=perfil,
        )

        self.services_factory.get_usuario_services().alterar_usuario(
            usuario_dto, self.usuario_logado
        )

        self.carregar_tabela()
        self.limpar_campos()
        self.carregar_perfil()

    def deletar_usuario(self) -> None:
        try:
            id_usuario = int(
                self.tree.item(self.tree.selection())['values'][-1]
            )

            perfil = self.perfis[
                self.tree.item(self.tree.selection())['values'][2]
            ]

            if perfil:
                resposta = messagebox.askquestion(
                    'Atenção',
                    'Tem certeza que deseja deletar o usuário?',
                )

            if resposta == 'yes':
                self.services_factory.get_usuario_services().deletar_usuario(
                    id_usuario, self.usuario_logado
                )
                self.carregar_tabela()
                self.limpar_campos()
                self.carregar_perfil()

        except IndexError:
            messagebox.showwarning(
                'Seleção Inválida',
                'Por favor, selecione um usuário para deletar.',
            )
        except Exception as e:
            messagebox.showerror(
                'Erro', f'Erro ao tentar deletar o usuário: {e}'
            )

    def carregar_tabela(self, busca: str = '', filtro: str = '') -> None:
        self.tree.delete(*self.tree.get_children())

        if busca:
            if filtro == 'fk_Perfil_Usuario':
                usuarios = self.services_factory.get_usuario_services().pesquisar_pelo_perfil(
                    busca
                )
            else:
                usuarios = self.services_factory.get_usuario_services().pesquisar_usuarios(
                    busca=busca,
                    filtro='nome_usuario' if filtro == 'nome' else filtro,
                )
        else:
            usuarios = (
                self.services_factory.get_usuario_services().listar_usuarios()
            )

        perfis = {
            perfil.id_perfil: perfil.nome_perfil
            for perfil in self.services_factory.get_perfil_services().buscar_todos_perfis()
        }

        for usuario in usuarios:
            nome_perfil = perfis.get(usuario.fk_Perfil_Usuario, 'Desconhecido')
            self.tree.insert(
                '',
                'end',
                values=(
                    usuario.nome_usuario,
                    usuario.login,
                    nome_perfil.title(),
                    usuario.senha,
                    usuario.id_usuario,
                ),
            )

    def carregar_perfil(self) -> None:
        try:

            perfil_services = self.services_factory.get_perfil_services()

            perfis = perfil_services.buscar_todos_perfis()

            self.perfis = {
                perfil.nome_perfil.title(): perfil.id_perfil
                for perfil in perfis
            }

            self.combobox_perfil.configure(values=list(self.perfis.keys()))

        except Exception as e:
            messagebox.showerror(
                'Erro ao carregar perfis', f'Erro ao carregar perfis: {e}'
            )

    def listar_colunas(self) -> list:
        colunas = self.services_factory.get_usuario_services().listar_nomes_colunas()[
            1:
        ]

        colunas = [
            'Nome'
            if coluna == 'nome_usuario'
            else 'Perfil'
            if coluna == 'fk_Perfil_Usuario'
            else coluna.title()
            for coluna in colunas
            if coluna != 'senha'
        ]

        return colunas

    def limpar_campos(self) -> None:
        self.entry_nome.configure(state='normal')
        self.entry_nome.delete(0, 'end')

        self.entry_login.configure(state='normal')
        self.entry_login.delete(0, 'end')

        self.entry_senha.configure(state='normal')
        self.entry_senha.delete(0, 'end')

        self.combobox_perfil.set(value=['Selecione'])

    def on_treeview_select(self, event=None) -> None:
        selected_item = self.tree.selection()
        if not selected_item:
            return

        values = self.tree.item(selected_item[0])['values']

        self.entry_nome.delete(0, 'end')
        self.entry_nome.insert(0, values[0])

        self.entry_login.delete(0, 'end')
        self.entry_login.insert(0, values[1])

        self.combobox_perfil.set(values[2])

    def on_search(self, event=None) -> None:
        busca = self.entry_busca.get()
        filtro = (
            self.combobox_colunas.get().lower()
            if self.combobox_colunas
            else ''
        )

        if filtro == 'perfil':
            filtro = 'fk_Perfil_Usuario'

        self.carregar_tabela(busca=busca, filtro=filtro)

    def _configure_janela(self):
        self.title('Manutenção de Usuários')
        self.geometry('800x600')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self):
        self._criar_frames()
        self._criar_campo_busca()
        self._criar_campo_tabela()
        self._criar_campo_entrada()
        self._criar_campo_botoes()

    def _criar_frames(self):
        self.frame_bg = ctk.CTkFrame(
            self, fg_color='#003f7b', bg_color='#003f7b'
        )
        self.frame_bg.pack(fill='both', expand=True)

        self.frame_busca = ctk.CTkFrame(
            self.frame_bg, fg_color='#003f7b', height=100
        )
        self.frame_busca.pack(side='top', fill='x')

        self.frame_tabela = ctk.CTkFrame(self.frame_bg, fg_color='#003f7b')
        self.frame_tabela.pack(fill='x', padx=10)

        self.frame_campo = ctk.CTkFrame(
            self.frame_bg, fg_color='#003f7b', height=150
        )
        self.frame_campo.pack(fill='x')

        self.frame_botao = ctk.CTkFrame(self.frame_bg, fg_color='#003f7b')
        self.frame_botao.pack(side='bottom', fill='x')

    def _criar_campo_busca(self) -> None:
        self.combobox_colunas = ctk.CTkComboBox(
            self.frame_busca,
            values=self.listar_colunas(),
            width=150,
            height=35,
            button_color='#F27F1B',
            button_hover_color='#F25C05',
        )
        self.combobox_colunas.place(x=40, y=30)

        self.entry_busca = ctk.CTkEntry(
            self.frame_busca, placeholder_text='Busca', width=400, height=35
        )
        self.entry_busca.place(x=220, y=30)

    def _criar_campo_tabela(self) -> None:
        columns = self.listar_colunas()
        self.tree = Treeview(
            self.frame_tabela, columns=columns, show='headings'
        )

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, width=40)

        self.scrollbar = ctk.CTkScrollbar(
            self.frame_tabela,
            orientation='vertical',
            command=self.tree.yview,
            button_color='#F27F1B',
            button_hover_color='#F25C05',
        )

        self.tree.configure(yscroll=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)

    def _criar_campo_entrada(self) -> None:
        self.label_nome = ctk.CTkLabel(
            self.frame_campo,
            text='Nome:',
            font=('Segoe UI', 16, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_nome.place(x=40, y=25)

        self.entry_nome = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text_color='#FFFFFF',
            width=255,
            height=40,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_nome.place(x=100, y=20)

        self.label_login = ctk.CTkLabel(
            self.frame_campo,
            text='Login:',
            font=('Segoe UI', 16, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_login.place(x=420, y=25)

        self.entry_login = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text_color='#FFFFFF',
            width=255,
            height=40,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_login.place(x=475, y=20)

        self.label_senha = ctk.CTkLabel(
            self.frame_campo,
            text='Senha:',
            font=('Segoe UI', 16, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_senha.place(x=40, y=85)

        self.entry_senha = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text_color='#FFFFFF',
            width=255,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            show='*',
        )
        self.entry_senha.place(x=100, y=80)

        self.label_perfil = ctk.CTkLabel(
            self.frame_campo,
            text='Perfil:',
            font=('Segoe UI', 16, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_perfil.place(x=420, y=85)

        self.combobox_perfil = ctk.CTkComboBox(
            self.frame_campo,
            values=['Selecione'],
            width=255,
            height=40,
            button_color='#F27F1B',
            button_hover_color='#F25C05',
        )
        self.combobox_perfil.place(x=475, y=80)

    def _criar_campo_botoes(self) -> None:
        self.btn_alterar = ctk.CTkButton(
            self.frame_botao,
            font=('Segoe UI', 16, 'bold'),
            text='Alterar',
            width=140,
            height=45,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.alterar_usuario,
        )
        self.btn_alterar.place(x=210, y=30)

        self.btn_excluir = ctk.CTkButton(
            self.frame_botao,
            font=('Segoe UI', 16, 'bold'),
            text='Excluir',
            width=140,
            height=45,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.deletar_usuario,
        )
        self.btn_excluir.place(x=460, y=30)
