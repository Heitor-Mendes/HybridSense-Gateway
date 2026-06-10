import customtkinter as ctk
from PIL import Image
import matplotlib.pyplot as plt
import main

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Aplicativo(ctk.CTk):
    
    def __init__(self):
        
        # Inicializacoes basicas
        super().__init__()
        self.title("HybridSense Gateway")
        self.geometry("1320x720")

        #Criando uma tela expansivel
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
    
        #parte lateral
        self.frame_lateral = ctk.CTkFrame(self, width=300)
        self.frame_lateral.grid(row=0, column=0, sticky="nswe")

        #parte principal
        self.frame_principal = ctk.CTkFrame(self)
        self.frame_principal.grid_rowconfigure(0, weight=0)    # Título fixo
        self.frame_principal.grid_rowconfigure(1, weight=1)    # Espaço vazio que expande
        self.frame_principal.grid_rowconfigure(2, weight=0)    # Rodapé
        self.frame_principal.grid_columnconfigure(0, weight=1) # Centraliza o conteú
        self.frame_principal.grid(row=0, column=1, sticky="nswe")

        self.construir_frame_lateral()
        self.frame_home()

    def construir_frame_lateral(self):

        # Faz as linhas crescerem
        for i in range(7):
            self.frame_lateral.grid_rowconfigure(i, weight=1)

        self.frame_lateral.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(self.frame_lateral, text="Menu", font=ctk.CTkFont(size=32, weight="bold"))

        titulo.grid(row=0, column=0, sticky="nsew", padx=20)

        botoes = [
            "Adicionar Sensor",
            "Remover Sensor",
            "Iniciar Simulação",
            "Adicionar Sensor Porta Serial",
            "Processamento de Sinais Virtuais",
            "Processamento de Sinais Físicos"]

        for i, texto in enumerate(botoes, start=1):
            btn = ctk.CTkButton(self.frame_lateral,text=texto, font=ctk.CTkFont(size=24), command=lambda opcao=texto: self.selecionar_opcao(opcao))

            btn.grid(row=i, column=0, sticky="nsew", padx=20, pady=10)

    
    #Enderecamento das opções do menu lateral
    def selecionar_opcao(self, opcao):
    
        main.enviar_comando(opcao)
        
        if opcao == "Adicionar Sensor":
            print(f"Opção: {opcao}")
            self.frame_adicionar_sensor()

        elif opcao == "Remover Sensor":
            print(f"Opção: {opcao}")
            self.frame_remover_sensor()

        elif opcao == "Iniciar Simulação":
            print(f"Opção: {opcao}  ")
            self.frame_iniciar_simulacao()

        elif opcao == "Adicionar Sensor Porta Serial":
            print(f"Opção: {opcao}")
            self.frame_adicionar_sensor_porta_serial()

        elif opcao == "Processamento de Sinais Virtuais":
            print(f"Opção: {opcao}")
            self.frame_processamento_sinais_virtuais()
        
        elif opcao == "Processamento de Sinais Físicos":
            print(f"Opção: {opcao}")
            self.frame_processamento_sinais_fisicos()

    # Logicca de pegar dados de novos sensores
    def frame_adicionar_sensor(self):
        
        self.clear_frame()

        self.sensor_nome = ctk.CTkEntry(self.frame_principal, placeholder_text="Nome do Sensor", width=300, height=60, font=ctk.CTkFont(size=32))
        self.sensor_nome.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")

        self.sensor_protocolo = ctk.CTkOptionMenu(self.frame_principal, values=["UART", "I2C", "SPI"], width=300, height=60, font=ctk.CTkFont(size=32))
        self.sensor_protocolo.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.sensor_tensao = ctk.CTkOptionMenu(self.frame_principal, values=["3.3V", "5V"], width=300, height=60, font=ctk.CTkFont(size=32))
        self.sensor_tensao.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")    
    
        btn_salvar = ctk.CTkButton(self.frame_principal, text="Salvar Sensor", command=self.confirmar_adicao_sensor)
        btn_salvar.grid(row=4, column=0, pady=20, padx=10, sticky="nsew")

        main.adicionar_sensor(self.sensor_nome, self.sensor_protocolo, self.sensor_tensao)

    def frame_remover_sensor(self):
        pass

    def frame_iniciar_simulacao(self):
        pass

    def frame_adicionar_sensor_porta_serial(self):
        pass

    def frame_processamento_sinais_virtuais(self):
        pass
    
    def frame_processamento_sinais_fisicos(self):
        pass

    def frame_home(self):
        self.clear_frame()
        imagem_del  = Image.open("Logo_Politecnica.png")
        
        self.label_principal = ctk.CTkLabel(self.frame_principal, text="Bem-Vindo ao HibridSense Gateway", font=ctk.CTkFont(size=48, weight="bold"), text_color="blue")
        self.label_principal.grid(row=0, column=0, pady=20, sticky="nsew")

        self.label_adjacente = ctk.CTkLabel(self.frame_principal, text="Escolha a opcao na barra lateral", font=ctk.CTkFont(size=48, weight="bold"))
        self.label_adjacente.grid(row=1, column=0, pady=20, sticky="nsew")

        imagem_ctk_del       = ctk.CTkImage(light_image=imagem_del,  dark_image=imagem_del,  size=(250,250))



        label_imagem_del     = ctk.CTkLabel(self.frame_principal, image=imagem_ctk_del, text="")
        label_imagem_del.grid(row=2, column=0, padx=20, pady=20, sticky="se")

    # utilidades
    def confirmar_adicao_sensor(self):
        nome   = self.sensor_nome.get()
        proto  = self.sensor_protocolo.get()
        tensao = self.sensor_tensao.get()

        if not nome:
            print("Erro: O nome do sensor é obrigatório!")
            return

        print(f"Enviando para C++: {nome}, {proto}, {tensao}")
        main.adicionar_sensor(nome, proto, tensao)
        
        #voltar para frame principal limpo
        self.frame_home()
    
    def clear_frame(self):
        # Destrói todos os widgets filhos do frame principal
        for widget in self.frame_principal.winfo_children():
            widget.destroy()

janela = Aplicativo()
janela.mainloop()