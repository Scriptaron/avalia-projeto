import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory
from avalia_projeto.view.GUIAvaliarProjeto import GUIAvaliarProjeto


class GUIAvaliarEventos(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int):
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
        self.carregar_tabela()

    def entrar_evento(self, evento):
        self.withdraw()
        selecionar_projeto = GUIAvaliarProjeto(
            root=self,
            usuario_logado=self.usuario_logado,
            id_evento=evento.id_evento,
        )
        selecionar_projeto.mainloop()

    def carregar_tabela(self) -> None:
        for widget in self.frame_grade.winfo_children():
            widget.destroy()

        evento_service = self.services_factory.get_evento_services()

        eventos = evento_service.listar_eventos_pelo_id_usuario(
            self.usuario_logado
        )

        for evento in eventos:
            evento_frame = ctk.CTkFrame(
                self.frame_grade, fg_color='#ffffff', corner_radius=10
            )
            evento_frame.pack(pady=15, padx=10, fill='x', expand=True)

            texto_resumo = f'Nome: {evento.nome_evento}\nData Inicio: {evento.data_inicio}\nData Termino: {evento.data_termino}'
            label_resumo = ctk.CTkLabel(
                evento_frame,
                text=texto_resumo,
                font=('Segoe UI', 15),
                wraplength=350,
            )
            label_resumo.pack(side='top', padx=5, pady=5)

            label_extra = ctk.CTkLabel(
                evento_frame,
                text=f'Descrição: {evento.descricao_evento}',
                font=('Segoe UI', 14),
                wraplength=350,
                justify='left',
            )
            label_extra.pack(side='top', padx=5, pady=5)

            button_entrar = ctk.CTkButton(
                evento_frame,
                text='Entrar',
                font=('Segoe UI', 14),
                command=lambda e=evento: self.entrar_evento(e),
            )
            button_entrar.pack(side='bottom', pady=10)

    def _configure_janela(self) -> None:
        self.title('Eventos para Avaliação')
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


if __name__ == '__main__':
    app = GUIAvaliarEventos(root=ctk.CTk(), usuario_logado=1)
    app.mainloop()
