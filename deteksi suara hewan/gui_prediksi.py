import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import numpy as np
import joblib
import pygame
import time

# Load model sekali di awal
model = joblib.load("model_hewan.pkl")

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=5.0)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return mfcc_mean.reshape(1, -1)

def get_info_hewan(label):
    data_hewan = {
        "Anjing": {"asal": "Domestik", "habitat": "Rumah, Jalan"},
        "Elang": {"asal": "Asia", "habitat": "Pegunungan"},
        "Harimau": {"asal": "Asia", "habitat": "Hutan Tropis"},
        "Kucing": {"asal": "Domestik", "habitat": "Rumah"},
        "Monyet": {"asal": "Asia", "habitat": "Hutan"},
        "Sapi": {"asal": "Domestik", "habitat": "Peternakan"},
    }
    return data_hewan.get(label, {"asal": "Tidak diketahui", "habitat": "Tidak diketahui"})

def main_prediksi(file_path):
    fitur = extract_features(file_path)
    hasil = model.predict(fitur)[0]
    info = get_info_hewan(hasil)

    hasil_teks = f"Hasil Deteksi: {hasil}\nAsal: {info['asal']}\nHabitat: {info['habitat']}"
    return hasil_teks

def pilih_file():
    file_path = filedialog.askopenfilename(
        title="Pilih file suara WAV",
        filetypes=[("Audio Files", "*.wav")]
    )

    if file_path:
        try:
            # Play suara dulu
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Tunggu sampai suara selesai
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            # Setelah selesai baru deteksi
            hasil_teks = main_prediksi(file_path)
            messagebox.showinfo("Hasil Deteksi", hasil_teks)

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mendeteksi: {e}")

# GUI Tkinter
root = tk.Tk()
root.title("Deteksi Suara Hewan")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Klik tombol di bawah untuk memilih file suara")
label.pack(pady=10)

btn = tk.Button(frame, text="Pilih File Suara", command=pilih_file)
btn.pack(pady=10)

root.mainloop()
