from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUICadProjeto(ctk.CTkToplevel):
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
        self.carregar_eventos()
        self.hover_campo()

    def cadastrar_projeto(self) -> None:
        nome = self.entry_nome.get().strip()
        descricao = self.textbox_descricao.get('1.0', ctk.END).strip()
        integrantes = self.entry_integrantes.get().strip()
        evento_selecionado = self.combobox_evento.get()

        if evento_selecionado not in self.eventos:
            messagebox.showerror(
                'Erro ao cadastrar projeto', 'Evento inválido.'
            )
            return

        evento = self.eventos[evento_selecionado]

        try:
            self.services_factory.get_projeto_services().criar_projeto(
                nome=nome,
                descricao=descricao,
                integrantes=integrantes,
                fk_evento=evento,
            )

            messagebox.showinfo('Sucesso', 'Projeto cadastrado com sucesso!')

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

            self.combobox_evento.configure(values=list(self.eventos.keys()))

        except Exception as e:
            messagebox.showerror(
                'Erro ao carregar eventos', f'Erro ao carregar eventos: {e}'
            )

    def limpar_campos(self) -> None:
        self.entry_nome.delete(0, ctk.END)
        self.textbox_descricao.delete('1.0', ctk.END)
        self.combobox_evento.set(value=['Selecione'])
        self.entry_integrantes.delete(0, ctk.END)

    def hover_campo(self) -> None:
        self.entry_nome.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('nome', '#F27F1B'),
        )
        self.entry_nome.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('nome', '#FFFFFF'),
        )

        self.textbox_descricao.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('descricao', '#F27F1B'),
        )
        self.textbox_descricao.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('descricao', '#FFFFFF'),
        )

        self.combobox_evento.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('evento', '#F27F1B'),
        )
        self.combobox_evento.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('evento', '#FFFFFF'),
        )

    def alterar_cor_campo(self, campo: str, cor: str) -> None:
        match campo.lower():
            case 'nome':
                self.label_nome.configure(text_color=cor)
                self.linha_nome.configure(fg_color=cor)

            case 'descricao':
                self.label_descricao.configure(text_color=cor)
                self.linha_descricao.configure(fg_color=cor)

            case 'evento':
                self.label_evento.configure(text_color=cor)

    def _configure_janela(self) -> None:
        self.title('Cadastro de Projeto')
        self.geometry('420x540')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self) -> None:
        self._criar_frames()
        self._criar_campo_nome()
        self._criar_campo_descricao()
        self._criar_campo_integrantes()
        self._criar_campo_evento()
        self._criar_campo_botoes()

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', expand=True)

    def _criar_campo_nome(self) -> None:
        self.label_nome = ctk.CTkLabel(
            self.frame_bg,
            text='Nome',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_nome.place(x=30, y=25)

        self.entry_nome = ctk.CTkEntry(
            self.frame_bg,
            placeholder_text_color='#FFFFFF',
            width=285,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
        )
        self.entry_nome.place(x=90, y=25)

        self.linha_nome = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=345
        )
        self.linha_nome.place(x=30, y=60)

    def _criar_campo_descricao(self) -> None:
        self.label_descricao = ctk.CTkLabel(
            self.frame_bg,
            text='Descricao',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_descricao.place(x=160, y=80)

        self.textbox_descricao = ctk.CTkTextbox(
            self.frame_bg,
            width=350,
            height=130,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
        )
        self.textbox_descricao.place(x=30, y=110)

        self.linha_descricao = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', height=4, width=350
        )
        self.linha_descricao.place(x=30, y=250)

    def _criar_campo_integrantes(self) -> None:
        self.label_integrantes = ctk.CTkLabel(
            self.frame_bg,
            text='Integrantes',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_integrantes.place(x=160, y=260)

        self.entry_integrantes = ctk.CTkEntry(
            self.frame_bg,
            placeholder_text='Formato: Nome1, Nome2, Nome3',
            width=350,
            height=30,
            font=('Segoe UI', 14, 'bold'),
            border_width=0,
        )
        self.entry_integrantes.place(x=30, y=300)

    def _criar_campo_evento(self) -> None:
        self.label_evento = ctk.CTkLabel(
            self.frame_bg,
            text='Evento',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_evento.place(x=110, y=360)

        self.combobox_evento = ctk.CTkComboBox(
            self.frame_bg,
            values=['Selecione'],
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
            width=200,
        )
        self.combobox_evento.place(x=180, y=360)

    def _criar_campo_botoes(self):
        self.botao_criar = ctk.CTkButton(
            self.frame_bg,
            text='Criar',
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            width=200,
            height=40,
            command=self.cadastrar_projeto,
        )
        self.botao_criar.place(x=105, y=450)
