import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory
from avalia_projeto.view.GUIAvaliacao import GUIAvaliacao


class GUIAvaliarProjeto(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int, id_evento: int):
        super().__init__()
        self.root = root
        self.usuario_logado = usuario_logado
        self.evento_selecionado = id_evento
        self.services_factory = ServicesFactory()

        self._load_ui()
        self._load_controller()

    def _load_ui(self) -> None:
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self) -> None:
        self.carregar_tabela()

    def entrar_projeto(self, projeto):

        self.withdraw()
        selecionar_projeto = GUIAvaliacao(
            root=self,
            usuario_logado=self.usuario_logado,
            id_projeto=projeto.id_projeto,
            id_evento=self.evento_selecionado,
        )
        selecionar_projeto.mainloop()

    def carregar_tabela(self) -> None:
        for widget in self.frame_grade.winfo_children():
            widget.destroy()

        projeto_services = self.services_factory.get_projeto_services()

        projetos = projeto_services.listar_projetos_pelo_id_evento(
            self.evento_selecionado
        )

        for projeto in projetos:
            projeto_frame = ctk.CTkFrame(
                self.frame_grade, fg_color='#ffffff', corner_radius=10
            )
            projeto_frame.pack(pady=15, padx=10, fill='x', expand=True)

            texto_resumo = f'Nome: {projeto.nome_projeto}\nIntegrantes: {projeto.integrantes}'
            label_resumo = ctk.CTkLabel(
                projeto_frame,
                text=texto_resumo,
                font=('Segoe UI', 15),
                wraplength=350,
            )
            label_resumo.pack(side='top', padx=5, pady=5)

            label_extra = ctk.CTkLabel(
                projeto_frame,
                text=f'Descrição: {projeto.descricao_projeto}',
                font=('Segoe UI', 14),
                wraplength=350,
                justify='left',
            )
            label_extra.pack(side='top', padx=5, pady=5)

            button_entrar = ctk.CTkButton(
                projeto_frame,
                text='Avaliar',
                font=('Segoe UI', 14),
                command=lambda p=projeto: self.entrar_projeto(p),
            )
            button_entrar.pack(side='bottom', pady=10)

    def _configure_janela(self) -> None:
        self.title('Projetos para Avaliação')
        self.geometry('700x500')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self) -> None:
        self._criar_frames()

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', expand=True)

        self.frame_grade = ctk.CTkScrollableFrame(
            self.frame_bg,
            scrollbar_button_color='#F27F1B',
            scrollbar_button_hover_color='#F25C05',
            fg_color='#003f7b',
        )
        self.frame_grade.pack(fill='both', expand=True, side='right')
