import sounddevice as sd
import soundfile as sf
import os

def rekam_tiruan(durasi=5, folder='rekaman_tiruan'):
    os.makedirs(folder, exist_ok=True)

    jumlah = int(input("Berapa sample tiruan yang ingin direkam? "))
    for i in range(jumlah):
        print(f"[TIRUAN] Rekaman {i+1} dimulai dalam 3 detik...")
        sd.sleep(3000)

        print(f"[TIRUAN] Rekaman {i+1} sedang berlangsung...")
        rekaman = sd.rec(int(durasi * 44100), samplerate=44100, channels=1)
        sd.wait()

        filename = f"{folder}/tiruan_{i+1}.wav"
        sf.write(filename, rekaman, 44100)
        print(f"[TIRUAN] Rekaman {i+1} disimpan di {filename}\n")

if __name__ == "__main__":
    rekam_tiruan()
