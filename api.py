from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict
import os
import secrets
from datetime import datetime
from contextlib import contextmanager

# Import library kriptografi (Wajib untuk logika keamanan)
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature

app = FastAPI(title="Security Service", version="1.0.0")

USER_KEYS_DB: Dict[str, bytes] = {}       # Simpan Public Key
MESSAGE_INBOX: Dict[str, List[dict]] = {} # Simpan Pesan Relay
ACTIVE_TOKENS: Dict[str, str] = {}        # Simpan Token Login

# Setup Keamanan (Bearer Token)
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if token not in ACTIVE_TOKENS:
        raise HTTPException(status_code=403, detail="Akses Ditolak: Token tidak valid/sesi berakhir.")
    return ACTIVE_TOKENS[token]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fungsi contoh untuk memeriksa apakah layanan berjalan dengan baik (health check)
@app.get("/health")
async def health_check():
    return {
        "status": "Security Service is running",
        "timestamp": datetime.now().isoformat(),
        "active_users": list(USER_KEYS_DB.keys())
    }

# Fungsi akses pada lokasi "root" atau "index"
@app.get("/")
async def get_index() -> dict:
    return {
        "message": "Hello world! Please visit http://localhost:8080/docs for API UI."
    }

# Token untuk login
@app.post("/login")
async def login(username: str = Form(...)):
    token_baru = secrets.token_hex(16)
    ACTIVE_TOKENS[token_baru] = username
    return {
        "status": "Login Berhasil",
        "username": username,
        "access_token": token_baru,
        "token_type": "Bearer",
        "message": "COPY access_token ini dan klik tombol 'Authorize' (Gembok) di pojok kanan atas."
    }
    
# Fungsi API untuk menerima public key dan memastikan keutuhan file public key yang diterima
@app.post("/store")
async def store_pubkey(username: str = Form(...), file: UploadFile = File(...), token_user: str = Depends(verify_token)):
    # pesan kembalian ke user (sukses/gagal)
    msg = None
    status_op = "failed"

    try:
        # Baca konten file
        key_content = await file.read()
        
        # Integrity Check: Cek apakah format PEM valid
        serialization.load_pem_public_key(key_content)
        
        # Simpan ke database (Multiuser)
        USER_KEYS_DB[username] = key_content
        
        msg = f"Public Key untuk user '{username}' berhasil disimpan."
        status_op = "success"
        
    except ValueError:
        msg = "File rusak atau bukan format Public Key (PEM) yang valid."
    except Exception as e:
        msg = f"Error: {str(e)}"

    return {
        "message": msg,
        "status": status_op,
        "username": username
    }
    
# Fungsi API untuk memverifikasi signature yang dibuat oleh seorang pengguna
@app.post("/verify")
async def verify(username: str = Form(...), message: str = Form(...), signature_hex: str = Form(...), token_user: str = Depends(verify_token)):
    # pesan kembalian ke user (sukses/gagal)
    msg = None
    result = "INVALID"

    # Tuliskan code Anda di sini
    if username not in USER_KEYS_DB:
        msg = "User belum upload public key."
    else:
        try:
            # Load Public Key User
            pub_key = serialization.load_pem_public_key(USER_KEYS_DB[username])
            
            # Verifikasi Signature (ECDSA)
            sig_bytes = bytes.fromhex(signature_hex)
            pub_key.verify(
                sig_bytes,
                message.encode('utf-8'),
                ec.ECDSA(hashes.SHA256())
            )
            result = "VALID"
            msg = "Signature cocok. Pesan otentik."
        except InvalidSignature:
            msg = "Signature TIDAK cocok! Pesan mungkin telah diubah."
        except Exception as e:
            msg = f"Error: {str(e)}"

    return {
        "message": msg,
        "verification_result": result,
        "timestamp": datetime.now().isoformat()
    }

# Fungsi API untuk relay pesan ke user lain yang terdaftar
@app.post("/relay")
async def relay(sender: str = Form(...), recipient: str = Form(...), content: str = Form(...), token_user: str = Depends(verify_token)):
    # pesan kembalian ke user (sukses/gagal)
    msg = None

    # Buat inbox jika belum ada
    if recipient not in MESSAGE_INBOX:
        MESSAGE_INBOX[recipient] = []
        
    # Simpan pesan ke inbox recipient
    paket_pesan = {
        "from": sender,
        "timestamp": datetime.now().isoformat(),
        "content": content
    }
    MESSAGE_INBOX[recipient].append(paket_pesan)
    
    msg = f"Pesan dari {sender} berhasil diteruskan ke {recipient}."

    return {
        "message": msg,
        "status": "queued",
        "recipient_inbox_count": len(MESSAGE_INBOX[recipient])
    }

# Fungsi contoh untuk mengunggah file pdf
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...), signature_hex: Optional[str] = Form(None), username: Optional[str] = Form(None)):
    fname = file.filename
    ctype = file.content_type
    msg = "File uploaded!"
    
    try:
        contents = await file.read()
        
        if signature_hex and username:
            if username in USER_KEYS_DB:
                pub_key = serialization.load_pem_public_key(USER_KEYS_DB[username])
                sig_bytes = bytes.fromhex(signature_hex)
                pub_key.verify(sig_bytes, contents, ec.ECDSA(hashes.SHA256()))
                msg = "VALID: Dokumen PDF Asli dan Signature Cocok."
            else:
                msg = "User tidak ditemukan."
                
    except InvalidSignature:
        msg = "INVALID: Dokumen PDF Palsu atau telah dimodifikasi!"
    except Exception as e:
        return {
            "message": str(e)
        }
    
    return {
        "message": msg,
        "content-type": ctype,
        "filename": fname
    }

# Endpoint Cek Inbox 
@app.get("/inbox/{username}", dependencies=[Depends(verify_token)])
async def check_inbox(username: str):
    return MESSAGE_INBOX.get(username, [])