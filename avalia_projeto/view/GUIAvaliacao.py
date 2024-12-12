from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUIAvaliacao(ctk.CTkToplevel):
    def __init__(
        self, root, usuario_logado: int, id_projeto: int, id_evento: int
    ):
        super().__init__()
        self.root = root
        self.usuario_logado = usuario_logado
        self.id_projeto = id_projeto
        self.services_factory = ServicesFactory()

        self.perguntas_dto = self.services_factory.get_pergunta_services().listar_perguntas_pelo_id_evento(
            id_evento
        )

        self.respostas = {
            pergunta.questao: 0 for pergunta in self.perguntas_dto
        }
        self.perguntas = list(self.respostas.keys())
        self.pergunta_atual = 0

        self._load_ui()
        self._load_controller()

    def _load_ui(self) -> None:
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self) -> None:
        self.atualizar_frame_pergunta()

    def _configure_janela(self):
        self.title('Sistema de Avaliação')
        self.geometry('500x350')
        self.resizable(False, False)
        self.grab_set()

    def avaliar_projeto(self):
        pergunta_atual = self.perguntas[self.pergunta_atual]
        self.respostas[pergunta_atual] = (
            self.frame_pergunta.winfo_children()[1].cget('variable').get()
        )

        self.services_factory.get_avaliacao_services().avaliar_projeto(
            self.respostas, self.id_projeto
        )

    def atualizar_frame_pergunta(self):
        for widget in self.frame_pergunta.winfo_children():
            widget.destroy()

        pergunta = self.perguntas[self.pergunta_atual]
        label_pergunta = ctk.CTkLabel(
            self.frame_pergunta,
            text=f'{pergunta}?',
            font=('Segoe UI', 20, 'bold'),
            text_color='#FFFFFF',
        )
        label_pergunta.place(relx=0.5, rely=0.1, anchor='center')

        var_nota = ctk.IntVar(value=self.respostas[pergunta])
        botao_por_linha = 5
        espacamento_horizontal = 50
        espacamento_vertical = 50
        margem_inicial_x = 130
        margem_inicial_y = 80

        for i in range(1, 11):
            linha = (i - 1) // botao_por_linha
            coluna = (i - 1) % botao_por_linha
            btn = ctk.CTkRadioButton(
                self.frame_pergunta,
                text=str(i),
                variable=var_nota,
                value=i,
                text_color='#FFFFFF',
                font=('Segoe UI', 14),
            )
            btn.place(
                x=margem_inicial_x + coluna * espacamento_horizontal,
                y=margem_inicial_y + linha * espacamento_vertical,
            )

        self.atualizar_botoes_navegacao(var_nota)

    def atualizar_botoes_navegacao(self, var_nota):
        # Remove widgets antigos do frame_botoes
        for widget in self.frame_botoes_navegacao.winfo_children():
            widget.destroy()

        btn_anterior = ctk.CTkButton(
            self.frame_botoes_navegacao,
            text='Anterior',
            command=lambda: self.navegar_pergunta(-1, var_nota),
            width=100,
            height=40,
        )
        btn_anterior.pack(side='left', padx=10)

        btn_proxima = ctk.CTkButton(
            self.frame_botoes_navegacao,
            text='Próxima',
            command=lambda: self.navegar_pergunta(1, var_nota),
            width=100,
            height=40,
        )
        btn_proxima.pack(side='right', padx=10)

    def navegar_pergunta(self, direcao, var_nota):
        if 0 <= self.pergunta_atual + direcao < len(self.perguntas):
            pergunta_atual = self.perguntas[self.pergunta_atual]
            self.respostas[pergunta_atual] = var_nota.get()
            self.pergunta_atual += direcao
            self.atualizar_frame_pergunta()

    def _load_widgets(self) -> None:
        self._criar_frames()
        self._criar_campo_botao()

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(self, fg_color='#1C1C1C')
        self.frame_bg.pack(fill='both', expand=True)

        self.frame_pergunta = ctk.CTkFrame(self.frame_bg, fg_color='#1C1C1C')
        self.frame_pergunta.pack(fill='both')

        self.frame_botoes_navegacao = ctk.CTkFrame(
            self.frame_bg, fg_color='#1C1C1C'
        )
        self.frame_botoes_navegacao.pack()

        self.frame_botao_avaliar = ctk.CTkFrame(
            self.frame_bg, fg_color='#1C1C1C'
        )
        self.frame_botao_avaliar.pack()

    def _criar_campo_botao(self) -> None:
        self.btn_avaliar = ctk.CTkButton(
            self.frame_botao_avaliar,
            text='Avaliar',
            height=35,
            width=120,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            font=('Segoe UI', 16, 'bold'),
            command=self.avaliar_projeto,
        )
        self.btn_avaliar.place(x=50, y=30)


if __name__ == '__main__':
    app = GUIAvaliacao(root=ctk.CTk(), usuario_logado=1)
    app.mainloop()
