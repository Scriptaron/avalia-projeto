import re
from datetime import date, datetime
from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.dto.EventoDTO import EventoDTO
from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUIManuEvento(ctk.CTkToplevel):
    def __init__(self, root, usuario_logado: int):
        super().__init__()
        self.root = root
        self.usuario_logado = usuario_logado
        self.banner_selecionado = None
        self.evento_selecionado = None
        self.services_factory = ServicesFactory()

        self._load_ui()
        self._load_controller()

    def _load_ui(self) -> None:
        self._configure_janela()
        self._load_widgets()

    def _load_controller(self) -> None:
        self.carregar_tabela()
        self.hover_campo()

        self.entry_inicio.bind('<KeyRelease>', self.formatar_data)
        self.entry_fim.bind('<KeyRelease>', self.formatar_data)

        self.entry_busca.bind('<KeyRelease>', self.on_search)

    def carregar_tabela(self, busca: str = '', filtro: str = '') -> None:
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        evento_service = self.services_factory.get_evento_services()

        eventos = (
            evento_service.pesquisar_eventos(busca, filtro)
            if busca
            else evento_service.listar_eventos()
        )

        todos_banners = []
        todos_estados = []
        todos_label_extras = []

        for evento in eventos:
            estado = {'expandido': False}

            banner = ctk.CTkFrame(
                self.frame_tabela,
                height=100,
                corner_radius=10,
            )
            banner.pack(pady=10, padx=5, fill='x', expand=True)

            texto_resumo = f'Nome: {evento.nome}\nData Inicio: {evento.data_inicio}\nData Termino: {evento.data_fim}'
            label_resumo = ctk.CTkLabel(
                banner,
                text=texto_resumo,
                font=('Segoe UI', 15),
                wraplength=350,
            )
            label_resumo.pack(side='top', padx=5, pady=5)

            label_extra = ctk.CTkLabel(
                banner,
                text=f'Descrição: {evento.descricao}',
                font=('Segoe UI', 14),
                wraplength=350,
                justify='left',
            )

            banner.bind(
                '<Button-1>',
                lambda event, f=banner, s=estado, l=label_extra, e=evento: self.expandir_tabela(
                    f,
                    s,
                    l,
                    e,
                    todos_banners,
                    todos_estados,
                    todos_label_extras,
                ),
            )

            todos_banners.append(banner)
            todos_estados.append(estado)
            todos_label_extras.append(label_extra)

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

        self.entry_fim.bind(
            '<FocusIn>',
            lambda event: self.alterar_cor_campo('termino', '#F27F1B'),
        )

        self.entry_fim.bind(
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

    def alterar_cor_campo(self, campo: str, cor: str) -> None:
        match campo.lower():
            case 'nome':
                self.label_nome.configure(text_color=cor)
                self.linha_nome.configure(fg_color=cor)

            case 'inicio':
                self.label_inicio.configure(text_color=cor)
                self.linha_inicio.configure(fg_color=cor)

            case 'termino':
                self.label_fim.configure(text_color=cor)
                self.linha_fim.configure(fg_color=cor)

            case 'descricao':
                self.label_descricao.configure(text_color=cor)

    def expandir_tabela(
        self,
        banner,
        estado,
        label_extra,
        evento,
        todos_banners,
        todos_estados,
        todos_label_extras,
    ):
        if not estado['expandido']:
            for i, b in enumerate(todos_banners):
                if todos_estados[i]['expandido']:
                    todos_label_extras[i].pack_forget()
                    todos_estados[i]['expandido'] = False

            label_extra.pack(side='top', padx=5, pady=5)
            estado['expandido'] = True

            self.banner_selecionado = banner
            self.evento_selecionado = evento

            self.preencher_dados_selecionados(evento)
        else:
            label_extra.pack_forget()
            estado['expandido'] = False

            self.banner_selecionado = None
            self.evento_selecionado = None

    def listar_colunas(self) -> None:
        return (
            self.services_factory.get_evento_services().listar_nomes_colunas()[
                1:
            ]
        )

    def alterar_evento(self) -> None:
        id_evento = int(self.evento_selecionado.id_evento)
        nome = self.entry_nome.get().strip()
        data_inicio = datetime.strptime(
            self.entry_inicio.get().strip(), '%d/%m/%Y'
        ).date()
        data_fim = datetime.strptime(
            self.entry_fim.get().strip(), '%d/%m/%Y'
        ).date()
        descricao = self.textbox_descricao.get('1.0', ctk.END).strip()

        evento_dto = EventoDTO(
            id_evento=id_evento,
            nome=nome,
            data_inicio=data_inicio,
            data_fim=data_fim,
            descricao=descricao,
            fk_administrador=self.usuario_logado,
        )

        self.services_factory.get_evento_services().alterar_evento(evento_dto)

        self.carregar_tabela()
        self.limpar_campos()

    def deletar_evento(self) -> None:
        try:
            id_evento = self.evento_selecionado.id_evento

            self.services_factory.get_evento_services().deletar_evento(
                id_evento
            )
            self.carregar_tabela()
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror(
                'Erro ao deletar evento',
                f'Erro ao deletar evento: Detalhes: {e}',
            )

    def limpar_campos(self) -> None:
        self.entry_nome.configure(state='normal')
        self.entry_nome.delete(0, 'end')

        self.entry_inicio.configure(state='normal')
        self.entry_inicio.delete(0, 'end')

        self.entry_fim.configure(state='normal')
        self.entry_fim.delete(0, 'end')

        self.textbox_descricao.configure(state='normal')
        self.textbox_descricao.delete('1.0', ctk.END)

    def preencher_dados_selecionados(self, evento_selecionado) -> None:
        self.entry_nome.configure(state='normal')
        self.entry_nome.delete(0, 'end')
        self.entry_nome.insert(0, self.evento_selecionado.nome)

        data_inicio_formatada = self.evento_selecionado.data_inicio.strftime(
            '%d/%m/%Y'
        )

        self.entry_inicio.configure(state='normal')
        self.entry_inicio.delete(0, 'end')
        self.entry_inicio.insert(0, data_inicio_formatada)

        data_termino_formatada = (
            evento_selecionado.data_fim.strftime('%d/%m/%Y')
            if evento_selecionado.data_fim
            else ''
        )

        self.entry_fim.configure(state='normal')
        self.entry_fim.delete(0, 'end')
        self.entry_fim.insert(0, data_termino_formatada)

        self.textbox_descricao.configure(state='normal')
        self.textbox_descricao.delete('1.0', ctk.END)
        self.textbox_descricao.insert('1.0', self.evento_selecionado.descricao)

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

    def on_search(self, event=None) -> None:
        busca = self.entry_busca.get().lower()
        filtro = self.combobox_colunas.get().lower()
        self.carregar_tabela(busca, filtro)

    def _configure_janela(self) -> None:
        self.title('Manutenção de Eventos')
        self.geometry('800x600')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self) -> None:
        self._criar_frames()
        self._configure_campo()
        self._configure_tabela()

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', expand=True)

        self.frame_campo = ctk.CTkFrame(self.frame_bg, fg_color='#003f7b')
        self.frame_campo.pack(fill='both', expand=True, side='left')

        self.frame_separador = ctk.CTkFrame(
            self.frame_bg, fg_color='#FFFFFF', width=7
        )
        self.frame_separador.pack(fill='y', side='left')

        self.frame_busca = ctk.CTkFrame(
            self.frame_bg, fg_color='#003f7b', height=120
        )
        self.frame_busca.pack(fill='both', side='top')

        self.frame_tabela = ctk.CTkScrollableFrame(
            self.frame_bg,
            scrollbar_button_color='#F27F1B',
            scrollbar_button_hover_color='#F25C05',
            fg_color='#003f7b',
        )
        self.frame_tabela.pack(fill='both', expand=True, side='right')

    def _configure_campo(self) -> None:
        self._criar_campo_nome()
        self._criar_campo_data()
        self._criar_campo_descricao()
        self._criar_campo_botoes()

    def _criar_campo_nome(self) -> None:
        self.label_nome = ctk.CTkLabel(
            self.frame_campo,
            text='Nome',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_nome.place(x=25, y=25)

        self.entry_nome = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text_color='#FFFFFF',
            width=260,
            height=40,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_nome.place(x=90, y=20)

        self.linha_nome = ctk.CTkFrame(
            self.frame_campo, fg_color='#FFFFFF', height=4, width=330
        )
        self.linha_nome.place(x=25, y=70)

    def _criar_campo_data(self) -> None:
        ctk.CTkLabel(
            self.frame_campo,
            text='Data',
            text_color='#FFFFFF',
            font=('Segoe UI', 20, 'bold'),
        ).place(x=170, y=80)

        self.label_inicio = ctk.CTkLabel(
            self.frame_campo,
            text='Inicio',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_inicio.place(x=60, y=110)

        self.entry_inicio = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text='dd/mm/yyyy',
            width=120,
            height=30,
            font=('Segoe UI', 17, 'bold'),
        )
        self.entry_inicio.place(x=25, y=150)

        self.linha_inicio = ctk.CTkFrame(
            self.frame_campo, fg_color='#FFFFFF', height=4, width=120
        )
        self.linha_inicio.place(x=25, y=190)

        self.label_fim = ctk.CTkLabel(
            self.frame_campo,
            text='Fim',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_fim.place(x=295, y=110)

        self.entry_fim = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text='dd/mm/yyyy',
            width=120,
            height=30,
            font=('Segoe UI', 17, 'bold'),
        )
        self.entry_fim.place(x=250, y=150)

        self.linha_fim = ctk.CTkFrame(
            self.frame_campo, fg_color='#FFFFFF', height=4, width=120
        )
        self.linha_fim.place(x=250, y=190)

    def _criar_campo_descricao(self) -> None:
        self.label_descricao = ctk.CTkLabel(
            self.frame_campo,
            text='Descrição',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_descricao.place(x=150, y=225)

        self.textbox_descricao = ctk.CTkTextbox(
            self.frame_campo,
            width=350,
            height=200,
            font=('Segoe UI', 16, 'bold'),
        )
        self.textbox_descricao.place(x=20, y=260)

    def _criar_campo_botoes(self) -> None:
        self.btn_alterar = ctk.CTkButton(
            self.frame_campo,
            font=('Segoe UI', 16, 'bold'),
            text='Alterar',
            width=140,
            height=45,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.alterar_evento,
        )
        self.btn_alterar.place(x=30, y=500)

        self.btn_excluir = ctk.CTkButton(
            self.frame_campo,
            font=('Segoe UI', 16, 'bold'),
            text='Excluir',
            width=140,
            height=45,
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.deletar_evento,
        )
        self.btn_excluir.place(x=230, y=500)

    def _configure_tabela(self) -> None:
        self._criar_campo_busca()

    def _criar_campo_busca(self) -> None:
        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text='Busca',
            width=380,
            height=40,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_busca.place(x=10, y=20)

        self.combobox_colunas = ctk.CTkComboBox(
            self.frame_busca,
            values=self.listar_colunas(),
            font=('Segoe UI', 16, 'bold'),
            button_color='#F27F1B',
            button_hover_color='#F25C05',
        )
        self.combobox_colunas.place(x=250, y=70)
