import customtkinter as ctk
from PIL import Image
import requests
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

API_URL = "http://127.0.0.1:5000"
TAMANHO_BUFFER_PADRAO = 1000


def post_api(rota, payload):
    try:
        resposta = requests.post(API_URL + rota, json=payload, timeout=5)
        return resposta.json()
    except Exception as erro:
        return {"sucesso": False, "mensagem": str(erro)}


def get_api(rota):
    try:
        resposta = requests.get(API_URL + rota, timeout=5)
        return resposta.json()
    except Exception as erro:
        return {"sucesso": False, "mensagem": str(erro)}


def enviar_comando(comando):
    return post_api("/Sistema/Comandos", {"comando": comando})


class Aplicativo(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HybridSense Gateway")
        self.geometry("1320x720")

        self.sensor_selecionado = None

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
            resposta = enviar_comando("adicionar_sensor_virtual")
            self.frame_adicionar_sensor(resposta)

        elif opcao == "Remover Sensor":
            resposta = enviar_comando("abrir_remocao_sensor_virtual")
            self.frame_remover_sensor(resposta)

        elif opcao == "Iniciar Simulação":
            resposta = enviar_comando("abrir_simulacao_sensor_virtual")
            self.frame_iniciar_simulacao(resposta)

        elif opcao == "Ler Sensor Porta Serial":
            self.frame_ler_sensor_real()

        elif opcao == "Processamento de Sinais Virtuais":
            resposta = enviar_comando("abrir_processamento_sensor_virtual")
            self.frame_processamento_sinais_virtuais(resposta)

        elif opcao == "Processamento de Sinais Físicos":
            self.frame_processamento_sinais_fisicos()

    def frame_home(self):
        self.clear_frame()

        label_principal = ctk.CTkLabel(self.frame_principal, text="Bem-vindo ao HybridSense Gateway", font=ctk.CTkFont(size=46, weight="bold"), text_color="blue")
        label_principal.grid(row=0, column=0, pady=30, sticky="nsew")

        label_adjacente = ctk.CTkLabel(self.frame_principal, text="Escolha uma opção na barra lateral", font=ctk.CTkFont(size=36, weight="bold"))
        label_adjacente.grid(row=1, column=0, pady=20, sticky="nsew")

        try:
            imagem = Image.open("Logo_Politecnica.png")
            imagem_ctk = ctk.CTkImage(light_image=imagem, dark_image=imagem, size=(200, 200))
            label_imagem = ctk.CTkLabel(self.frame_principal, image=imagem_ctk, text="")
            label_imagem.grid(row=2, column=0, padx=20, pady=20, sticky="se")
        except Exception:
            label_logo = ctk.CTkLabel(self.frame_principal, text="HybridSense", font=ctk.CTkFont(size=28, weight="bold"))
            label_logo.grid(row=2, column=0, padx=20, pady=20, sticky="se")

    def frame_adicionar_sensor(self, resposta_comando=None):
        self.clear_frame()

        self.titulo("Adicionar Sensor Virtual")

        self.sensor_nome = ctk.CTkEntry(self.frame_principal, placeholder_text="Nome do Sensor", width=420, height=55, font=ctk.CTkFont(size=24))
        self.sensor_nome.grid(row=1, column=0, padx=280, pady=12, sticky="ew")

        self.sensor_protocolo = ctk.CTkOptionMenu(self.frame_principal, values=["UART", "I2C", "SPI"], width=420, height=55, font=ctk.CTkFont(size=24))
        self.sensor_protocolo.grid(row=2, column=0, padx=280, pady=12, sticky="ew")

        self.sensor_tensao = ctk.CTkOptionMenu(self.frame_principal, values=["3.3V", "5V"], width=420, height=55, font=ctk.CTkFont(size=24))
        self.sensor_tensao.grid(row=3, column=0, padx=280, pady=12, sticky="ew")

        btn_salvar = ctk.CTkButton(self.frame_principal, text="Salvar Sensor", height=55, font=ctk.CTkFont(size=24), command=self.confirmar_adicao_sensor)
        btn_salvar.grid(row=4, column=0, padx=280, pady=20, sticky="ew")

        btn_voltar = ctk.CTkButton(self.frame_principal, text="Voltar", height=45, command=self.frame_home)
        btn_voltar.grid(row=5, column=0, padx=280, pady=10, sticky="ew")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao liberar rota."), 6)

    def confirmar_adicao_sensor(self):
        nome = self.sensor_nome.get()
        protocolo = self.sensor_protocolo.get()
        tensao_texto = self.sensor_tensao.get()

        if not nome:
            self.mensagem("Erro: o nome do sensor é obrigatório.", 6)
            return

        tensao = 3.3 if tensao_texto == "3.3V" else 5.0

        payload = {"nome": nome, "tensao": tensao, "protocolo": protocolo, "tamanhoBuffer": TAMANHO_BUFFER_PADRAO}
        resposta = post_api("/Sistema/SensoresVirtuais/Adicionar", payload)

        if resposta.get("sucesso", False):
            self.frame_resultado_simples("Sensor adicionado", resposta.get("mensagem", "Sensor virtual adicionado com sucesso."))
        else:
            self.mensagem(resposta.get("mensagem", "Erro ao adicionar sensor."), 6)

    def frame_remover_sensor(self, resposta_comando=None):
        self.clear_frame()
        self.titulo("Remover Sensor Virtual")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao carregar lista."), 1)
            return

        sensores = self.carregar_lista_sensores()
        self.construir_lista_sensores(sensores, self.confirmar_remocao_sensor, "Remover")

    def confirmar_remocao_sensor(self, sensor):
        resposta = post_api("/Sistema/SensoresVirtuais/Remover", {"endereco": sensor["endereco"]})

        if resposta.get("sucesso", False):
            self.frame_resultado_simples("Sensor removido", resposta.get("mensagem", "Sensor removido com sucesso."))
        else:
            self.frame_resultado_simples("Erro", resposta.get("mensagem", "Erro ao remover sensor."))

    def frame_iniciar_simulacao(self, resposta_comando=None):
        self.clear_frame()
        self.titulo("Iniciar Simulação")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao carregar lista."), 1)
            return

        sensores = self.carregar_lista_sensores()
        self.construir_lista_sensores(sensores, self.confirmar_simulacao_sensor, "Simular")

    def confirmar_simulacao_sensor(self, sensor):
        resposta_post = post_api("/Sistema/SensoresVirtuais/Simulacao", {"endereco": sensor["endereco"]})

        if not resposta_post.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta_post.get("mensagem", "Erro ao simular sensor."))
            return

        resposta_get = get_api("/Sistema/SensoresVirtuais/Simulacao")

        if not resposta_get.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta_get.get("mensagem", "Erro ao ler simulação."))
            return

        sinal = resposta_get.get("sinal", [])
        self.frame_plot_sinal("Sinal Simulado", sinal, "Amostras do sensor virtual")

    def frame_processamento_sinais_virtuais(self, resposta_comando=None):
        self.clear_frame()
        self.titulo("Processamento de Sinais Virtuais")

        if resposta_comando and not resposta_comando.get("sucesso", False):
            self.mensagem(resposta_comando.get("mensagem", "Erro ao carregar lista."), 1)
            return

        sensores = self.carregar_lista_sensores()
        self.construir_lista_sensores(sensores, self.confirmar_processamento_virtual, "Processar")

    def confirmar_processamento_virtual(self, sensor):
        resposta_post = post_api("/Sistema/SensoresVirtuais/ProcessamentoDeSinais", {"endereco": sensor["endereco"]})

        if not resposta_post.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta_post.get("mensagem", "Erro ao processar sinais."))
            return

        resposta_get = get_api("/Sistema/SensoresVirtuais/ProcessamentoDeSinais")

        if not resposta_get.get("sucesso", False):
            self.frame_resultado_simples("Erro", resposta_get.get("mensagem", "Erro ao ler processamento."))
            return

        self.frame_resultado_processamento(resposta_get)

    def frame_ler_sensor_real(self):
        self.clear_frame()
        self.titulo("Leitura do Sensor Físico")

        resposta = get_api("/Sistema/SensorReal/Dados")

        if not resposta.get("sucesso", False):
            self.mensagem(resposta.get("mensagem", "Sensor físico ainda não implementado."), 1)
            return

        sinal = resposta.get("sinal", [])
        self.frame_plot_sinal("Sinal Físico", sinal, "Amostras do sensor real")

    def frame_processamento_sinais_fisicos(self):
        self.clear_frame()
        self.titulo("Processamento de Sinais Físicos")

        resposta = get_api("/Sistema/SensorReal/ProcessamentoDeSinais")

        if not resposta.get("sucesso", False):
            self.mensagem(resposta.get("mensagem", "Processamento físico ainda não implementado."), 1)
            return

        self.frame_resultado_processamento(resposta)

    def carregar_lista_sensores(self):
        resposta = get_api("/Sistema/SensoresVirtuais/Lista")

        if not resposta.get("sucesso", False):
            self.mensagem(resposta.get("mensagem", "Erro ao carregar sensores."), 1)
            return []

        return resposta.get("sensores", [])

    def construir_lista_sensores(self, sensores, callback, texto_botao):
        if len(sensores) == 0:
            self.mensagem("Nenhum sensor virtual cadastrado.", 1)
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

        btn_voltar = ctk.CTkButton(self.frame_principal, text="Voltar", height=45, command=self.frame_home)
        btn_voltar.grid(row=2, column=0, padx=280, pady=10, sticky="ew")

    def frame_resultado_processamento(self, resposta):
        self.clear_frame()
        self.titulo("Resultado do Processamento")

        metricas = resposta.get("metricas", {})
        sinais = resposta.get("sinais", {})

        frame_metricas = ctk.CTkFrame(self.frame_principal)
        frame_metricas.grid(row=1, column=0, padx=20, pady=10, sticky="new")

        texto_metricas = ""
        texto_metricas += f"Média: {metricas.get('media', 0):.4f}\n"
        texto_metricas += f"Mínimo: {metricas.get('minimo', 0):.4f}\n"
        texto_metricas += f"Máximo: {metricas.get('maximo', 0):.4f}\n"
        texto_metricas += f"Desvio padrão: {metricas.get('desvioPadrao', 0):.4f}\n"
        texto_metricas += f"Razão sinal-ruído: {metricas.get('razaoSinalRuido', 0):.4f}"

        label_metricas = ctk.CTkLabel(frame_metricas, text=texto_metricas, font=ctk.CTkFont(size=22), justify="left")
        label_metricas.pack(padx=20, pady=20)

        frame_grafico = ctk.CTkFrame(self.frame_principal)
        frame_grafico.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        figura = Figure(figsize=(8, 3.7), dpi=100)
        eixo = figura.add_subplot(111)

        sinal_original = sinais.get("sinalOriginal", [])
        media_movel = sinais.get("mediaMovel", [])
        kalman = sinais.get("kalman", [])

        if len(sinal_original) > 0:
            eixo.plot(sinal_original, label="Sinal original")

        if len(media_movel) > 0:
            eixo.plot(media_movel, label="Média móvel")

        if len(kalman) > 0:
            eixo.plot(kalman, label="Kalman")

        eixo.set_title("Sinais Processados")
        eixo.set_xlabel("Amostra")
        eixo.set_ylabel("Valor")
        eixo.legend()
        eixo.grid(True)

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        btn_voltar = ctk.CTkButton(self.frame_principal, text="Voltar", height=45, command=self.frame_home)
        btn_voltar.grid(row=3, column=0, padx=280, pady=10, sticky="ew")

    def frame_plot_sinal(self, titulo, sinal, descricao):
        self.clear_frame()
        self.titulo(titulo)

        if len(sinal) == 0:
            self.mensagem("Nenhuma amostra disponível para plotagem.", 1)
            return

        label = ctk.CTkLabel(self.frame_principal, text=descricao, font=ctk.CTkFont(size=22))
        label.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        frame_grafico = ctk.CTkFrame(self.frame_principal)
        frame_grafico.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        figura = Figure(figsize=(9, 4.2), dpi=100)
        eixo = figura.add_subplot(111)
        eixo.plot(sinal)
        eixo.set_title(titulo)
        eixo.set_xlabel("Amostra")
        eixo.set_ylabel("Valor")
        eixo.grid(True)

        canvas = FigureCanvasTkAgg(figura, master=frame_grafico)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        btn_voltar = ctk.CTkButton(self.frame_principal, text="Voltar", height=45, command=self.frame_home)
        btn_voltar.grid(row=3, column=0, padx=280, pady=10, sticky="ew")

    def frame_resultado_simples(self, titulo, mensagem):
        self.clear_frame()
        self.titulo(titulo)

        label = ctk.CTkLabel(self.frame_principal, text=mensagem, font=ctk.CTkFont(size=28), wraplength=850)
        label.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        btn_voltar = ctk.CTkButton(self.frame_principal, text="Voltar", height=45, command=self.frame_home)
        btn_voltar.grid(row=2, column=0, padx=280, pady=10, sticky="ew")

    def titulo(self, texto):
        label = ctk.CTkLabel(self.frame_principal, text=texto, font=ctk.CTkFont(size=42, weight="bold"), text_color="blue")
        label.grid(row=0, column=0, pady=25, sticky="nsew")

    def mensagem(self, texto, row):
        label = ctk.CTkLabel(self.frame_principal, text=texto, font=ctk.CTkFont(size=24), wraplength=850)
        label.grid(row=row, column=0, padx=40, pady=20, sticky="nsew")

    def clear_frame(self):
        for widget in self.frame_principal.winfo_children():
            widget.destroy()


janela = Aplicativo()
janela.mainloop()