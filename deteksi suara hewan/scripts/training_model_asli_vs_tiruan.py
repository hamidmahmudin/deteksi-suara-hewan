import os
import librosa
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

def extract_fitur_folder(folder_path, label_name):
    fitur = []
    label = []

    for file in os.listdir(folder_path):
        if file.endswith(".wav"):
            file_path = os.path.join(folder_path, file)
            y, sr = librosa.load(file_path, duration=5.0)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc.T, axis=0)

            fitur.append(mfcc_mean)
            label.append(label_name)

    return fitur, label

if __name__ == "__main__":
    fitur_asli, label_asli = extract_fitur_folder("data_wav", "Asli")
    fitur_tiruan, label_tiruan = extract_fitur_folder("rekaman_tiruan", "Tiruan")

    X = np.array(fitur_asli + fitur_tiruan)
    y = np.array(label_asli + label_tiruan)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, "model_asli_vs_tiruan.pkl")
    print("[✓] Model berhasil dilatih dan disimpan ke model_asli_vs_tiruan.pkl")
