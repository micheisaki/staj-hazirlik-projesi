# Staj Hazırlık Projesi — FastAPI + LLM + RAG

Yapay zekâ destekli bir backend servisi. Kullanıcılar JWT ile kayıt olup giriş yapar, korumalı endpoint üzerinden Google Gemini'ye soru sorar ve örnek ürün verisi üzerinde RAG (Retrieval-Augmented Generation) ile çalışan bir soru-cevap sistemini kullanır.

## Kullanılan Teknolojiler

- **Python, FastAPI**: REST API ve otomatik Swagger dokümantasyonu
- **Google Gemini API**: LLM ile metin üretimi ve embedding
- **RAG**: Gemini embedding'leri + kosinüs benzerliği ile en alakalı içeriği bulup modele bağlam olarak verme
- **JWT Authentication**: Token tabanlı kimlik doğrulama, hash'lenmiş şifreler
- **Güvenlik**: API anahtarı ve secret key ortam değişkenlerinden (`.env`) okunur, repoya gönderilmez

## Endpoint'ler

| Metot | Endpoint | Açıklama |
|---|---|---|
| POST | `/kayit` | Yeni kullanıcı kaydı (şifre hash'lenerek saklanır) |
| POST | `/giris` | Giriş yapar, JWT access token döner |
| POST | `/sor` | **Korumalı.** Token ile Gemini'ye soru sorar |
| POST | `/urun-sor` | Ürün verisi üzerinde RAG ile soru-cevap |
| GET | `/` | Sağlık kontrolü |

## Kurulum

```bash
git clone https://github.com/micheisaki/staj-hazirlik-projesi.git
cd staj-hazirlik-projesi

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env            # Ardından .env içine kendi değerlerini gir
```

`.env` içinde gerekenler:

```
GEMINI_API_KEY=...   # Google AI Studio'dan alınır
SECRET_KEY=...       # JWT imzalamak için rastgele uzun bir metin
```

## Çalıştırma

```bash
uvicorn main:app --reload
```

Swagger arayüzü: http://127.0.0.1:8000/docs

Swagger'da `/kayit` ile kullanıcı oluştur, sağ üstteki **Authorize** butonuyla giriş yap, ardından `/sor` endpoint'ini dene.

## Staj Sürecinde Eklenenler

Bu repo projenin ilk sürümüdür. theBlueRed'deki stajım sırasında proje şu yönlerde genişletildi:

- Kullanıcı verilerinin bellekten **PostgreSQL + SQLAlchemy**'ye taşınması
- **React (Vite + axios)** ile kayıt/giriş arayüzü, CORS yapılandırması
- **React Native (Expo)** mobil uygulamanın backend'e bağlanması
- Gemini ile **sesten metne** (speech-to-text) endpoint'i

## Notlar

- Paket kurma komutlarını her zaman venv aktifken çalıştır.
- Yeni paket eklediğinde: `pip freeze > requirements.txt`
