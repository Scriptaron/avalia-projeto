from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUICadUsuario(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int) -> None:
        super().__init__()
        self.root = root
        self.usuario_logado = usuario_logado
        self.services_factory = ServicesFactory()

        self._load_ui()
        self._load_controller()

    def _load_ui(self) -> None:
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self) -> None:
        self.hover_campo()
        self.carregar_perfil()

    def cadastrar_usuario(self) -> None:
        nome = self.entry_nome.get().strip()
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        perfil = self.perfis[self.combobox_perfil.get()]

        try:
            usuario_services = self.services_factory.get_usuario_services()
            usuario_services.criar_usuario(nome, login, senha, perfil)

            messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso!')

            self.limpar_campos()

        except Exception as e:
            messagebox.showerror(
                'Erro ao cadastrar usuário', f'Erro ao cadastrar usuário: {e}'
            )

    def hover_campo(self) -> None:
        self.entry_nome.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('nome', '#F27F1B'),
        )
        self.entry_nome.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('nome', '#FFFFFF'),
        )

        self.entry_login.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('login', '#F27F1B'),
        )
        self.entry_login.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('login', '#FFFFFF'),
        )

        self.entry_senha.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('senha', '#F27F1B'),
        )
        self.entry_senha.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('senha', '#FFFFFF'),
        )

    def alterar_cor_campo(self, campo: str, cor: str) -> None:
        match campo.lower():
            case 'nome':
                self.label_nome.configure(text_color=cor)
                self.linha_div_nome.configure(fg_color=cor)

            case 'login':
                self.label_login.configure(text_color=cor)
                self.linha_div_login.configure(fg_color=cor)

            case 'senha':
                self.label_senha.configure(text_color=cor)
                self.linha_div_senha.configure(fg_color=cor)

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

    def limpar_campos(self) -> None:
        self.entry_nome.delete(0, 'end')
        self.entry_login.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.combobox_perfil.set(value=['Selecione'])

    def _configure_janela(self) -> None:
        self.title('Cadastro de Usuário')
        self.geometry('420x350')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self) -> None:
        self._criar_frames()
        self._criar_campo_nome()
        self._criar_campo_login()
        self._criar_campo_senha()
        self._criar_campo_perfil()
        self._criar_campo_botao()

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', expand=True)

    def _criar_campo_nome(self) -> None:
        self.label_nome = ctk.CTkLabel(
            self.frame_bg,
            text='Nome:',
            font=('Segoe UI', 18, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_nome.place(x=30, y=25)

        self.entry_nome = ctk.CTkEntry(
            self.frame_bg,
            placeholder_text_color='#FFFFFF',
            width=305,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            fg_color='#003f7b',
            text_color='#FFFFFF',
        )
        self.entry_nome.place(x=90, y=20)

        self.linha_div_nome = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=360
        )
        self.linha_div_nome.place(x=30, y=60)

    def _criar_campo_login(self) -> None:
        self.label_login = ctk.CTkLabel(
            self.frame_bg,
            text='Login:',
            font=('Segoe UI', 18, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_login.place(x=30, y=85)

        self.entry_login = ctk.CTkEntry(
            self.frame_bg,
            placeholder_text_color='#FFFFFF',
            width=305,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            fg_color='#003f7b',
            text_color='#FFFFFF',
        )
        self.entry_login.place(x=90, y=80)

        self.linha_div_login = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=360
        )
        self.linha_div_login.place(x=30, y=120)

    def _criar_campo_senha(self) -> None:
        self.label_senha = ctk.CTkLabel(
            self.frame_bg,
            text='Senha:',
            font=('Segoe UI', 18, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_senha.place(x=30, y=145)

        self.entry_senha = ctk.CTkEntry(
            self.frame_bg,
            placeholder_text_color='#FFFFFF',
            width=305,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            fg_color='#003f7b',
            text_color='#FFFFFF',
        )
        self.entry_senha.place(x=90, y=140)

        self.linha_div_senha = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=360
        )
        self.linha_div_senha.place(x=30, y=180)

    def _criar_campo_perfil(self) -> None:
        self.label_perfil = ctk.CTkLabel(
            self.frame_bg,
            text='Perfil:',
            font=('Segoe UI', 18, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_perfil.place(x=180, y=200)

        self.combobox_perfil = ctk.CTkComboBox(
            self.frame_bg,
            values=['Selecione'],
            button_color='#F27F1B',
            button_hover_color='#F25C05',
        )
        self.combobox_perfil.place(x=255, y=200)

    def _criar_campo_botao(self) -> None:
        self.btn_cadastrar = ctk.CTkButton(
            self.frame_bg,
            text='Cadastrar',
            height=35,
            width=120,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            font=('Segoe UI', 16, 'bold'),
            command=self.cadastrar_usuario,
        )
        self.btn_cadastrar.place(x=150, y=280)
