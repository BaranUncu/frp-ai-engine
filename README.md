# 🎲 FRP AI Game Master Engine (Alpha v0.1.0)

Bu proje, Masaüstü Rol Yapma Oyunları (FRP/TTRPG) için tasarlanmış, yapay zeka destekli modüler bir Game Master (Oyun Yöneticisi) arka uç motorudur. Python ve FastAPI tabanlı asenkron mimarisiyle kural motorlarını, zar hesaplamalarını ve RAG (Retrieval-Augmented Generation) hafızasını tek bir sistemde birleştirir.

## 🚀 Öne Çıkan Özellikler

- **Çoklu Sistem Desteği:** D&D 5e, Fate Core ve Call of Cthulhu kural setlerini destekleyecek soyut mimari (`base_system.py`).
- **Gelişmiş Zar Motoru:** Regex tabanlı zar parser'ı ile karmaşık zar formüllerini (ör. `1d20+5`, `4dF`) anında hesaplama yeteneği.
- **Session 0 Entegrasyonu:** Pydantic şemaları ile oyuncu sınırlarını, evren kurallarını ve karakter motivasyonlarını yapay zeka bağlamına (context) aktarma.
- **Hibrit Hafıza Mimarisi:**
  - *Hard Data:* Karakter statları, HP ve envanter yönetimi için ilişkisel veritabanı (**SQLite & SQLAlchemy**).
  - *Soft Data:* Oyun geçmişi, NPC diyalogları ve dünya lore'u için RAG (Retrieval-Augmented Generation) destekli vektör veritabanı (**ChromaDB**).
- **Gerçek Zamanlı İletişim:** FastAPI WebSockets ile asenkron oyun döngüsü ve LLM'den gelen hikayenin istemciye kelime kelime (streaming) aktarımı.
- **Hafif ve Modern Frontend:** Node.js gerektirmeyen, Vanilla JS ve Tailwind CSS ile kurulan, 3D fizik tabanlı zar motoruna (`@3d-dice/dice-box`) ve Web Speech API (TTS) entegrasyonuna sahip tarayıcı arayüzü.

## 🛠️ Kullanılan Teknolojiler

- **Backend:** Python 3.11/3.12, FastAPI, SQLAlchemy, Pydantic, Uvicorn
- **Veritabanı ve Hafıza:** SQLite, ChromaDB
- **Frontend:** HTML5, Vanilla ES6 JavaScript, Tailwind CSS (CDN), Three.js (3D Zar)

## 📦 Kurulum ve Çalıştırma

Projeyi yerel ortamınızda ayağa kaldırmak için:

1. Depoyu klonlayın ve proje dizinine girin:
   ```bash
   git clone [https://github.com/kullaniciadiniz/frp-ai-engine.git](https://github.com/kullaniciadiniz/frp-ai-engine.git)
   cd frp-ai-engine
