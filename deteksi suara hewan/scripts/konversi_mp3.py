from pydub import AudioSegment
import os

def convert_mp3_to_wav(mp3_folder, wav_folder):
    # Cek folder output, buat kalau belum ada
    if not os.path.exists(wav_folder):
        os.makedirs(wav_folder)

    # Loop semua file di folder mp3
    for file_name in os.listdir(mp3_folder):
        if file_name.endswith(".mp3"):
            mp3_path = os.path.join(mp3_folder, file_name)
            wav_path = os.path.join(wav_folder, file_name.replace(".mp3", ".wav"))

            try:
                audio = AudioSegment.from_mp3(mp3_path)
                audio.export(wav_path, format="wav")
                print(f"[✓] Berhasil convert: {file_name} → {wav_path}")
            except Exception as e:
                print(f"[!] Gagal convert {file_name}: {e}")

if __name__ == "__main__":
    convert_mp3_to_wav("data_mp3", "data_wav")
