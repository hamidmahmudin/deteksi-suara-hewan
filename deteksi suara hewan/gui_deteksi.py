import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pygame
import librosa
import numpy as np
import joblib
import sounddevice as sd
import soundfile as sf
import os
import warnings
import threading
import time
from datetime import datetime
import ttkbootstrap as ttk

warnings.filterwarnings("ignore", category=UserWarning)

model_hewan = joblib.load("model/model_hewan.pkl")
model_asli_tiruan = joblib.load("model/model_asli_vs_tiruan.pkl")

label_wav_map = {
    "suara anjing.wav": "Anjing",
    "suara kucing.wav": "Kucing",
    "suara harimau.wav": "Harimau",
    "suara elang.wav": "Elang",
    "suara monyet.wav": "Monyet",
    "suara sapi.wav": "Sapi",
}

data_hewan = {
    "Anjing": {"Asal": "Global", "Habitat": "Pemukiman, Hutan"},
    "Kucing": {"Asal": "Global", "Habitat": "Pemukiman"},
    "Harimau": {"Asal": "Asia", "Habitat": "Hutan Tropis"},
    "Elang": {"Asal": "Global", "Habitat": "Pegunungan, Hutan"},
    "Monyet": {"Asal": "Asia, Afrika", "Habitat": "Hutan Tropis"},
    "Sapi": {"Asal": "Global", "Habitat": "Peternakan, Padang Rumput"},
}

pygame.mixer.init()
app = ttk.Window(themename="flatly")
app.title("Deteksi Suara Hewan")
app.geometry("600x700")
loading_window = None
loading_label = None


def show_loading():
    global loading_window, loading_label
    loading_window = tk.Toplevel(app)
    loading_window.title("Loading")
    loading_window.geometry("250x300")
    loading_window.resizable(False, False)

    loading_gif = Image.open("share/loading_icon.gif")
    frames = []
    try:
        while True:
            frames.append(ImageTk.PhotoImage(loading_gif.copy().resize((150, 150))))
            loading_gif.seek(len(frames))
    except EOFError:
        pass

    def update(ind):
        frame = frames[ind]
        loading_label.configure(image=frame)
        loading_label.image = frame
        ind = (ind + 1) % len(frames)
        loading_window.after(100, update, ind)

    loading_label = ttk.Label(loading_window)
    loading_label.pack(pady=10)
    ttk.Label(loading_window, text="Sistem sedang mendeteksi!   ", font=("Arial", 12)).pack()
    update(0)
    loading_window.update()


def hide_loading():
    global loading_window
    if loading_window:
        app.after(0, loading_window.destroy)
        loading_window = None



def play_sound_and_wait(file_path):
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)


def proses_prediksi_file(file_path):
    show_loading()
    play_sound_and_wait(file_path)
    hasil_asli_tiruan = predict_asli_tiruan(file_path)
    hide_loading()

    if hasil_asli_tiruan == "Tiruan":
        messagebox.showinfo("Hasil", "Deteksi: Suara tiruan/manusia")
    else:
        file_name = os.path.basename(file_path)
        if file_name in label_wav_map:
            hasil_label = label_wav_map[file_name]
            info = data_hewan.get(hasil_label, {"Asal": "Tidak diketahui", "Habitat": "Tidak diketahui"})
            messagebox.showinfo("Hasil Deteksi", f"Hewan: {hasil_label}\nAsal: {info['Asal']}\nHabitat: {info['Habitat']}")
        else:
            hasil = predict_hewan(file_path)
            info = data_hewan.get(hasil, {"Asal": "Tidak diketahui", "Habitat": "Tidak diketahui"})
            messagebox.showinfo("Hasil Deteksi", f"Hewan: {hasil}\nAsal: {info['Asal']}\nHabitat: {info['Habitat']}")


def predict_asli_tiruan(file_path):
    y, sr = librosa.load(file_path, duration=5.0)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0).reshape(1, -1)
    return model_asli_tiruan.predict(mfcc_mean)[0]


def predict_hewan(file_path):
    y, sr = librosa.load(file_path, duration=5.0)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0).reshape(1, -1)
    return model_hewan.predict(mfcc_mean)[0]


def pilih_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")], initialdir="data_wav")
    if file_path:
        threading.Thread(target=proses_prediksi_file, args=(file_path,), daemon=True).start()


def rekam_suara():
    folder = "rekaman_suara"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"rekaman_{timestamp}.wav")

    record_icon = Image.open("share/record_icon.png").resize((100, 100))
    record_photo = ImageTk.PhotoImage(record_icon)

    icon_window = tk.Toplevel(app)
    icon_window.title("Sedang Merekam")
    icon_label = ttk.Label(icon_window, image=record_photo)
    icon_label.image = record_photo
    icon_label.pack()

    def proses_rekam():
        durasi = 5
        fs = 44100
        rekaman = sd.rec(int(durasi * fs), samplerate=fs, channels=1)
        sd.wait()
        sf.write(filename, rekaman, fs)

        icon_window.destroy()  # Tutup icon record setelah selesai
        threading.Thread(target=proses_prediksi_file, args=(filename,), daemon=True).start()

    # Jalankan proses rekam di thread lain supaya icon muncul dulu
    threading.Thread(target=proses_rekam, daemon=True).start()



logo_img = Image.open("share/logo.png").resize((150, 150))
logo = ImageTk.PhotoImage(logo_img)
ttk.Label(app, image=logo).pack(pady=10)

ttk.Button(app, text="Pilih File Suara dari data_wav", command=pilih_file).pack(pady=10)
ttk.Button(app, text="Rekam Suara dari Mic", command=rekam_suara).pack(pady=10)

app.mainloop()
