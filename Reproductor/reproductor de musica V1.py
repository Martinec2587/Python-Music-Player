import os
import pygame
import tkinter as tk
from tkinter import filedialog

# Inicializar pygame mixer
pygame.mixer.init()

# Funciones del reproductor
def cargar_canciones():
    global songs, current
    folder = filedialog.askdirectory(title="Selecciona carpeta de música")
    if folder:
        songs = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith((".mp3", ".wav"))]
        if songs:
            current = 0
            lista_canciones.delete(0, tk.END)
            for song in songs:
                lista_canciones.insert(tk.END, os.path.basename(song))

def play_song():
    global current
    if songs:
        current = lista_canciones.curselection()[0] if lista_canciones.curselection() else current
        pygame.mixer.music.load(songs[current])
        pygame.mixer.music.play()
        estado.set(f"Reproduciendo: {os.path.basename(songs[current])}")

def pause_song():
    pygame.mixer.music.pause()
    estado.set("Pausado")

def unpause_song():
    pygame.mixer.music.unpause()
    estado.set("Reanudado")

def stop_song():
    pygame.mixer.music.stop()
    estado.set("Detenido")

def next_song():
    global current
    if songs:
        current = (current + 1) % len(songs)
        lista_canciones.selection_clear(0, tk.END)
        lista_canciones.selection_set(current)
        play_song()

def prev_song():
    global current
    if songs:
        current = (current - 1) % len(songs)
        lista_canciones.selection_clear(0, tk.END)
        lista_canciones.selection_set(current)
        play_song()

# Interfaz
root = tk.Tk()
root.title("Mini Reproductor de Música")

estado = tk.StringVar()
estado.set("Sin música cargada")

frame = tk.Frame(root)
frame.pack(pady=10)

btn_cargar = tk.Button(frame, text="Cargar música", command=cargar_canciones)
btn_cargar.grid(row=0, column=0, padx=5)

btn_play = tk.Button(frame, text="▶️ Play", command=play_song)
btn_play.grid(row=0, column=1, padx=5)

btn_pause = tk.Button(frame, text="⏸ Pausa", command=pause_song)
btn_pause.grid(row=0, column=2, padx=5)

btn_unpause = tk.Button(frame, text="🔄 Reanudar", command=unpause_song)
btn_unpause.grid(row=0, column=3, padx=5)

btn_stop = tk.Button(frame, text="⏹ Stop", command=stop_song)
btn_stop.grid(row=0, column=4, padx=5)

btn_prev = tk.Button(frame, text="⏮ Anterior", command=prev_song)
btn_prev.grid(row=1, column=0, padx=5, pady=5)

btn_next = tk.Button(frame, text="⏭ Siguiente", command=next_song)
btn_next.grid(row=1, column=4, padx=5, pady=5)

lista_canciones = tk.Listbox(root, width=50, height=10)
lista_canciones.pack(pady=10)

lbl_estado = tk.Label(root, textvariable=estado)
lbl_estado.pack()

# Variables globales
songs = []
current = 0

root.mainloop()

