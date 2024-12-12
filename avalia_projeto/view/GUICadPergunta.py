from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUICadPergunta(ctk.CTkToplevel):
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
        self.carregar_notas()
        self.carregar_eventos()

    def cadastrar_pergunta(self) -> None:
        questao = self.entry_questao.get()
        peso = self.combobox_peso.get()
        evento_selecionado = self.combobox_eventos.get()

        if evento_selecionado not in self.eventos:
            messagebox.showerror(
                'Erro ao cadastrar projeto', 'Evento inválido.'
            )
            return

        evento_selecionado = self.eventos[evento_selecionado]

        try:
            self.services_factory.get_pergunta_services().criar_pergunta(
                questao=questao,
                peso=peso,
                fk_evento=evento_selecionado,
            )

            messagebox.showinfo('Sucesso', 'Pergunta cadastrada com sucesso!')

            self.limpar_campos()
        except Exception as e:
            messagebox.showerror(
                'Erro ao cadastrar projeto', f'Erro ao cadastrar projeto: {e}'
            )

    def carregar_eventos(self) -> None:
        try:
            eventos = (
                self.services_factory.get_evento_services().listar_eventos()
            )

            self.eventos = {
                evento.nome_evento: evento.id_evento for evento in eventos
            }

            self.combobox_eventos.configure(values=list(self.eventos.keys()))

        except Exception as e:
            messagebox.showerror(
                'Erro ao carregar eventos', f'Erro ao carregar eventos: {e}'
            )

    def carregar_notas(self):
        self.combobox_peso.configure(
            values=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        )

    def limpar_campos(self) -> None:
        self.entry_questao.delete(0, ctk.END)
        self.combobox_peso.set(value=['Selecione'])
        self.combobox_eventos.set(value=['Selecione'])

    def _configure_janela(self):
        self.title('Cadastro de Pergunta')
        self.geometry('520x320')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self):
        self._criar_frames()
        self._configure_campo()

    def _criar_frames(self):
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', expand=True)

    def _configure_campo(self) -> None:
        self._criar_campo_pergunta()
        self._criar_campo_peso()
        self._criar_campo_evento()
        self._criar_campo_botao()

    def _criar_campo_pergunta(self) -> None:
        self.label_questao = ctk.CTkLabel(
            self.frame_bg,
            text='Questão',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_questao.place(x=30, y=25)

        self.entry_questao = ctk.CTkEntry(
            self.frame_bg,
            placeholder_text_color='#FFFFFF',
            width=440,
            height=30,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_questao.place(x=30, y=70)

        self.simbolo_pergunta = ctk.CTkLabel(
            self.frame_bg,
            text='?',
            text_color='#FFFFFF',
            font=('Segoe UI', 40, 'bold'),
        )
        self.simbolo_pergunta.place(x=480, y=55)

        self.linha_pertgunta = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=440
        )
        self.linha_pertgunta.place(x=30, y=110)

    def _criar_campo_peso(self) -> None:
        self.label_peso = ctk.CTkLabel(
            self.frame_bg,
            text='Peso',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_peso.place(x=30, y=150)

        self.combobox_peso = ctk.CTkComboBox(
            self.frame_bg,
            values=['Selecione'],
            font=('Segoe UI', 12, 'bold'),
            border_width=0,
            width=100,
            height=30,
        )
        self.combobox_peso.place(x=80, y=150)

        self.linha_peso = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=150
        )
        self.linha_peso.place(x=30, y=185)

    def _criar_campo_evento(self) -> None:
        self.label_evento = ctk.CTkLabel(
            self.frame_bg,
            text='Evento',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_evento.place(x=220, y=150)

        self.combobox_eventos = ctk.CTkComboBox(
            self.frame_bg,
            values=['Selecione'],
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            width=210,
            height=30,
        )
        self.combobox_eventos.place(x=290, y=150)

        self.linha_evento = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=280
        )
        self.linha_evento.place(x=220, y=185)

    def _criar_campo_botao(self) -> None:
        self.botao_cadastrar = ctk.CTkButton(
            self.frame_bg,
            text='Cadastrar',
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            width=150,
            height=40,
            command=self.cadastrar_pergunta,
        )
        self.botao_cadastrar.place(x=180, y=250)
