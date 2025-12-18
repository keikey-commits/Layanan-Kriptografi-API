from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import os

def generate_and_save_keys(username):
    print(f"--- Membuat Kunci untuk User: {username} ---")
    
    # 1. Generate Private Key (Menggunakan Algoritma Elliptic Curve SECP256K1)
    priv_key = ec.generate_private_key(ec.SECP256K1(), backend=default_backend())

    # 2. Generate Public Key dari Private Key
    pub_key = priv_key.public_key()

    # 3. Serialisasi Private Key ke format PEM (Simpan ke file)
    pem_priv = priv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Simpan Private Key 
    priv_filename = f"{username}_priv.pem"
    with open(priv_filename, "wb") as f:
        f.write(pem_priv)
    print(f"[OK] Private Key disimpan: {priv_filename}")

    # 4. Serialisasi Public Key ke format PEM (Simpan ke file)
    pem_pub = pub_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    pub_filename = f"{username}_pub.pem"
    with open(pub_filename, "wb") as f:
        f.write(pem_pub)
    print(f"[OK] Public Key disimpan: {pub_filename}")
    
    return priv_key, pub_key

# Fungsi untuk menandatangani pesan (Sign)
def sign_message(private_key, message_text):
    print(f"\n--- Menandatangani Pesan: '{message_text}' ---")
    
    # Encode pesan ke bytes
    data = message_text.encode('utf-8')
    
    # Buat tanda tangan digital (ECDSA dengan SHA256)
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )
    
    # Konversi signature ke format Hexadecimal (agar mudah dikirim via API)
    sig_hex = signature.hex()
    
    print(f"Signature (Hex): {sig_hex}")
    print("COPY Signature di atas untuk dimasukkan ke Swagger UI (/verify)!")
    return sig_hex

def sign_pdf_file(private_key, filename):
    print(f"\n--- Menandatangani File PDF: {filename} ---")
    
    try:
        # Buka file PDF dalam mode binary (rb)
        with open(filename, "rb") as f:
            pdf_data = f.read()
            
        # Tanda tangani data binary tersebut
        signature = private_key.sign(
            pdf_data,
            ec.ECDSA(hashes.SHA256())
        )
        
        sig_hex = signature.hex()
        print(f"PDF Signature (Hex): {sig_hex}")
        print("COPY Signature ini untuk di-upload di menu /upload-pdf")
        return sig_hex
        
    except FileNotFoundError:
        print(f"Error: File {filename} tidak ditemukan. Buat dulu file dummy.")

if __name__ == "__main__":
    nama_user = "keissa" # bisa ganti dengan nama lain
    
    # 1. Generate Key
    my_priv, my_pub = generate_and_save_keys(nama_user)
    
    # 2. Contoh membuat Signature pesan (biar bisa tes Verify nanti)
    pesan_saya = "HAIIIIII SEMUAA, ini project KID"
    sign_message(my_priv, pesan_saya)
    
    # 3. Buat file untuk ttd
    with open("ttd_keissa.pdf", "w") as f: # bisa ganti dengan nama lain
        f.write("Laporan Sistem Keamanan oleh Keissa.")
    print("\n[INFO] File 'ttd_keissa.pdf' berhasil dibuat untuk tes.")

    # 4. Tanda tangani PDF tersebut
    sign_pdf_file(my_priv, "ttd_keissa.pdf")

    print(f"\n[SUKSES] Key untuk '{nama_user}' sudah jadi!")