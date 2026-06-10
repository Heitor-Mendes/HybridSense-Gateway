import tkinter as tk
import requests
import matplotlib.pyplot as plt

API = "http://127.0.0.1:5000"


# =========================
# APP
# =========================
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("HybridSense Gateway")
        self.geometry("600x450")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (
            Menu,
            AddSensor,
            RemoveSensor,
            SimularSensor,
            Processamento
        ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show(Menu)

    def show(self, frame):
        self.frames[frame].tkraise()


# =========================
# MENU (6 opções fixas)
# =========================
class Menu(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        tk.Label(self, text="MENU PRINCIPAL", font=("Arial", 18)).pack(pady=10)

        tk.Button(self, text="1 - Adicionar Sensor",
                  command=lambda: app.show(AddSensor)).pack(pady=5)

        tk.Button(self, text="2 - Remover Sensor",
                  command=lambda: app.show(RemoveSensor)).pack(pady=5)

        tk.Button(self, text="3 - Simular Sensores",
                  command=lambda: app.show(SimularSensor)).pack(pady=5)

        tk.Button(self, text="4 - Processamento de Sinais",
                  command=lambda: app.show(Processamento)).pack(pady=5)

        tk.Button(self, text="5 - Sensor Físico",
                  command=lambda: app.show(AddSensor)).pack(pady=5)

        tk.Button(self, text="6 - Processamento Físico",
                  command=lambda: app.show(Processamento)).pack(pady=5)


# =========================
# ADD SENSOR
# =========================
class AddSensor(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.nome = tk.Entry(self)
        self.nome.pack()

        tk.Label(self, text="Tensão").pack()

        self.tensao = tk.StringVar(value="3.3")

        tk.Radiobutton(self, text="3.3V", variable=self.tensao, value="3.3").pack()
        tk.Radiobutton(self, text="5V", variable=self.tensao, value="5").pack()
        tk.Radiobutton(self, text="12V", variable=self.tensao, value="12").pack()

        tk.Label(self, text="Protocolo").pack()

        self.proto = tk.StringVar(value="UART")

        tk.Radiobutton(self, text="UART", variable=self.proto, value="UART").pack()
        tk.Radiobutton(self, text="I2C", variable=self.proto, value="I2C").pack()
        tk.Radiobutton(self, text="SPI", variable=self.proto, value="SPI").pack()

        tk.Button(self, text="Salvar", command=self.salvar).pack()
        tk.Button(self, text="Voltar", command=lambda: app.show(Menu)).pack()

    def salvar(self):
        data = {
            "nome": self.nome.get(),
            "tensao": self.tensao.get(),
            "protocolo": self.proto.get()
        }

        r = requests.post(f"{API}/sensor/add", json=data)

        print(r.json())

        self.app.show(Menu)


# =========================
# REMOVER SENSOR
# =========================
class RemoveSensor(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.listbox = tk.Listbox(self)
        self.listbox.pack()

        tk.Button(self, text="Atualizar", command=self.load).pack()
        tk.Button(self, text="Remover", command=self.remove).pack()
        tk.Button(self, text="Voltar", command=lambda: app.show(Menu)).pack()

    def load(self):
        r = requests.get(f"{API}/sensor/list")
        self.data = r.json()

        self.listbox.delete(0, tk.END)

        for s in self.data:
            self.listbox.insert(tk.END, f'{s["id"]} - {s["nome"]}')

    def remove(self):
        sel = self.listbox.get(tk.ACTIVE)
        sid = sel.split(" - ")[0]

        requests.post(f"{API}/sensor/remove", json={"id": sid})

        self.load()
        self.app.show(Menu)


# =========================
# SIMULAR SENSOR
# =========================
class SimularSensor(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        self.listbox = tk.Listbox(self)
        self.listbox.pack()

        tk.Button(self, text="Carregar", command=self.load).pack()
        tk.Button(self, text="Iniciar Simulação", command=self.start).pack()
        tk.Button(self, text="Voltar", command=lambda: app.show(Menu)).pack()

    def load(self):
        r = requests.get(f"{API}/sensor/list")
        self.data = r.json()

        self.listbox.delete(0, tk.END)

        for s in self.data:
            self.listbox.insert(tk.END, f'{s["id"]} - {s["nome"]}')

    def start(self):
        sel = self.listbox.get(tk.ACTIVE)
        sid = sel.split(" - ")[0]

        r = requests.post(f"{API}/simular", json={"id": sid})

        print(r.json())

        self.app.show(Menu)


# =========================
# PROCESSAMENTO
# =========================
class Processamento(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)

        self.app = app

        tk.Button(self, text="Rodar FFT/Senoide", command=self.run).pack()
        tk.Button(self, text="Voltar", command=lambda: app.show(Menu)).pack()

    def run(self):
        r = requests.post(f"{API}/processar")

        data = r.json()

        plt.plot(data["t"], data["y"])
        plt.title("Sinal Simulado")
        plt.grid()
        plt.show()

        self.app.show(Menu)


App().mainloop()