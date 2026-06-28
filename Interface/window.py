import os
import customtkinter as ctk
from PIL import Image

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import api_client as api

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HybridSense Gateway")
        self.geometry("1320x720")

        self.porta_serial_real = None
        self.baud_rate_real = None
        self.tamanho_buffer_real = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_lateral = ctk.CTkFrame(self, width=300)
        self.frame_lateral.grid(row=0, column=0, sticky="nswe")

        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid(row=0, column=1, sticky="nswe")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(0, weight=0)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_rowconfigure(2, weight=0)

        self.construir_frame_lateral()
        self.frame_home()

    def construir_frame_lateral(self):
        for i in range(7):
            self.frame_lateral.grid_rowconfigure(i, weight=1)

        self.frame_lateral.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(self.frame_lateral, text="Menu", font=ctk.CTkFont(size=32, weight="bold"))
        titulo.grid(row=0, column=0, sticky="nsew", padx=20)

        botoes = [
            "Adicionar Sensor",
            "Remover Sensor",
            "Iniciar Simulação",
            "Ler Sensor Porta Serial",
            "Processamento de Sinais Virtuais",
            "Processamento de Sinais Físicos"
        ]

        for i, texto in enumerate(botoes, start=1):
            btn = ctk.CTkButton(self.frame_lateral, text=texto, font=ctk.CTkFont(size=22), command=lambda opcao=texto: self.selecionar_opcao(opcao))
            btn.grid(row=i, column=0, sticky="nsew", padx=20, pady=10)

    def selecionar_opcao(self, opcao):
        if opcao == "Adicionar Sensor":
            resposta = api.enviar_comando("adicionar_sensor_virtual")
            self.frame_adicionar_sensor(resposta)

        elif opcao == "Remover Sensor":
            resposta = api.enviar_comando("abrir_remocao_sensor_virtual")
            self.frame_remover_sensor(resposta)

        elif opcao == "Iniciar Simulação":
            resposta = api.enviar_comando("abrir_simulacao_sensor_virtual")
            self.frame_iniciar_simulacao(resposta)

        elif opcao == "Ler Sensor Porta Serial":
            api.cancelar_fluxo()
            self.frame_ler_sensor_real()

        elif opcao == "Processamento de Sinais Virtuais":
            resposta = api.enviar_comando("abrir_processamento_sensor_virtual")
            self.frame_processamento_sinais_virtuais(resposta)

        elif opcao == "Processamento de Sinais Físicos":
            api.cancelar_fluxo()
            self.frame_processamento_sinais_fisicos()

    def voltar_home(self):
        api.cancelar_fluxo()
        self.frame_home()

    def frame_home(self):
        self.clear_frame()

        for i in range(5):
            self.frame_principal.grid_rowconfigure(i, weight=0)

        self.frame_principal.grid_rowconfigure(2, weight=1)

        label_principal = ctk.CTkLabel(self.frame_principal, text="HybridSense Gateway", font=ctk.CTkFont(size=54, weight="bold"), text_color="#084D85")
        label_principal.grid(row=0, column=0, pady=(40, 10), sticky="nsew")

        label_adjacente = ctk.CTkLabel(self.frame_principal, text="Sistema de aquisição, simulação e processamento de sinais", font=ctk.CTkFont(size=28, weight="bold"))
        label_adjacente.grid(row=1, column=0, pady=(0, 20), sticky="nsew")

        frame_logo = ctk.CTkFrame(self.frame_principal, fg_color="#1A1A1A", corner_radius=24)
        frame_logo.grid(row=2, column=0, padx=180, pady=20, sticky="nsew")
        frame_logo.grid_columnconfigure(0, weight=1)
        frame_logo.grid_rowconfigure(0, weight=1)

        try:
            pasta_atual = os.path.dirname(os.path.abspath(__file__))
            caminho_logo = os.path.join(pasta_atual, "Logo_Politecnica.png")

            imagem = Image.open(caminho_logo)
            self.logo_poli = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(260, 260))

            label_imagem = ctk.CTkLabel(frame_logo, image=self.logo_poli, text="")
            label_imagem.grid(row=0, column=0, padx=30, pady=30)

        except Exception:
            label_logo = ctk.CTkLabel(frame_logo, text="POLI/UFRJ", font=ctk.CTkFont(size=44, weight="bold"), text_color="#3B8ED0")
            label_logo.grid(row=0, column=0, padx=30, pady=30)

        label_rodape = ctk.CTkLabel(self.frame_principal, text="Escolha uma opção na barra lateral para iniciar", font=ctk.CTkFont(size=22))
        label_rodape.grid(row=3, column=0, pady=(10, 35), sticky="nsew")

    def frame_adicionar_sensor(self, resposta_comando=None):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo("Adicionar Sensor Virtual")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao liberar rota."), 1)
            self.botao_voltar(2)
            return

        self.sensor_nome = ctk.CTkEntry(self.frame_principal, placeholder_text="Nome do Sensor", width=420, height=55, font=ctk.CTkFont(size=24))
        self.sensor_nome.grid(row=1, column=0, padx=280, pady=12, sticky="ew")

        self.sensor_protocolo = ctk.CTkOptionMenu(self.frame_principal, values=["UART", "I2C", "SPI"], width=420, height=55, font=ctk.CTkFont(size=24))
        self.sensor_protocolo.grid(row=2, column=0, padx=280, pady=12, sticky="ew")

        self.sensor_tensao = ctk.CTkOptionMenu(self.frame_principal, values=["3.3V", "5V"], width=420, height=55, font=ctk.CTkFont(size=24))
        self.sensor_tensao.grid(row=3, column=0, padx=280, pady=12, sticky="ew")

        btn_salvar = ctk.CTkButton(self.frame_principal, text="Salvar Sensor", height=55, font=ctk.CTkFont(size=24), command=self.confirmar_adicao_sensor)
        btn_salvar.grid(row=4, column=0, padx=280, pady=20, sticky="ew")

        self.botao_voltar(5)

    def confirmar_adicao_sensor(self):
        nome = self.sensor_nome.get()
        protocolo = self.sensor_protocolo.get()
        tensao_texto = self.sensor_tensao.get()

        if not nome:
            self.mensagem("Erro: o nome do sensor é obrigatório.", 6)
            return

        tensao = 3.3 if tensao_texto == "3.3V" else 5.0
        resposta = api.adicionar_sensor_virtual(nome, protocolo, tensao)

        if resposta.get("sucesso", False):
            self.frame_resultado_simples("Sensor adicionado", resposta.get("mensagem", "Sensor virtual adicionado com sucesso."))
        else:
            self.mensagem(resposta.get("mensagem", "Erro ao adicionar sensor."), 6)

    def frame_remover_sensor(self, resposta_comando=None):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo("Remover Sensor Virtual")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao carregar lista."), 1)
            self.botao_voltar(2)
            return

        sensores = self.carregar_lista_sensores()
        self.construir_lista_sensores(sensores, self.confirmar_remocao_sensor, "Remover")

    def confirmar_remocao_sensor(self, sensor):
        resposta = api.remover_sensor_virtual(sensor["endereco"])

        if resposta.get("sucesso", False):
            self.frame_resultado_simples("Sensor removido", resposta.get("mensagem", "Sensor removido com sucesso."))
        else:
            self.frame_resultado_simples("Erro", resposta.get("mensagem", "Erro ao remover sensor."))

    def frame_iniciar_simulacao(self, resposta_comando=None):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo("Iniciar Simulação")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao carregar lista."), 1)
            self.botao_voltar(2)
            return

        sensores = self.carregar_lista_sensores()
        self.construir_lista_sensores(sensores, self.confirmar_simulacao_sensor, "Simular")

    def confirmar_simulacao_sensor(self, sensor):
        resposta = api.simular_sensor_virtual(sensor["endereco"])

        if not resposta.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta.get("mensagem", "Erro ao simular sensor."))
            return

        sinal = resposta.get("sinal", [])
        self.frame_plot_sinal("Sinal Simulado", sinal, "Amostras do sensor virtual")

    def frame_processamento_sinais_virtuais(self, resposta_comando=None):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo("Processamento de Sinais Virtuais")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao carregar lista."), 1)
            self.botao_voltar(2)
            return

        sensores = self.carregar_lista_sensores()
        self.construir_lista_sensores(sensores, self.confirmar_processamento_virtual, "Processar")

    def confirmar_processamento_virtual(self, sensor):
        resposta = api.processar_sinais_virtual(sensor["endereco"])

        if not resposta.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta.get("mensagem", "Erro ao processar sinais."))
            return

        self.frame_resultado_processamento(resposta)

    def frame_ler_sensor_real(self):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo("Leitura do Sensor Físico")

        frame_form = ctk.CTkFrame(self.frame_principal, corner_radius=18)
        frame_form.grid(row=1, column=0, padx=280, pady=20, sticky="ew")
        frame_form.grid_columnconfigure(0, weight=1)

        label_info = ctk.CTkLabel(frame_form, text="Configure a comunicação serial do ESP32", font=ctk.CTkFont(size=24, weight="bold"), text_color="#D9D9D9")
        label_info.grid(row=0, column=0, padx=30, pady=(25, 5), sticky="ew")

        label_porta = ctk.CTkLabel(frame_form, text="Porta serial", font=ctk.CTkFont(size=18), anchor="w")
        label_porta.grid(row=1, column=0, padx=35, pady=(14, 0), sticky="ew")

        portas = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM11", "COM12", "COM13", "COM14", "COM15", "COM16", "COM17", "COM18", "COM19", "COM20", "/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyACM0", "/dev/ttyACM1"]
        self.sensor_real_porta = ctk.CTkOptionMenu(frame_form, values=portas, width=420, height=50, font=ctk.CTkFont(size=22))
        self.sensor_real_porta.set(self.porta_serial_real if self.porta_serial_real else "COM3")
        self.sensor_real_porta.grid(row=2, column=0, padx=30, pady=8, sticky="ew")

        label_baud = ctk.CTkLabel(frame_form, text="Baud rate", font=ctk.CTkFont(size=18), anchor="w")
        label_baud.grid(row=3, column=0, padx=35, pady=(10, 0), sticky="ew")

        self.sensor_real_baud = ctk.CTkOptionMenu(frame_form, values=["9600", "19200", "38400", "57600", "115200"], width=420, height=50, font=ctk.CTkFont(size=22))
        self.sensor_real_baud.set(str(self.baud_rate_real) if self.baud_rate_real else "115200")
        self.sensor_real_baud.grid(row=4, column=0, padx=30, pady=8, sticky="ew")

        label_buffer = ctk.CTkLabel(frame_form, text="Tamanho do buffer", font=ctk.CTkFont(size=18), anchor="w")
        label_buffer.grid(row=5, column=0, padx=35, pady=(10, 0), sticky="ew")

        self.sensor_real_buffer = ctk.CTkOptionMenu(frame_form, values=["25", "50", "100"], width=420, height=50, font=ctk.CTkFont(size=22))
        self.sensor_real_buffer.set(str(self.tamanho_buffer_real) if self.tamanho_buffer_real else "50")
        self.sensor_real_buffer.grid(row=6, column=0, padx=30, pady=8, sticky="ew")

        btn_salvar = ctk.CTkButton(frame_form, text="Salvar e iniciar leitura", height=55, font=ctk.CTkFont(size=22), command=self.confirmar_configuracao_sensor_real)
        btn_salvar.grid(row=7, column=0, padx=30, pady=(18, 28), sticky="ew")

        self.botao_voltar(2)

    def confirmar_configuracao_sensor_real(self):
        porta_serial = self.sensor_real_porta.get()
        baud_rate = int(self.sensor_real_baud.get())
        tamanho_buffer = int(self.sensor_real_buffer.get())

        self.porta_serial_real = porta_serial
        self.baud_rate_real = baud_rate
        self.tamanho_buffer_real = tamanho_buffer

        resposta = api.configurar_sensor_real(porta_serial, baud_rate, tamanho_buffer)

        if not resposta.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta.get("mensagem", "Erro ao configurar e ler sensor físico."))
            return

        sinal = resposta.get("sinal", [])
        descricao = f"Amostras do sensor real em {porta_serial} @ {baud_rate} baud | Buffer: {tamanho_buffer}"
        self.frame_plot_sensor_real(sinal, descricao)

    def atualizar_leitura_sensor_real(self):
        resposta = api.ler_sensor_real()

        if not resposta.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta.get("mensagem", "Erro ao atualizar leitura do sensor físico."))
            return

        sinal = resposta.get("sinal", [])
        descricao = f"Amostras do sensor real em {self.porta_serial_real} @ {self.baud_rate_real} baud | Buffer: {self.tamanho_buffer_real}"
        self.frame_plot_sensor_real(sinal, descricao)

    def frame_processamento_sinais_fisicos(self):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo("Processamento de Sinais Físicos")

        resposta = api.processar_sinais_real()

        if not resposta.get("sucesso", False):
            self.mensagem(resposta.get("mensagem", "Configure e leia o sensor físico antes de processar."), 1)
            btn_configurar = ctk.CTkButton(self.frame_principal, text="Configurar Sensor Físico", height=50, font=ctk.CTkFont(size=20), command=self.frame_ler_sensor_real)
            btn_configurar.grid(row=2, column=0, padx=280, pady=10, sticky="ew")
            self.botao_voltar(3)
            return

        self.frame_resultado_processamento(resposta)

    def carregar_lista_sensores(self):
        resposta = api.listar_sensores_virtuais()

        if not resposta.get("sucesso", False):
            self.mensagem(resposta.get("mensagem", "Erro ao carregar sensores."), 1)
            return []

        return resposta.get("sensores", [])

    def construir_lista_sensores(self, sensores, callback, texto_botao):
        if len(sensores) == 0:
            self.mensagem("Nenhum sensor virtual cadastrado.", 1)
            self.botao_voltar(2)
            return

        frame_lista = ctk.CTkScrollableFrame(self.frame_principal, width=760, height=460)
        frame_lista.grid(row=1, column=0, padx=120, pady=20, sticky="nsew")

        frame_lista.grid_columnconfigure(0, weight=1)
        frame_lista.grid_columnconfigure(1, weight=0)

        for i, sensor in enumerate(sensores):
            texto = f"{sensor['nome']} | Endereço: {sensor['endereco']}"

            label = ctk.CTkLabel(frame_lista, text=texto, font=ctk.CTkFont(size=22), anchor="w")
            label.grid(row=i, column=0, padx=20, pady=10, sticky="ew")

            btn = ctk.CTkButton(frame_lista, text=texto_botao, width=140, height=40, font=ctk.CTkFont(size=18), command=lambda s=sensor: callback(s))
            btn.grid(row=i, column=1, padx=20, pady=10)

        self.botao_voltar(2)

    def frame_resultado_processamento(self, resposta):
        self.clear_frame()
        self.preparar_layout_grafico()
        self.titulo("Resultado do Processamento")

        metricas = resposta.get("metricas", {})
        sinais = resposta.get("sinais", {})

        frame_metricas = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_metricas.grid(row=1, column=0, padx=18, pady=(0, 8), sticky="ew")

        for i in range(5):
            frame_metricas.grid_columnconfigure(i, weight=1)

        cards = [
            ("Média", metricas.get("media", 0), "#1F6AA5"),
            ("Mínimo", metricas.get("minimo", 0), "#2E8B57"),
            ("Máximo", metricas.get("maximo", 0), "#B8860B"),
            ("Desvio padrão", metricas.get("desvioPadrao", 0), "#7B68EE"),
            ("SNR", metricas.get("razaoSinalRuido", 0), "#C74747")
        ]

        for i, card in enumerate(cards):
            nome, valor, cor = card

            frame_card = ctk.CTkFrame(frame_metricas, fg_color=cor, corner_radius=16)
            frame_card.grid(row=0, column=i, padx=6, pady=4, sticky="nsew")

            label_nome = ctk.CTkLabel(frame_card, text=nome, font=ctk.CTkFont(size=16, weight="bold"), text_color="white")
            label_nome.pack(padx=10, pady=(10, 0))

            label_valor = ctk.CTkLabel(frame_card, text=f"{valor:.4f}", font=ctk.CTkFont(size=24, weight="bold"), text_color="white")
            label_valor.pack(padx=10, pady=(0, 10))

        frame_grafico = ctk.CTkFrame(self.frame_principal, corner_radius=18)
        frame_grafico.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        frame_grafico.grid_rowconfigure(0, weight=1)
        frame_grafico.grid_columnconfigure(0, weight=1)

        figura = Figure(figsize=(12, 6), dpi=100)
        figura.patch.set_facecolor("#2B2B2B")

        eixo = figura.add_subplot(111)
        eixo.set_facecolor("#1E1E1E")

        sinal_original = sinais.get("sinalOriginal", [])
        media_movel = sinais.get("mediaMovel", [])
        kalman = sinais.get("kalman", [])

        if len(sinal_original) > 0:
            eixo.plot(sinal_original, label="Sinal original", linewidth=1.4, color="#3B8ED0")

        if len(media_movel) > 0:
            eixo.plot(media_movel, label="Média móvel", linewidth=2.0, color="#2E8B57")

        if len(kalman) > 0:
            eixo.plot(kalman, label="Kalman", linewidth=2.0, color="#C74747")

        eixo.set_title("Sinais Processados", color="white", fontsize=16)
        eixo.set_xlabel("Amostra", color="white")
        eixo.set_ylabel("Valor", color="white")
        eixo.tick_params(colors="white")
        eixo.grid(True, color="#444444", alpha=0.55)

        for spine in eixo.spines.values():
            spine.set_color("#666666")

        legenda = eixo.legend(facecolor="#2B2B2B", edgecolor="#666666")
        for texto in legenda.get_texts():
            texto.set_color("white")

        figura.subplots_adjust(left=0.06, right=0.985, top=0.92, bottom=0.11)

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        self.botao_voltar(3)

    def frame_plot_sinal(self, titulo, sinal, descricao):
        self.clear_frame()
        self.preparar_layout_grafico()
        self.titulo(titulo)

        if len(sinal) == 0:
            self.mensagem("Nenhuma amostra disponível para plotagem.", 1)
            self.botao_voltar(2)
            return

        label = ctk.CTkLabel(self.frame_principal, text=descricao, font=ctk.CTkFont(size=20))
        label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="nsew")

        frame_grafico = ctk.CTkFrame(self.frame_principal, corner_radius=18)
        frame_grafico.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        frame_grafico.grid_rowconfigure(0, weight=1)
        frame_grafico.grid_columnconfigure(0, weight=1)

        figura = Figure(figsize=(12, 6), dpi=100)
        figura.patch.set_facecolor("#2B2B2B")

        eixo = figura.add_subplot(111)
        eixo.set_facecolor("#1E1E1E")
        eixo.plot(sinal, linewidth=1.8, color="#3B8ED0")
        eixo.set_title(titulo, color="white", fontsize=16)
        eixo.set_xlabel("Amostra", color="white")
        eixo.set_ylabel("Valor", color="white")
        eixo.tick_params(colors="white")
        eixo.grid(True, color="#444444", alpha=0.55)

        for spine in eixo.spines.values():
            spine.set_color("#666666")

        figura.subplots_adjust(left=0.06, right=0.985, top=0.92, bottom=0.11)

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        self.botao_voltar(3)

    def frame_plot_sensor_real(self, sinal, descricao):
        self.clear_frame()
        self.preparar_layout_grafico()
        self.titulo("Sinal Físico")

        if len(sinal) == 0:
            self.mensagem("Nenhuma amostra disponível para plotagem.", 1)
            self.botao_voltar(2)
            return

        label = ctk.CTkLabel(self.frame_principal, text=descricao, font=ctk.CTkFont(size=20))
        label.grid(row=1, column=0, padx=20, pady=(0, 5), sticky="nsew")

        frame_grafico = ctk.CTkFrame(self.frame_principal, corner_radius=18)
        frame_grafico.grid(row=2, column=0, padx=18, pady=8, sticky="nsew")
        frame_grafico.grid_rowconfigure(0, weight=1)
        frame_grafico.grid_columnconfigure(0, weight=1)

        figura = Figure(figsize=(12, 6), dpi=100)
        figura.patch.set_facecolor("#2B2B2B")

        eixo = figura.add_subplot(111)
        eixo.set_facecolor("#1E1E1E")
        eixo.plot(sinal, linewidth=1.8, color="#3B8ED0")
        eixo.set_title("Leitura Serial do ESP32", color="white", fontsize=16)
        eixo.set_xlabel("Amostra", color="white")
        eixo.set_ylabel("Valor", color="white")
        eixo.tick_params(colors="white")
        eixo.grid(True, color="#444444", alpha=0.55)

        for spine in eixo.spines.values():
            spine.set_color("#666666")

        figura.subplots_adjust(left=0.06, right=0.985, top=0.92, bottom=0.11)

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", padx=8, pady=8)

        frame_botoes = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        frame_botoes.grid(row=3, column=0, padx=280, pady=(6, 14), sticky="ew")
        frame_botoes.grid_columnconfigure(0, weight=1)
        frame_botoes.grid_columnconfigure(1, weight=1)

        btn_atualizar = ctk.CTkButton(frame_botoes, text="Atualizar leitura", height=42, font=ctk.CTkFont(size=18), command=self.atualizar_leitura_sensor_real)
        btn_atualizar.grid(row=0, column=0, padx=8, sticky="ew")

        btn_voltar = ctk.CTkButton(frame_botoes, text="Voltar", height=42, font=ctk.CTkFont(size=18), command=self.voltar_home)
        btn_voltar.grid(row=0, column=1, padx=8, sticky="ew")

    def frame_resultado_simples(self, titulo, mensagem):
        self.clear_frame()
        self.preparar_layout_formulario()
        self.titulo(titulo)

        label = ctk.CTkLabel(self.frame_principal, text=mensagem, font=ctk.CTkFont(size=28), wraplength=850)
        label.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        self.botao_voltar(2)

    def titulo(self, texto):
        label = ctk.CTkLabel(self.frame_principal, text=texto, font=ctk.CTkFont(size=42, weight="bold"), text_color="#084D85")
        label.grid(row=0, column=0, pady=25, sticky="nsew")

    def mensagem(self, texto, row):
        label = ctk.CTkLabel(self.frame_principal, text=texto, font=ctk.CTkFont(size=24), wraplength=850)
        label.grid(row=row, column=0, padx=40, pady=20, sticky="nsew")

    def botao_voltar(self, row):
        btn_voltar = ctk.CTkButton(self.frame_principal, text="Voltar", height=45, command=self.voltar_home)
        btn_voltar.grid(row=row, column=0, padx=280, pady=10, sticky="ew")

    def clear_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

    def preparar_layout_formulario(self):
        for i in range(8):
            self.frame_principal.grid_rowconfigure(i, weight=0)

        self.frame_principal.grid_columnconfigure(0, weight=1)

    def preparar_layout_grafico(self):
        for i in range(6):
            self.frame_principal.grid_rowconfigure(i, weight=0)

        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(2, weight=1)


janela = Aplicativo()
janela.mainloop()
