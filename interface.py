# gui.py

import tkinter as tk
import requests

API_URL = "http://127.0.0.1:5000/comando"

def enviar(opcao):
    try:
        resposta = requests.post(
            API_URL,
            json={"opcao": opcao}
        )

        resultado.config(
            text=f"Resposta: {resposta.json()['status']}"
        )

    except Exception as e:
        resultado.config(text=str(e))


janela = tk.Tk()
janela.title("Menu Principal")
janela.geometry("400x400")

titulo = tk.Label(
    janela,
    text="Escolha uma opção",
    font=("Arial", 16)
)
titulo.pack(pady=10)

text = ["Adicionar Sensor", "Remover Sensor", "Simular Sensores", "Processamento de Sinais", "Adicionar Sensor Físico", "Processamento do Sensor Físico"]
for i in range(len(text)):
    tk.Button(
        janela,
        text=f" {i+1}" + " - " + text[i],
        width=40,
        command=lambda x=i: enviar(x)
    ).pack(pady=5)

resultado = tk.Label(janela, text="")
resultado.pack(pady=20)

janela.mainloop()