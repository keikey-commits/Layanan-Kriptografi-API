# File utama menjalankan API server yang ada di file api.py

import uvicorn
import os
from dotenv import load_dotenv

# Memuat variabel lingkungan dari file .env (jika ada)
# Ini praktik yang baik karena dependensi python-dotenv sudah terinstall
load_dotenv()

def main():
    # Menjalankan server menggunakan Uvicorn
    # "api:app" merujuk pada file api.py dan object app di dalamnya
    # Port 8080 disesuaikan dengan petunjuk di README.md
    # reload=True mengaktifkan auto-reload saat coding
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)

if __name__ == "__main__":
    main()