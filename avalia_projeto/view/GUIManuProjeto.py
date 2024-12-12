from tkinter import messagebox

import customtkinter as ctk

from avalia_projeto.dto.ProjetoDTO import ProjetoDTO
from avalia_projeto.services.ServicesFactory import ServicesFactory


class GUIManuProjeto(ctk.CTkToplevel):
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
        self.carregar_tabela()
        self.hover_campo()

        self.entry_busca.bind('<KeyRelease>', self.on_search)

    def alterar_projeto(self) -> None:
        id_projeto = int(self.projeto_selecionado.id_projeto)
        nome = self.entry_nome.get().strip()
        descricao = self.textbox_descricao.get('1.0', ctk.END).strip()
        evento = self.eventos[self.combobox_evento.get()]

        projeto_dto = ProjetoDTO(
            id_projeto=id_projeto,
            nome=nome,
            descricao=descricao,
            fk_administrador=self.usuario_logado,
            fk_evento=evento,
        )

        self.services_factory.get_projeto_services().alterar_projeto(
            projeto_dto
        )

        self.carregar_tabela()
        self.limpar_campos()

    def deletar_projeto(self) -> None:
        try:
            id_projeto = self.projeto_selecionado.id_projeto

            self.services_factory.get_projeto_services().deletar_projeto(
                id_projeto
            )

            self.carregar_tabela()
            self.limpar_campos()
        except Exception as e:
            messagebox.showerror(
                'Erro ao deletar projeto',
                f'Erro ao deletar projeto: Detalhes: {e}',
            )

    def carregar_eventos(self) -> None:
        try:
            eventos = (
                self.services_factory.get_evento_services().listar_eventos()
            )

            self.eventos = {
                evento.nome: evento.id_evento for evento in eventos
            }

            self.combobox_evento.configure(values=list(self.eventos.keys()))

        except Exception as e:
            messagebox.showerror(
                'Erro ao carregar eventos', f'Erro ao carregar eventos: {e}'
            )

    def limpar_campos(self) -> None:
        self.entry_nome.configure(state='normal')
        self.entry_nome.delete(0, ctk.END)

        self.textbox_descricao.configure(state='normal')
        self.textbox_descricao.delete('1.0', ctk.END)

        self.combobox_evento.configure(state='normal')
        self.combobox_evento.set(value=['Selecione'])

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

    def carregar_tabela(self, busca: str = '', filtro: str = '') -> None:
        for widget in self.frame_tabela.winfo_children():
            widget.destroy()

        projeto_services = self.services_factory.get_projeto_services()

        if busca:
            if filtro == 'fk_evento':
                projetos = projeto_services.pesquisar_pelo_evento(busca)
            else:
                projetos = projeto_services.pesquisar_projetos(busca, filtro)
        else:
            projetos = projeto_services.listar_projetos()

        todos_banners = []
        todos_estados = []
        todos_label_extras = []

        for projeto in projetos:
            evento_nome = next(
                (
                    nome
                    for nome, id_evento in self.eventos.items()
                    if id_evento == projeto.fk_evento
                ),
                '',
            )
            estado = {'expandido': False}

            banner = ctk.CTkFrame(
                self.frame_tabela,
                height=100,
                corner_radius=10,
            )
            banner.pack(pady=10, padx=5, fill='x', expand=True)

            texto_resumo = f'Nome: {projeto.nome}\nEvento: {evento_nome}'
            label_resumo = ctk.CTkLabel(
                banner,
                text=texto_resumo,
                font=('Segoe UI', 15),
                wraplength=350,
            )
            label_resumo.pack(side='top', padx=5, pady=5)

            label_extra = ctk.CTkLabel(
                banner,
                text=f'Descrição: {projeto.descricao}',
                font=('Segoe UI', 14),
                wraplength=350,
                justify='left',
            )

            banner.bind(
                '<Button-1>',
                lambda event, f=banner, s=estado, l=label_extra, e=projeto: self.expandir_tabela(
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

    def expandir_tabela(
        self,
        banner,
        estado,
        label_extra,
        projeto,
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
            self.projeto_selecionado = projeto

            self.preencher_dados_selecionados(projeto)
        else:
            label_extra.pack_forget()
            estado['expandido'] = False

            self.banner_selecionado = None
            self.projeto_selecionado = None

    def preencher_dados_selecionados(self, projeto_selecionado) -> None:
        self.entry_nome.configure(state='normal')
        self.entry_nome.delete(0, 'end')
        self.entry_nome.insert(0, projeto_selecionado.nome)

        self.textbox_descricao.configure(state='normal')
        self.textbox_descricao.delete('1.0', 'end')
        self.textbox_descricao.insert('1.0', projeto_selecionado.descricao)

        evento = next(
            (
                nome
                for nome, id_evento in self.eventos.items()
                if id_evento == projeto_selecionado.fk_evento
            ),
            '',
        )

        self.combobox_evento.configure(state='normal')
        self.combobox_evento.set(evento)

    def listar_colunas(self) -> None:
        colunas = self.services_factory.get_projeto_services().listar_nomes_colunas()[
            1:
        ]

        colunas = [
            coluna for coluna in colunas if coluna != 'fk_administrador'
        ]

        return colunas

    def on_search(self, event=None) -> None:
        busca = self.entry_busca.get().lower()
        filtro = self.combobox_colunas.get().lower()
        self.carregar_tabela(busca, filtro)

    def _configure_janela(self) -> None:
        self.title('Manutenção de Projetos')
        self.geometry('700x500')
        self.resizable(False, False)
        self.grab_set()

    def _load_widgets(self) -> None:
        self._criar_frames()
        self._configure_campo()
        self._configure_tabela()

    def _criar_frames(self) -> None:
        self.frame_bg = ctk.CTkFrame(self, fg_color='#003f7b')
        self.frame_bg.pack(fill='both', expand=True)

        self.frame_campo = ctk.CTkFrame(
            self.frame_bg, fg_color='#003f7b', width=220
        )
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
        self._criar_campo_descricao()
        self._criar_campo_evento()
        self._criar_campo_botoes()

    def _criar_campo_nome(self) -> None:
        self.label_nome = ctk.CTkLabel(
            self.frame_campo,
            text='Nome',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_nome.place(x=20, y=25)

        self.entry_nome = ctk.CTkEntry(
            self.frame_campo,
            placeholder_text_color='#FFFFFF',
            width=240,
            height=40,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_nome.place(x=80, y=20)

        self.linha_nome = ctk.CTkFrame(
            self.frame_campo, fg_color='#FFFFFF', height=4, width=300
        )
        self.linha_nome.place(x=20, y=70)

    def _criar_campo_descricao(self) -> None:
        self.label_descricao = ctk.CTkLabel(
            self.frame_campo,
            text='Descrição',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_descricao.place(x=130, y=90)

        self.textbox_descricao = ctk.CTkTextbox(
            self.frame_campo,
            width=280,
            height=160,
            font=('Segoe UI', 15, 'bold'),
        )
        self.textbox_descricao.place(x=30, y=130)

        self.linha_descricao = ctk.CTkFrame(
            self.frame_campo, fg_color='#FFFFFF', height=4, width=280
        )
        self.linha_descricao.place(x=30, y=300)

    def _criar_campo_evento(self) -> None:
        self.label_evento = ctk.CTkLabel(
            self.frame_campo,
            text='Evento',
            text_color='#FFFFFF',
            font=('Segoe UI', 18, 'bold'),
        )
        self.label_evento.place(x=40, y=320)

        self.combobox_evento = ctk.CTkComboBox(
            self.frame_campo,
            width=200,
            height=30,
            font=('Segoe UI', 14, 'bold'),
            values=['Selecione'],
        )
        self.combobox_evento.place(x=110, y=320)

    def _criar_campo_botoes(self) -> None:
        self.btn_alterar = ctk.CTkButton(
            self.frame_campo,
            text='Alterar',
            width=110,
            height=40,
            font=('Segoe UI', 14, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.alterar_projeto,
        )
        self.btn_alterar.place(x=35, y=400)

        self.btn_excluir = ctk.CTkButton(
            self.frame_campo,
            text='Excluir',
            width=110,
            height=40,
            font=('Segoe UI', 14, 'bold'),
            fg_color='#F27F1B',
            text_color='#000000',
            hover_color='#F25C05',
            command=self.deletar_projeto,
        )
        self.btn_excluir.place(x=200, y=400)

    def _configure_tabela(self) -> None:
        self._criar_campo_busca()

    def _criar_campo_busca(self) -> None:
        self.entry_busca = ctk.CTkEntry(
            self.frame_busca,
            placeholder_text='Busca',
            width=320,
            height=40,
            font=('Segoe UI', 16, 'bold'),
        )
        self.entry_busca.place(x=10, y=20)

        self.combobox_colunas = ctk.CTkComboBox(
            self.frame_busca,
            font=('Segoe UI', 16, 'bold'),
            button_color='#F27F1B',
            button_hover_color='#F25C05',
            values=self.listar_colunas(),
        )
        self.combobox_colunas.place(x=190, y=70)
