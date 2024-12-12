import customtkinter as ctk


class AvaliacaoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Sistema de Avaliação')
        self.geometry('600x400')
        self.configure(bg='#1C1C1C')

        # Lista de perguntas e controle de respostas
        self.perguntas = [
            'Qualidade do conteúdo?',
            'Clareza das explicações?',
            'Facilidade de navegação?',
            'Relevância do material?',
        ]
        self.respostas = [0] * len(
            self.perguntas
        )  # Inicializa as respostas com 0
        self.pergunta_atual = 0  # Pergunta que está sendo exibida

        # Frame principal
        self.frame_bg = ctk.CTkFrame(self)
        self.frame_bg.pack(fill='both', expand=True)

        # Inicializa a exibição da primeira pergunta
        self.atualizar_frame_pergunta()

    def atualizar_frame_pergunta(self):
        # Remove widgets antigos do frame
        for widget in self.frame_bg.winfo_children():
            widget.destroy()

        # Exibe a pergunta atual
        pergunta = self.perguntas[self.pergunta_atual]
        label_pergunta = ctk.CTkLabel(
            self.frame_bg,
            text=pergunta,
            font=('Segoe UI', 20, 'bold'),
            text_color='#FFFFFF',
        )
        label_pergunta.pack(pady=10)

        # Cria botões de nota (de 1 a 10)
        var_nota = ctk.IntVar(
            value=self.respostas[self.pergunta_atual]
        )  # Recupera a resposta atual
        for i in range(1, 11):
            btn = ctk.CTkRadioButton(
                self.frame_bg,
                text=str(i),
                variable=var_nota,
                value=i,
                text_color='#FFFFFF',
                font=('Segoe UI', 16, 'bold'),
            )
            btn.pack(side='left', padx=5)

        # Adiciona botões de navegação
        self.adicionar_botoes_navegacao(var_nota)

    def adicionar_botoes_navegacao(self, var_nota):
        btn_anterior = ctk.CTkButton(
            self.frame_bg,
            text='Anterior',
            command=lambda: self.navegar_pergunta(-1, var_nota),
            width=100,
            height=40,
        )
        btn_anterior.pack(side='left', padx=10)

        btn_proxima = ctk.CTkButton(
            self.frame_bg,
            text='Próxima',
            command=lambda: self.navegar_pergunta(1, var_nota),
            width=100,
            height=40,
        )
        btn_proxima.pack(side='right', padx=10)

    def navegar_pergunta(self, direcao, var_nota):
        if 0 <= self.pergunta_atual + direcao < len(self.perguntas):
            self.respostas[
                self.pergunta_atual
            ] = var_nota.get()  # Salva a resposta atual
            self.pergunta_atual += direcao
            self.atualizar_frame_pergunta()  # Atualiza a interface com a próxima/pergunta anterior


# Criando a instância da aplicação e iniciando a interface
if __name__ == '__main__':
    app = AvaliacaoApp()
    app.mainloop()
