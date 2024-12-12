import re
from datetime import datetime
from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.services.ServicesFactory import ServicesFactory
from avalia_projeto.util.validacao import Utils


class GUICadEvento(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int) -> None:
        super().__init__()
        self.avaliadores_listados: list[str] = []
        self.root = root
        self.usuario_logado = usuario_logado
        self.services_factory = ServicesFactory()

        self._load_ui()
        self._load_controller()

    def _load_ui(self):
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self):
        self.hover_campo()
        self.listar_avaliadores()
        self.entry_inicio.bind('<KeyRelease>', self.formatar_data)
        self.entry_termino.bind('<KeyRelease>', self.formatar_data)

    def cadastrar_evento(self) -> None:
        nome = self.entry_nome.get().strip()
        descricao = self.textbox_descricao.get('1.0', ctk.END).strip()
        lista_usuarios = (
            self.services_factory.get_usuario_services().listar_usuarios()
        )

        usuarios = {
            usuario.nome_usuario: usuario.id_usuario
            for usuario in lista_usuarios
        }

        avaliadores_id = [
            usuarios[usuario]
            for usuario in self.avaliadores_listados
            if usuario in usuarios
        ]

        try:
            data_inicial_input = self.entry_inicio.get().strip()
            data_final_input = self.entry_termino.get().strip()

            data_inicial = datetime.strptime(
                data_inicial_input, '%d/%m/%Y'
            ).date()
            data_final = (
                datetime.strptime(data_final_input, '%d/%m/%Y').date()
                if data_final_input
                else None
            )

            if not Utils.validar_datas(data_inicial_input, data_final_input):
                messagebox.showerror(
                    'Erro ao cadastrar evento',
                    'A data inicial deve ser maior ou igual à data atual e menor que a data final.',
                )
                return

            evento_services = self.services_factory.get_evento_services()

            evento_services.criar_evento(
                nome=nome,
                data_inicio=data_inicial,
                data_termino=data_final,
                descricao=descricao,
                avaliadores=avaliadores_id,
            )
            messagebox.showinfo('Sucesso', 'Evento cadastrado com sucesso!')

            self.limpar_campos()

        except Exception as e:
            messagebox.showerror(
                'Erro ao cadastrar evento', f'Erro ao cadastrar evento: {e}'
            )

    def adicionar_avaliador(self) -> None:
        avaliador_selecionado = self.combobox_avaliadores.get()

        if avaliador_selecionado not in self.avaliadores_listados:
            self.avaliadores_listados.append(avaliador_selecionado)
            self.label_lista_avaliador.configure(
                text=self.avaliadores_listados
            )

    def remover_avaliador(self) -> None:
        avaliador_selecionado = self.combobox_avaliadores.get()

        if avaliador_selecionado in self.avaliadores_listados:
            self.avaliadores_listados.remove(avaliador_selecionado)
            self.label_lista_avaliador.configure(
                text=self.avaliadores_listados
            )

    def adicionar_pergunta(self) -> None:
        ...

    def remover_pergunta(self) -> None:
        ...

    def listar_avaliadores(self) -> None:
        avaliadores = (
            self.services_factory.get_usuario_services().listar_usuarios()
        )

        self.combobox_avaliadores.configure(
            values=[avaliador.nome_usuario for avaliador in avaliadores]
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

        self.entry_inicio.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('inicio', '#F27F1B'),
        )

        self.entry_inicio.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('inicio', '#FFFFFF'),
        )

        self.entry_termino.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('termino', '#F27F1B'),
        )

        self.entry_termino.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('termino', '#FFFFFF'),
        )

        self.textbox_descricao.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('descricao', '#F27F1B'),
        )

        self.textbox_descricao.bind(
            '<FocusOut>',
            lambda event: self.alterar_cor_campo('descricao', '#FFFFFF'),
        )

    def formatar_data(self, event) -> None:
        entry_widget = event.widget
        texto = entry_widget.get()

        texto = re.sub(r'[^0-9]', '', texto)

        if len(texto) > 8:
            texto = texto[:8]

        if len(texto) >= 3:
            texto = texto[:2] + '/' + texto[2:]
        if len(texto) >= 6:
            texto = texto[:5] + '/' + texto[5:]
        entry_widget.delete(0, ctk.END)
        entry_widget.insert(0, texto)

    def alterar_cor_campo(self, campo: str, cor: str) -> None:
        match campo.lower():
            case 'nome':
                self.label_nome.configure(text_color=cor)
                self.linha_nome.configure(fg_color=cor)

            case 'inicio':
                self.label_inicio.configure(text_color=cor)
                self.linha_inicio.configure(fg_color=cor)

            case 'termino':
                self.label_termino.configure(text_color=cor)
                self.linha_termino.configure(fg_color=cor)

            case 'descricao':
                self.label_descricao.configure(text_color=cor)
                self.linha_descricao.configure(fg_color=cor)

    def limpar_campos(self) -> None:
        self.entry_nome.delete(0, ctk.END)
        self.entry_inicio.delete(0, ctk.END)
        self.entry_termino.delete(0, ctk.END)
        self.textbox_descricao.delete('1.0', ctk.END)

    def _configure_janela(self):
        self.title('Cadastro de Evento')
        self.geometry('700x480')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self):
        self._load_campo_evento()
        self._load_campo_avaliador()

    def _criar_frames(self):
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', side='left', expand=True)

        self.frame_evento = ctk.CTkFrame(self.frame_bg, fg_color='#003f7b')
        self.frame_evento.pack(fill='both', side='left', expand=True)

        self.frame_separador = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', width=7
        )
        self.frame_separador.pack(fill='y', side='left')

        self.frame_avaliador = ctk.CTkFrame(
            self.frame_bg, fg_color='#003f7b', width=80
        )
        self.frame_avaliador.pack(fill='both', side='right', expand=True)

    def _load_campo_evento(self):
        self._criar_frames()
        self._criar_campo_nome()
        self._criar_campo_data()
        self._criar_campo_descricao()
        self._criar_campo_botoes()

    def _load_campo_avaliador(self):
        self._criar_campo_avaliador()
        self._criar_campo_perguntas()

    def _criar_campo_nome(self):
        self.label_nome = ctk.CTkLabel(
            self.frame_evento,
            text='Nome',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_nome.place(x=30, y=25)

        self.entry_nome = ctk.CTkEntry(
            self.frame_evento,
            placeholder_text_color='#FFFFFF',
            width=285,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
        )
        self.entry_nome.place(x=90, y=25)

        self.linha_nome = ctk.CTkFrame(
            self.frame_evento, fg_color='#FFFFFF', height=4, width=345
        )
        self.linha_nome.place(x=30, y=60)

    def _criar_campo_data(self):
        ctk.CTkLabel(
            self.frame_evento,
            text='Data',
            text_color='#FFFFFF',
            font=('Segoe UI', 20, 'bold'),
        ).place(x=175, y=70)

        self.label_inicio = ctk.CTkLabel(
            self.frame_evento,
            text='Inicio',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_inicio.place(x=60, y=110)

        self.entry_inicio = ctk.CTkEntry(
            self.frame_evento,
            placeholder_text='dd/mm/yyyy',
            width=120,
            height=30,
            font=('Segoe UI', 17, 'bold'),
            border_width=0,
        )
        self.entry_inicio.place(x=25, y=150)

        self.linha_inicio = ctk.CTkFrame(
            self.frame_evento, fg_color='#FFFFFF', height=4, width=120
        )
        self.linha_inicio.place(x=25, y=190)

        self.label_termino = ctk.CTkLabel(
            self.frame_evento,
            text='Termino',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_termino.place(x=285, y=110)

        self.entry_termino = ctk.CTkEntry(
            self.frame_evento,
            placeholder_text='dd/mm/yyyy',
            width=120,
            height=30,
            font=('Segoe UI', 17, 'bold'),
            border_width=0,
        )
        self.entry_termino.place(x=260, y=150)

        self.linha_termino = ctk.CTkFrame(
            self.frame_evento, fg_color='#FFFFFF', height=4, width=120
        )
        self.linha_termino.place(x=260, y=190)

    def _criar_campo_descricao(self):
        self.label_descricao = ctk.CTkLabel(
            self.frame_evento,
            text='Descricao',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_descricao.place(x=160, y=230)

        self.textbox_descricao = ctk.CTkTextbox(
            self.frame_evento,
            width=360,
            height=100,
            font=('Segoe UI', 14, 'bold'),
            border_width=0,
        )
        self.textbox_descricao.place(x=25, y=270)

        self.linha_descricao = ctk.CTkFrame(
            self.frame_evento, fg_color='#FFFFFF', height=4, width=360
        )
        self.linha_descricao.place(x=25, y=380)

    def _criar_campo_botoes(self):
        self.btn_cadastrar = ctk.CTkButton(
            self.frame_evento,
            text='Cadastrar',
            width=200,
            height=40,
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.cadastrar_evento,
        )
        self.btn_cadastrar.place(x=105, y=420)

    def _criar_campo_avaliador(self):
        self.label_avaliador = ctk.CTkLabel(
            self.frame_avaliador,
            text='Avaliador',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_avaliador.place(x=100, y=10)

        self.btn_adicionar = ctk.CTkButton(
            self.frame_avaliador,
            text='Adicionar',
            width=100,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.adicionar_avaliador,
        )
        self.btn_adicionar.place(x=20, y=60)

        self.btn_remover = ctk.CTkButton(
            self.frame_avaliador,
            text='Remover',
            width=100,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.remover_avaliador,
        )
        self.btn_remover.place(x=170, y=60)

        self.combobox_avaliadores = ctk.CTkComboBox(
            self.frame_avaliador,
            values=['Selecione'],
            width=240,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
        )
        self.combobox_avaliadores.place(x=30, y=120)

        self.label_avaliadores_selecionados = ctk.CTkLabel(
            self.frame_avaliador,
            text=f'Avaliadores selecionados:',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_avaliadores_selecionados.place(x=10, y=180)

        self.label_lista_avaliador = ctk.CTkLabel(
            self.frame_avaliador,
            text='',
            text_color='#FFFFFF',
            font=('Segoe UI', 16, 'bold'),
            wraplength=300,
        )
        self.label_lista_avaliador.place(x=10, y=220)

    def _criar_campo_perguntas(self) -> None:
        self.label_perguntas = ctk.CTkLabel(
            self.frame_avaliador,
            text='Perguntas',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_perguntas.place(x=30, y=200)

        self.btn_adicionar_pergunta = ctk.CTkButton(
            self.frame_avaliador,
            text='Adicionar',
            width=100,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.adicionar_pergunta,
        )
        self.btn_adicionar_pergunta.place(x=30, y=250)

        self.btn_remover_pergunta = ctk.CTkButton(
            self.frame_avaliador,
            text='Remover',
            width=100,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.remover_pergunta,
        )
        self.btn_remover_pergunta.place(x=170, y=250)

        self.combobox_perguntas = ctk.CTkComboBox(
            self.frame_avaliador,
            values=['Selecione'],
            width=240,
            height=30,
            font=('Segoe UI', 16, 'bold'),
            border_width=0,
        )
        self.combobox_perguntas.place(x=30, y=310)

        self.label_perguntas_selecionadas = ctk.CTkLabel(
            self.frame_avaliador,
            text=f'Perguntas selecionadas:',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_perguntas_selecionadas.place(x=10, y=370)

        self.label_lista_perguntas = ctk.CTkLabel(
            self.frame_avaliador,
            text='',
            text_color='#FFFFFF',
            font=('Segoe UI', 16, 'bold'),
            wraplength=300
        )