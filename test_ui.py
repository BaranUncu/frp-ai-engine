import asyncio
import json
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 1. WEBSOCKET ROTASI: İletişim Tüneli
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Bağlantı başarılı: İstemci (Frontend) bağlandı.")
    
    try:
        while True:
            # A. Frontend'den gelen mesajı bekle ve JSON formatından Python sözlüğüne (dictionary) çevir
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            
            print(f"Frontend'den gelen veri: {data}")

            response_text = ""
            
            # B. Gelen mesajın tipine göre sahte (mock) bir senaryo uydur
            if data.get("type") == "chat":
                user_msg = data.get("content")
                response_text = f"Sistem mesajını aldı: '{user_msg}'. Karanlık ormanda rüzgar uğulduyor... Ne yapacaksın?"
                
            elif data.get("type") == "roll_result":
                total = data.get("total")
                notation = data.get("notation")
                if total >= 10:
                    response_text = f"Harika! {notation} attın ve {total} geldi. Kılıcınla goblini başarıyla alt ettin."
                else:
                    response_text = f"Eyvah... {notation} attın ama {total} geldi. Ayağın takıldı ve yere düştün."

            # C. Yanıtı sanki bir yapay zeka üretiyormuş gibi kelime kelime parçala (Streaming simülasyonu)
            words = response_text.split()
            for word in words:
                # Her kelimeyi 'stream' etiketiyle frontend'e yolla. Sonuna boşluk ekliyoruz ki kelimeler yapışmasın.
                await websocket.send_text(json.dumps({"type": "stream", "content": word + " "}))
                # Daktilo animasyonunu insan gözüyle görebilmek için kodun çalışmasını 0.1 saniye beklet
                await asyncio.sleep(0.1) 
            
            # D. Mesajın bittiğini frontend'e bildir (app.js'deki yanıp sönen imleci durdurmak için)
            await websocket.send_text(json.dumps({"type": "done"}))

    except WebSocketDisconnect:
        print("İstemci (Frontend) bağlantıyı kopardı veya sayfayı yeniledi.")

# 2. STATİK DOSYA SUNUCUSU: Frontend dosyalarını dışa açar
# Dikkat: Bunu en alta yazıyoruz ki "/ws" rotasını statik bir dosya sanıp engellemesin.
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Sunucuyu yerel bilgisayarda 8000 portunda başlat
    uvicorn.run(app, host="127.0.0.1", port=8000)