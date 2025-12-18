# Layanan Kriptografi API
Proyek UAS Mata Kuliah Keamanan dan Integritas Data Semester 3 Sains Data Unesa

### Anggota Kelompok 12
1. Ananda Keissa Az Zahra (24031554051)
2. Laili Nurrohmatul Fadhila Z. (24031554093)
3. Eka Putri Maharani (24031554121)

## Tujuan Proyek:
1. Merancang dan mengimplementasikan sebuah sistem API berbasis FastAPI yang berfungsi sebagai Trusted Authority Server.
2. Mengimplementasikan mekanisme pengelolaan kunci publik sebagai dasar proses otentikasi antar pengguna sistem.
3. Menerapkan verifikasi tanda tangan digital untuk menjamin integritas dan keaslian data yang dipertukarkan melalui API.
4. Membangun mekanisme penyampaian pesan (relay) yang aman guna mendukung pertukaran informasi penelitian secara terpercaya.

## Struktur File
1. main.py: Entry point untuk menjalankan server uvicorn.
2. api.py: Core logic API, autentikasi, dan verifikasi kriptografi.
3. client.py: Simulasi user untuk membuat kunci dan signature.

## Prasyarat
1. Sebelum menjalankan proyek ini, pastikan komputer Anda telah terinstal **`uv`** (Python Package Manager). Kunjungi https://docs.astral.sh/uv/ untuk metode instalasinya.
2. Persiapkan project ini dengan melakukan sinkronisasi dependensi. Ketik `uv sync` pada terminal di lokasi project ini berada. Perintah ini akan membuat sebuah virtual environment `.venv` (hidden) pada root folder, lalu memasang libraries yang dibutuhkan.

## Cara Menjalankan (Pipeline)
Ikuti langkah-langkah berikut untuk mensimulasikan alur kerja Client-Server:

### 1. Persiapan Sisi Client (Generate Key & Signature)
Jalankan skrip client untuk membuat pasangan kunci (Public/Private Key) dan menandatangani dokumen PDF secara lokal.

```bash
uv run client.py
```

### 2. Menjalankan Server
Nyalakan server API di terminal terpisah:

```bash
uv run main.py
```
Buka browser (chrome/edge) dan akses antarmuka Swagger UI di: http://localhost:8080/docs

### Tampilan Swagger UI

<img width="1918" height="997" alt="Image" src="https://github.com/user-attachments/assets/cc8f8c0f-5e83-4a25-8a0f-5486f1b4a2cb" />

### 3. Pengujian 
Laman `SwaggerAPI` (http://localhost:8080/docs) akan menampilkan seluruh fungsi-fungsi API yang telah dibuat dalam file `api.py`.
    -   Klik pada fungsi yang akan diakses.
    -   Klik `Try it out`
    -   Lengkapi formulir (parameters fungsi) yang dibutuhkan.
    -   Klik `Execute` untuk melakukan "submission".



