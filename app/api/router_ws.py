from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.llm_service import LLMService
import json
import urllib.parse  # YENİ: URL'deki boşlukları %20 formatına çevirmek için
import asyncio
router = APIRouter()

@router.websocket("/ws/game")
async def game_websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # İstemciden aksiyon/mesaj bekle
            data = await websocket.receive_text()
            
            # TODO: Phase 1 & 2 Entegrasyonu
            # 1. Gelen mesajı parse et (Zar var mı? -> dice_parser.py)
            # 2. Vektör DB'den benzer geçmişi getir (-> vector_db.py)
            # 3. Session 0 sınırlarını kontrol et (-> session_zero.py)
            rag_context = "Önceki odada bir goblin cesedi bulunmuştu." 
            
            # ---------------- YENİ EKLENEN KISIM (GÖRSEL SİNYALİ) ----------------
            # Yapay zeka yazmaya başlamadan önce mekanı belirleyip arkaplanı değiştiriyoruz.
            # (Şimdilik sabit, ileride LLM'e 'bana ortamı anlatan ingilizce bir kelime grubu ver' diyebilirsin)
            scene_prompt = "dark fantasy dungeon with a dead goblin on the floor, cinematic lighting, 4k"
            
            # URL'de boşluk olamayacağı için boşlukları güvenli formata (%20) çeviriyoruz
            safe_prompt = urllib.parse.quote(scene_prompt) 
            image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
            
            # Frontend'e arkaplanı değiştirmesi için JSON emrini yolluyoruz
            await websocket.send_json({
                "type": "image",
                "url": image_url
            })
            # ---------------------------------------------------------------------

            # Not: llm_generator'ın senin kodunda LLMService tarafından üretildiğini varsayıyoruz
            # Örn: llm_generator = LLMService.generate(...)
            
            # LLM streaming yanıtını istemciye parça parça gönder
            async def mock_llm_generator():
                test_sentence = "Maceracılar, karanlık mağaraya adım attınız. Yerlerde kemikler var! Geri mi döneceksiniz? Yoksa devam mı edeceksiniz?"
                # Metni boşluklara göre kelime kelime böl ve yolla
                for word in test_sentence.split():
                    yield word + " " 
                    await asyncio.sleep(0.3) # Daktilo efekti için her kelimede 0.3 saniye bekle

            # llm_generator = mock_llm_generator() # Fonksiyonu çağır ve değişkene ata
            llm_generator = mock_llm_generator()

            async for chunk in llm_generator:
                await websocket.send_json({
                    "type": "token",
                    "content": chunk
                })
            # ---------------------------------------------------------------------------------
            
    except WebSocketDisconnect:
        print("İstemci (Oyuncu) bağlantıyı kesti.")
    except Exception as e:
        print(f"Beklenmeyen Hata: {e}")
        await websocket.close()