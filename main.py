import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
from auth import gecerli_kullanici, token_olustur, sifre_hashle, sifre_dogrula
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm


kullanicilar_db = {}

load_dotenv()  # .env dosyasını okur

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

@app.post("/kayit")
def kayit_ol(kullanici_adi: str, sifre: str):
    if kullanici_adi in kullanicilar_db:
        raise HTTPException(status_code=400, detail="Kullanici adi zaten mevcut")
    hashli_sifre = sifre_hashle(sifre)
    kullanicilar_db[kullanici_adi] = hashli_sifre
    return {"mesaj": "Kayit başarili"}

@app.post("/giris")
def giris(form_data: OAuth2PasswordRequestForm = Depends()):
    hashli_sifre = kullanicilar_db.get(form_data.username)
    if not hashli_sifre or not sifre_dogrula(form_data.password, hashli_sifre):
        raise HTTPException(status_code=400, detail="Kullanici adi veya sifre hatali")
    token = token_olustur(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

@app.get("/")
def ana_sayfa():
    return {"mesaj": "Merhaba, bu benim ilk API'm!"}

@app.get("/selam/{isim}")
def selamla(isim):
    return {"mesaj": f"Merhaba {isim}, hoş geldin!"}

class Soru(BaseModel):
    metin: str

@app.post("/sor")
def sor(soru: Soru, kullanici: str = Depends(gecerli_kullanici)):
    cevap = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=soru.metin
    )
    return {"cevap": cevap.text}
import numpy as np

URUNLER = [
    "Beyaz seramik lavabo, 60cm, modern banyo tasarimi, 4500 TL",
    "Gömme rezervuar seti, mat siyah buton, 7200 TL",
    "Krem rengi yer seramiği, 60x60, kaymaz yüzey, metrekare 850 TL",
    "Duşakabin, 90x90 köşe, temperli cam, 12500 TL",
    "Banyo bataryasi, krom, su tasarruf özellikli, 3200 TL",
]

def embed(metin):
    sonuc = client.models.embed_content(
        model="gemini-embedding-001",
        contents=metin
    )
    return np.array(sonuc.embeddings[0].values)

URUN_VEKTORLERI = [embed(u) for u in URUNLER]

def en_yakin_urunler(soru, kac_tane=2):
    soru_v = embed(soru)
    benzerlikler = []
    for i, uv in enumerate(URUN_VEKTORLERI):
        skor = np.dot(soru_v, uv) / (np.linalg.norm(soru_v) * np.linalg.norm(uv))
        benzerlikler.append((skor, URUNLER[i]))
    benzerlikler.sort(reverse=True)
    return [u for _, u in benzerlikler[:kac_tane]]

@app.post("/urun-sor")
def urun_sor(soru: Soru):
    bulunanlar = en_yakin_urunler(soru.metin)
    prompt = f"""Sen bir yapi market satiş asistanisin.
Müşterinin sorusu: {soru.metin}
Elimizdeki ilgili ürünler: {bulunanlar}
Sadece bu ürünlere dayanarak kisa ve samimi bir cevap ver."""
    cevap = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return {"bulunan_urunler": bulunanlar, "cevap": cevap.text}

