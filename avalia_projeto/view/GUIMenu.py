from os import path
from tkinter import Menu, messagebox

import customtkinter as ctk
from PIL import Image, UnidentifiedImageError

from avalia_projeto.view.GUIAvaliarEventos import GUIAvaliarEventos
from avalia_projeto.view.GUICadEvento import GUICadEvento
from avalia_projeto.view.GUICadPergunta import GUICadPergunta
from avalia_projeto.view.GUICadProjeto import GUICadProjeto
from avalia_projeto.view.GUICadUsuario import GUICadUsuario
from avalia_projeto.view.GUIManuEvento import GUIManuEvento
from avalia_projeto.view.GUIManuProjeto import GUIManuProjeto
from avalia_projeto.view.GUIManuUsuario import GUIManuUsuario


class GUIMenu(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int) -> None:
        super().__init__()
        self.root = root
        self.usuario_logado = usuario_logado

        self._load_ui()

    def abrir_avaliacao(self) -> None:
        menu_avaliacao = GUIAvaliarEventos(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_avaliacao.mainloop()

    def abrir_cadastro_usuario(self) -> None:
        menu_cad_usuario = GUICadUsuario(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_cad_usuario.mainloop()

    def abrir_manutencao_usuario(self) -> None:
        menu_manu_usuario = GUIManuUsuario(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_manu_usuario.mainloop()

    def abrir_cadastro_evento(self) -> None:
        menu_cad_evento = GUICadEvento(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_cad_evento.mainloop()

    def abrir_manutencao_evento(self) -> None:
        menu_manu_evento = GUIManuEvento(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_manu_evento.mainloop()

    def abrir_cadastro_projeto(self) -> None:
        menu_cad_projeto = GUICadProjeto(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_cad_projeto.mainloop()

    def abrir_manutencao_projeto(self) -> None:
        menu_manu_projeto = GUIManuProjeto(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_manu_projeto.mainloop()

    def abrir_cadastro_pergunta(self) -> None:
        menu_cad_pergunta = GUICadPergunta(
            root=self, usuario_logado=self.usuario_logado
        )
        menu_cad_pergunta.mainloop()

    def fechar_menu(self) -> None:
        self.destroy()
        self.root.deiconify()

    def _load_ui(self) -> None:
        self._configure_janela()
        self._load_widgets()

    def desabilitar_cadastro(self) -> None:
        self.menu_bar.entryconfig('Cadastrar', state= 'disabled')

    def desabilitar_manutencao(self) -> None:
        self.menu_bar.entryconfig('Manutenção', state= 'disabled')

    def desabilitar_relatorio(self) -> None:
        self.menu_bar.entryconfig('Relatórios', state= 'disabled')

    def _configure_janela(self) -> None:
        self.title('Tela de Menu')
        self.state('zoomed')

    def _load_widgets(self) -> None:
        self._load_imagens()
        self._criar_frames()
        self._criar_campo_bg()
        self._configure_menus()

    def _load_imagens(self) -> None:
        base_path = path.dirname(path.abspath(__file__))
        bg_path = path.join(base_path, '..', 'assets', 'img', 'senac_bg.png')

        try:
            self.img_bg = ctk.CTkImage(
                Image.open(bg_path),
                size=(self.winfo_screenwidth(), self.winfo_screenheight()),
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
        self.frame_bg = ctk.CTkFrame(self)
        self.frame_bg.pack(fill='both', expand=True)

    def _criar_campo_bg(self) -> None:
        self.label_bg = ctk.CTkLabel(self.frame_bg, image=self.img_bg, text='')
        self.label_bg.pack()

    def _configure_menus(self) -> None:
        self.menu_bar = Menu(self)
        self.config(menu=self.menu_bar)

        self._criar_menu_avaliacao()
        self._criar_menu_cadastrar()
        self._criar_menu_manutencao()
        self._criar_menu_relatorios()
        self._criar_menu_sair()

    def _criar_menu_avaliacao(self) -> None:
        self.menu_bar.add_cascade(
            label='Avaliação', command=self.abrir_avaliacao
        )

    def _criar_menu_cadastrar(self) -> None:
        cadastrar_menu = Menu(self.menu_bar, tearoff=0)
    
        evento_submenu = Menu(cadastrar_menu, tearoff=0)

        evento_submenu.add_cascade(
            label='Evento', command=self.abrir_cadastro_evento
        )

        evento_submenu.add_separator()

        evento_submenu.add_command(
            label='Perguntas'
        )
        evento_submenu.add_command(
            label='Avaliadores'
        )

        
        # Adicionando o submenu "Evento" ao menu "Cadastrar"
        cadastrar_menu.add_cascade(label='Evento', menu=evento_submenu)
        
        # Outras opções no menu "Cadastrar"
        cadastrar_menu.add_command(
            label='Projeto', command=self.abrir_cadastro_projeto
        )
        cadastrar_menu.add_command(
            label='Pergunta', command=self.abrir_cadastro_pergunta
        )
        cadastrar_menu.add_separator()
        cadastrar_menu.add_command(
            label='Usuario', command=self.abrir_cadastro_usuario
        )
        
        # Adicionar o menu "Cadastrar" na barra de menus principal
        self.menu_bar.add_cascade(label='Cadastrar', menu=cadastrar_menu)


    def _criar_menu_manutencao(self) -> None:
        manu_menu = Menu(self.menu_bar, tearoff=0)
        manu_menu.add_command(
            label='Eventos', command=self.abrir_manutencao_evento
        )
        manu_menu.add_command(
            label='Projetos', command=self.abrir_manutencao_projeto
        )
        manu_menu.add_command(label='Perguntas')
        manu_menu.add_separator()
        manu_menu.add_command(
            label='Usuarios', command=self.abrir_manutencao_usuario
        )
        self.menu_bar.add_cascade(label='Manutenção', menu=manu_menu)

    def _criar_menu_relatorios(self) -> None:
        self.menu_bar.add_cascade(label='Relatórios')

    def _criar_menu_sair(self) -> None:
        self.menu_bar.add_cascade(label='Sair', command=self.fechar_menu)
