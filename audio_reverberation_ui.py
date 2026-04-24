import tkinter as tk
from tkinter import filedialog, ttk
import librosa
import sounddevice as sd
import numpy as np
from scipy.signal import convolve
import matplotlib.pyplot as plt

audio = None
ir = None
resultado = None
sr = 44100


# ------------------ CARGAR AUDIO ------------------
def cargar_audio():
    global audio, sr
    file = filedialog.askopenfilename(filetypes=[("WAV", "*.wav")])
    if file:
        audio, sr = librosa.load(file, sr=None)
        label_audio.config(text="Audio cargado ✔")


# ------------------ CARGAR IR ------------------
def cargar_ir():
    global ir
    file = filedialog.askopenfilename(filetypes=[("WAV", "*.wav")])
    if file:
        ir, _ = librosa.load(file, sr=sr)
        label_ir.config(text="IR cargada ✔")


# ------------------ SIMULAR ------------------
def simular():
    global resultado
    if audio is not None and ir is not None:
        resultado = convolve(audio, ir, mode="full")
        resultado = resultado / np.max(np.abs(resultado))
        label_result.config(text="Reverberación lista ✔")


# ------------------ AUDIO ------------------
def play(data):
    if data is not None:
        sd.play(data, sr)
        sd.wait()


# ------------------ GRÁFICAS ------------------
def graficar():
    if audio is None or ir is None or resultado is None:
        return

    plt.figure(figsize=(12, 6))

    plt.subplot(3, 1, 1)
    plt.plot(audio)
    plt.title("Audio de entrada")

    plt.subplot(3, 1, 2)
    plt.plot(ir)
    plt.title("Respuesta impulsional")

    plt.subplot(3, 1, 3)
    plt.plot(resultado)
    plt.title("Audio con reverberación")

    plt.tight_layout()
    plt.show()


# ------------------ UI ------------------
root = tk.Tk()
root.title("Simulador de Reverberación")
root.geometry("800x500")

# PANEL IZQUIERDO
panel = tk.Frame(root)
panel.pack(side="left", padx=20, pady=20)

tk.Button(panel, text="Cargar Audio", command=cargar_audio, width=25).pack(pady=5)
label_audio = tk.Label(panel, text="Sin audio")
label_audio.pack()

tk.Button(panel, text="Cargar IR", command=cargar_ir, width=25).pack(pady=5)
label_ir = tk.Label(panel, text="Sin IR")
label_ir.pack()

tk.Button(panel, text="Simular Reverberación", command=simular, width=25).pack(pady=10)
label_result = tk.Label(panel, text="Sin procesar")
label_result.pack()

tk.Button(panel, text="▶ Entrada", command=lambda: play(audio), width=25).pack(pady=5)
tk.Button(panel, text="▶ IR", command=lambda: play(ir), width=25).pack(pady=5)
tk.Button(panel, text="▶ Resultado", command=lambda: play(resultado), width=25).pack(pady=5)

tk.Button(panel, text="📊 Gráficas", command=graficar, width=25).pack(pady=10)

root.mainloop()