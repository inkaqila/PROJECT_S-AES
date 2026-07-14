# 💻 Web Simulasi Kriptografi: Simplified Advanced Encryption Standard (S-AES)

Proyek ini adalah aplikasi web simulasi interaktif untuk mengenkripsi dan mendekripsi data menggunakan algoritma **Simplified Advanced Encryption Standard (S-AES)**. Aplikasi ini dibangun menggunakan framework **Python Flask** sebagai backend dan **HTML5/Tailwind CSS/Vanilla JavaScript** pada sisi frontend. 

Dibuat khusus untuk memenuhi Tugas Individu Mata Kuliah Kriptografi, Semester Genap 2025/2026, Program Studi Informatika, Universitas Bale Bandung.

---

## 👤 Identitas Mahasiswa
* **Nama:** Inka Aqila Nurfalqi
* **NIM:** 301230043
* **Kelas:** IF 6A
* **Mata Kuliah:** Kriptografi
* **Institusi:** Universitas Bale Bandung

---

## 🛠️ Fitur Utama Aplikasi
1. **Mode Ganda:** Mendukung fungsionalitas penuh untuk proses **Enkripsi** dan **Dekripsi**.
2. **Validasi Input Real-Time:** Input biner 16-bit divalidasi secara langsung agar mencegah kesalahan input karakter non-biner.
3. **Key Expansion Penjabaran Rinci:** Menampilkan komputasi pembagian Word ($w_0$ s.d $w_5$) beserta penggunaan konstanta RCON dan S-Box.
4. **Visualisasi State Matrix 2x2:** Menampilkan representasi grid *column-major* dalam format gabungan `Hex (Biner)` di setiap tahapan transformasi.
5. **Aritmetika Galois Field $GF(2^4)$:** Logika perkalian bitwise murni di backend menggunakan irredusibel polinomial $x^4 + x + 1$.
6. **Toggle Tampilan:** Detail perhitungan langkah dapat disembunyikan atau ditampilkan secara dinamis melalui antarmuka interaktif.

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