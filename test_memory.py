import os
import sys

# Proje ana dizinini Python yoluna ekleyerek 'app' klasörünün her koşulda bulunmasını garantiye alıyoruz
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.db.database import init_db, SessionLocal, create_campaign, create_character
    from app.db.vector_db import VectorMemory
except ModuleNotFoundError as e:
    print(f"\n[Kritik Hata] Gerekli bir kütüphane eksik: {e}")
    print("Lütfen terminalde şu komutu çalıştırarak paketleri yükleyin:")
    print(".\\venv\\Scripts\\pip install sqlalchemy chromadb fastapi uvicorn")
    sys.exit(1)

def test_systems():
    print("--- 1. SQLite Veritabanı ve CRUD Testi ---")
    try:
        init_db()
        print("Veritabanı tabloları başarıyla oluşturuldu.")
        
        db = SessionLocal()
        campaign = create_campaign(
            db=db,
            name="Gölge Diyarları",
            system="D&D 5e",
            session_zero_data={"tone": "Dark Fantasy"}
        )
        print(f"[SQL] Kampanya Eklendi -> ID: {campaign.id}, İsim: {campaign.name}")
        
        character = create_character(
            db=db,
            campaign_id=campaign.id,
            name="Aelion",
            stats={"HP": 30, "Class": "Rogue"},
            motivations="Kayıp kardeşini bulmak."
        )
        print(f"[SQL] Karakter Eklendi -> ID: {character.id}, İsim: {character.name}")
        db.close()
    except Exception as e:
        print(f"[SQL] İşlem başarısız: {e}")
        
    print("\n--- 2. ChromaDB Vektör RAG Hafıza Testi ---")
    try:
        vector_db = VectorMemory()
        test_campaign_id = "1"
        
        vector_db.add_memory(
            campaign_id=test_campaign_id,
            memory_text="Oyuncular eski kütüphanenin bodrum katında mühürlü bir kadim kitap buldular.",
            event_type="lore"
        )
        print("[ChromaDB] Anı başarıyla vektör veritabanına eklendi.")
        
        results = vector_db.query_memory(
            campaign_id=test_campaign_id,
            query_text="Bodrumda ne buldular?",
            n_results=1
        )
        
        print(f"[ChromaDB] Bulunan Sonuç: {results}")
        print("\nTüm testler başarıyla tamamlandı!")
    except Exception as e:
        print(f"[ChromaDB] İşlem başarısız: {e}")

if __name__ == "__main__":
    test_systems()