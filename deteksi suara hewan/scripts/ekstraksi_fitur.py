import librosa
import os
import numpy as np
import pandas as pd

def extract_features(file_path):
    y, sr = librosa.load(file_path, duration=5.0)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    mfcc_mean = np.mean(mfcc.T, axis=0)
    return mfcc_mean

def create_dataset(wav_folder, label_mapping):
    features = []
    labels = []

    for file_name in os.listdir(wav_folder):
        if file_name.endswith(".wav"):
            file_path = os.path.join(wav_folder, file_name)
            try:
                mfcc_features = extract_features(file_path)
                label = label_mapping.get(file_name, "Unknown")

                features.append(mfcc_features)
                labels.append(label)

                print(f"[✓] Ekstrak: {file_name} → Label: {label}")
            except Exception as e:
                print(f"[!] Gagal ekstrak {file_name}: {e}")

    df = pd.DataFrame(features)
    df['label_hewan'] = labels
    return df

if __name__ == "__main__":
    label_mapping = {
        "suara anjing.wav": "Anjing",
        "suara elang.wav": "Elang",
        "suara harimau.wav": "Harimau",
        "suara kucing.wav": "Kucing",
        "suara monyet.wav": "Monyet",
        "suara sapi.wav": "Sapi",
    }

    dataset = create_dataset("data_wav", label_mapping)
    dataset.to_csv("fitur_dataset.csv", index=False)
    print("[✓] Dataset berhasil disimpan ke fitur_dataset.csv")
