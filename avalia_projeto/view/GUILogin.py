from os import path
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image, UnidentifiedImageError

from avalia_projeto.services.ServicesFactory import ServicesFactory
from avalia_projeto.view.GUIMenu import GUIMenu


class GUILogin(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.services_factory = ServicesFactory()

        self._load_ui()
        self._load_controller()

    def _load_ui(self) -> None:
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self) -> None:
        self.carregar_perfil()

    def abrir_menu(self, usuario_logado: int) -> None:
        self.withdraw()
        self.limpar_campos()
        menu_janela = GUIMenu(root=self, usuario_logado=usuario_logado)

        if usuario_logado != 1:
            menu_janela.desabilitar_cadastro()
            menu_janela.desabilitar_manutencao()
            menu_janela.desabilitar_relatorio()

        menu_janela.mainloop()

    def verificar_login(self) -> None:
        login = self.entry_login.get().strip()
        senha = self.entry_senha.get().strip()
        perfil = self.perfis[self.combobox_perfil.get()]

        try:
            usuario_dto = self.services_factory.get_usuario_services().autenticar_usuario(
                login=login, senha=senha, perfil=perfil
            )

            if usuario_dto:
                self.abrir_menu(usuario_dto.id_usuario)
            else:
                messagebox.showerror(
                    'Erro ao autenticar',
                    'Login, senha ou perfil invalidos',
                )

        except Exception as e:
            messagebox.showerror(
                'Erro ao verificar login', f'Erro ao verificar login: {e}'
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

    def limpar_campos(self) -> None:
        self.entry_login.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.combobox_perfil.set(value=['Selecione'])

    def toggle_senha(self, event=None) -> None:
        is_checked = (
            self.checkbox_mostrar_senha.cget('image') == self.img_checked
        )
        self.entry_senha.configure(show='' if is_checked else '*')
        self.checkbox_mostrar_senha.configure(
            image=self.img_unchecked if is_checked else self.img_checked
        )

    def get_posicao_central(self, largura: int, altura: int) -> str:
        largura_tela = self.winfo_screenwidth()
        altura_tela = self.winfo_screenheight()

        posx = (largura_tela - largura) // 2
        posy = (altura_tela - altura) // 2

        return f'{largura}x{altura}+{posx}+{posy}'

    def _configure_janela(self) -> None:
        self.title('Tela de Login')
        self.geometry(self.get_posicao_central(largura=330, altura=420))
        self.resizable(False, False)

    def _load_widgets(self) -> None:
        self._load_imagens()
        self._criar_frames()
        self._criar_campo_logo()
        self._criar_campo_login()
        self._criar_campo_senha()
        self._criar_campo_perfil()
        self._criar_campo_botao()

    def _load_imagens(self) -> None:
        base_path = path.dirname(path.abspath(__file__))

        logo_path = path.join(
            base_path, '..', 'assets', 'img', 'senac_logo.png'
        )

        checked_path = path.join(
            base_path, '..', 'assets', 'img', 'hide_pass.png'
        )

        unchecked_path = path.join(
            base_path, '..', 'assets', 'img', 'show_pass.png'
        )

        try:
            self.img_logo = ctk.CTkImage(
                dark_image=Image.open(logo_path), size=(240, 120)
            )
            self.img_checked = ctk.CTkImage(
                Image.open(checked_path), size=(30, 30)
            )
            self.img_unchecked = ctk.CTkImage(
                Image.open(unchecked_path), size=(30, 30)
            )

        except FileNotFoundError as fnfe:
            messagebox.showerror(
                'Erro ao carregar as imagens',
                f'Erro ao carregar as imagens: Arquivo nao encontrado. Detalhes: {fnfe}',
            )
        except UnidentifiedImageError as uie:
            messagebox.showerror(
                'Erro ao carregar as imagens',
                f'Erro ao carregar as imagens: O arquivo nao eh uma imagem valida. Detalhes: {uie}',
            )
        except Exception as e:
            messagebox.showerror(
                'Erro ao carregar as imagens',
                f'Erro ao carregar as imagens: Erro desconhecido. Detalhes: {e}',
            )

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(
            self, fg_color='#003f7b', bg_color='#003f7b'
        )
        self.frame_bg.pack(fill='both', expand=True)

        self.frame_top = ctk.CTkFrame(
            self.frame_bg, fg_color='#003f7b', height=125
        )
        self.frame_top.pack(fill='x')

        self.frame_mid = ctk.CTkFrame(self.frame_bg, fg_color='#003f7b')
        self.frame_mid.pack(fill='x')

        self.frame_bot = ctk.CTkFrame(self.frame_bg, fg_color='#003f7b')
        self.frame_bot.pack(fill='x')

    def _criar_campo_logo(self) -> None:
        label_logo = ctk.CTkLabel(self.frame_top, image=self.img_logo, text='')
        label_logo.place(x=50, y=10)

    def _criar_campo_login(self) -> None:
        self.entry_login = ctk.CTkEntry(
            self.frame_mid,
            placeholder_text='Login',
            width=250,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            fg_color='#003f7b',
            text_color='#FFFFFF',
            placeholder_text_color='#FFFFFF',
        )
        self.entry_login.place(x=40, y=20)

        ctk.CTkFrame(
            self.frame_mid, fg_color='#FFFFFF', height=4, width=250
        ).place(x=40, y=60)

    def _criar_campo_senha(self) -> None:
        self.entry_senha = ctk.CTkEntry(
            self.frame_mid,
            placeholder_text='Senha',
            width=220,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            fg_color='#003f7b',
            text_color='#FFFFFF',
            placeholder_text_color='#FFFFFF',
            show='*',
        )
        self.entry_senha.place(x=40, y=80)

        ctk.CTkFrame(
            self.frame_mid, height=4, width=250, fg_color='#FFFFFF'
        ).place(x=40, y=120)

        self.checkbox_mostrar_senha = ctk.CTkLabel(
            self.frame_mid, image=self.img_checked, text=''
        )
        self.checkbox_mostrar_senha.place(x=260, y=85)

        self.checkbox_mostrar_senha.bind('<Button-1>', self.toggle_senha)

    def _criar_campo_perfil(self) -> None:
        self.label_perfil = ctk.CTkLabel(
            self.frame_mid,
            text='Perfil:',
            font=('Segoe UI', 16, 'bold'),
            text_color='#FFFFFF',
        )
        self.label_perfil.place(x=45, y=140)

        self.combobox_perfil = ctk.CTkComboBox(
            self.frame_mid,
            values=['Selecione'],
            button_color='#F27F1B',
            button_hover_color='#F25C05',
        )
        self.combobox_perfil.place(x=120, y=140)

    def _criar_campo_botao(self) -> None:
        self.btn_entrar = ctk.CTkButton(
            self.frame_bot,
            text='Entrar',
            height=35,
            width=120,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            font=('Segoe UI', 16, 'bold'),
            command=self.verificar_login,
        )
        self.btn_entrar.place(x=105, y=30)
