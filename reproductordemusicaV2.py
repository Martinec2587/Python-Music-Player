import os
import pygame
import tkinter as tk
from tkinter import filedialog, ttk
from mutagen.mp3 import MP3  # Para obtener la duración de los mp3
import time

# Inicializar pygame mixer
pygame.mixer.init()

# Variables globales
songs = []
current = 0
song_length = 0  # duración actual de la canción en segundos
updating = False  # bandera para evitar múltiples actualizaciones

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

def obtener_duracion(song_path):
    if song_path.endswith('.mp3'):
        audio = MP3(song_path)
        return int(audio.info.length)
    elif song_path.endswith('.wav'):
        # Si quieres soporte para wav, puedes usar wave.open
        import wave
        with wave.open(song_path, 'rb') as w:
            frames = w.getnframes()
            rate = w.getframerate()
            return int(frames / float(rate))
    return 0

def play_song():
    global current, song_length, updating
    if songs:
        current = lista_canciones.curselection()[0] if lista_canciones.curselection() else current
        pygame.mixer.music.load(songs[current])
        pygame.mixer.music.play()
        estado.set(f"Reproduciendo: {os.path.basename(songs[current])}")
        song_length = obtener_duracion(songs[current])
        progress_bar['maximum'] = song_length
        progress_bar['value'] = 0
        actualizar_barra_progreso()
        updating = True

def pause_song():
    global updating
    pygame.mixer.music.pause()
    estado.set("Pausado")
    updating = False

def unpause_song():
    global updating
    pygame.mixer.music.unpause()
    estado.set("Reanudado")
    if not updating:
        actualizar_barra_progreso()
        updating = True

def stop_song():
    global updating
    pygame.mixer.music.stop()
    estado.set("Detenido")
    progress_bar['value'] = 0
    updating = False

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

def actualizar_barra_progreso():
    if pygame.mixer.music.get_busy():
        # pygame.mixer.music.get_pos() regresa milisegundos
        actual = pygame.mixer.music.get_pos() // 1000
        if actual < 0: actual = 0
        progress_bar['value'] = actual
        # Actualiza la etiqueta de tiempo
        lbl_tiempo.config(text=f"{formatear_tiempo(actual)} / {formatear_tiempo(song_length)}")
        root.after(500, actualizar_barra_progreso)
    else:
        progress_bar['value'] = song_length
        lbl_tiempo.config(text=f"{formatear_tiempo(song_length)} / {formatear_tiempo(song_length)}")

def formatear_tiempo(segundos):
    minutos = segundos // 60
    segundos = segundos % 60
    return f"{minutos:02}:{segundos:02}"

def saltar_a_posicion(event):
    if song_length > 0:
        x = event.x
        ancho = progress_bar.winfo_width()
        nuevo_segundo = int((x / ancho) * song_length)
        pygame.mixer.music.play(start=nuevo_segundo)
        progress_bar['value'] = nuevo_segundo

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

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=5)
# Para barra interactiva: progress_bar.bind("<Button-1>", saltar_a_posicion)

lbl_tiempo = tk.Label(root, text="00:00 / 00:00")
lbl_tiempo.pack()

lbl_estado = tk.Label(root, textvariable=estado)
lbl_estado.pack()

root.mainloop()
