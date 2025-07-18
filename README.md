Library yang digunakan 

1. Phyton Versi 3.10 (digunakan untuk : bahasa utama proyek)
2. scikit-learn Versi 1.3.0+ (digunakan untuk : memuat mode ML (.joblib))
3. librosa Versi 0.10.1+ (digunakan untuk : ekstraksi fitur audio (MFCC, Zero-Crossing Rate, dll))
4. soundfile Versi 0.12.1+ (digunakan untuk : membaca dan menulis file audio (WAV))
5. pygame Versi 2.6.1+ (digunakan untuk : memutar audio WAV)
6. sounddevice Versi 0.4.6+ (digunakan untuk merekam suara dari mikrofon)
7. pillow Versi 10.2.0+ (digunakan untuk menampilkan gambar atau icon dalam GUI)
8. ttkbootsrap Versi 1.10.1+ (digunakan untuk Library UI berbasis Tkinter dengan tampilan modern)
9. joblib Versi 1.4.2+ (digunakan untuk memuat model machine learning (.joblib)
10. tkinter Versi (built-in) (digunakan GUI utama, sudah tersedia dalam phyton bawaan)

CATATAN (tkinter tidak perlu di-install karena sudah include di phyton/anaconda)

Langkah-langkah instalasi Anaconda
1. Buka Anaconda Prompt
2. aktifkan environment baru dengan perintah:
   conda create -n deteksi_suara python=3.10
   conda activate deteksi_suara
3. Install library via conda dengan perintah:
   conda install scikit-learn librosa soundfile pillow joblib
4. Install library tambahan via pip dengan perintah:
   pip install pygame sounddevice ttkbootstrap
Jika Anda ingin membagikan environment ini ke dosen atau rekan, bisa buat file environment.yml berikut:
name: deteksi_suara
channels:
  - defaults
  - conda-forge
dependencies:
  - python=3.10
  - scikit-learn
  - librosa
  - soundfile
  - pillow
  - joblib
  - pip
  - pip:
      - pygame
      - sounddevice
      - ttkbootstrap

Instalasi dari file:

conda env create -f environment.yml

conda activate deteksi_suara
