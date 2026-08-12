# Staj Hazırlık Projesi — Ortam Kurulum Notları

## Venv'i Aktifleştirme

**Windows:**
venv\Scripts\activate

**macOS:**
source venv/bin/activate

## Projeyi Çalıştırma (venv aktifken, her iki OS'ta aynı)
uvicorn main:app --reload

Swagger arayüzü: http://127.0.0.1:8000/docs

## Venv'den Çıkma (her iki OS'ta aynı)
deactivate

## Paket Kurma (venv aktifken)
pip install -r requirements.txt

## requirements.txt'i Güncelleme (yeni paket eklediğinde)
pip freeze > requirements.txt

## Notlar
- Paket kurma komutlarını HER ZAMAN venv aktifken çalıştır, aksi halde
  proje çalışırken paketleri bulamaz (ModuleNotFoundError/ImportError alırsın).
- `.env` dosyası git'e gönderilmez (gitignore'lu), her makinede elle
  oluşturulup GEMINI_API_KEY ve SECRET_KEY girilmesi gerekir.
  