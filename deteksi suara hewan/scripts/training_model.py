import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# 1. Load dataset
data = pd.read_csv("fitur_dataset.csv")

# 2. Pisahkan fitur dan label
X = data.drop(columns=["label_hewan"])
y = data["label_hewan"]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Training model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 5. Evaluasi
print("Akurasi Training:", model.score(X_train, y_train))
print("Akurasi Testing:", model.score(X_test, y_test))

# 6. Simpan model
joblib.dump(model, "model_hewan.pkl")
print("[✓] Model tersimpan sebagai model_hewan.pkl")
