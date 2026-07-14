# 💻 Web Simulasi Kriptografi: Simplified Advanced Encryption Standard (S-AES)

[cite_start]Proyek ini adalah aplikasi web simulasi interaktif untuk mengenkripsi dan mendekripsi data menggunakan algoritma **Simplified Advanced Encryption Standard (S-AES)**[cite: 8, 9]. [cite_start]Aplikasi ini dibangun menggunakan framework **Python Flask** sebagai backend dan **HTML5/Tailwind CSS/Vanilla JavaScript** pada sisi frontend[cite: 126]. 

[cite_start]Dibuat khusus untuk memenuhi Tugas Individu Mata Kuliah Kriptografi, Semester Genap 2025/2026, Program Studi Informatika, Universitas Bale Bandung[cite: 1, 2, 3, 95].

---

## 👤 Identitas Mahasiswa
* [cite_start]**Nama:** Inka Aqila Nurfalqi [cite: 95, 190]
* [cite_start]**NIM:** 301230043 [cite: 95, 190]
* [cite_start]**Kelas:** IF 6A [cite: 95, 190]
* [cite_start]**Mata Kuliah:** Kriptografi [cite: 2, 95]
* [cite_start]**Institusi:** Universitas Bale Bandung [cite: 95, 335]

---

## 🛠️ Fitur Utama Aplikasi
1. [cite_start]**Mode Ganda:** Mendukung fungsionalitas penuh untuk proses **Enkripsi** dan **Dekripsi**[cite: 9, 32].
2. [cite_start]**Validasi Input Real-Time:** Input biner 16-bit divalidasi secara langsung agar mencegah kesalahan input karakter non-biner[cite: 74].
3. [cite_start]**Key Expansion Penjabaran Rinci:** Menampilkan komputasi pembagian Word ($w_0$ s.d $w_5$) beserta penggunaan konstanta RCON dan S-Box[cite: 38, 39, 40, 41, 42, 43, 44].
4. [cite_start]**Visualisasi State Matrix 2x2:** Menampilkan representasi grid *column-major* dalam format gabungan `Hex (Biner)` di setiap tahapan transformasi[cite: 21, 46, 77].
5. [cite_start]**Aritmetika Galois Field $GF(2^4)$:** Logika perkalian bitwise murni di backend menggunakan irredusibel polinomial $x^4 + x + 1$[cite: 21].
6. [cite_start]**Toggle Tampilan:** Detail perhitungan langkah dapat disembunyikan atau ditampilkan secara dinamis melalui antarmuka interaktif[cite: 76].

---

## 📂 Struktur Direktori Proyek
```text
📦 saes-simulation-app
├── 📂 saes_crypto          # Modul Core Kriptografi S-AES
│   ├── 📄 __init__.py
│   └── 📄 saes_engine.py   # Logika GF(2^4), S-Box, & Transformasi State
├── 📂 templates
│   └── 📄 index.html       # Single Page Application (UI & Interaktivitas JS)
├── 📄 app.py               # Entry Point Aplikasi Flask & Routing API
├── 📄 requirements.txt     # Daftar Dependensi Library
└── 📄 vercel.json          # Konfigurasi Deployment Serverless Vercel