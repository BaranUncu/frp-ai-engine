import asyncio
import websockets

async def test_game_loop():
    # FastAPI sunucumuzun adresi
    uri = "ws://127.0.0.1:8000/ws/game"
    print(f"Sunucuya bağlanılıyor: {uri}")

    try:
        # Sunucuyla bağlantı kur
        async with websockets.connect(uri) as websocket:
            print("Bağlantı başarılı! (Çıkmak için 'quit' yazın)\n")

            while True:
                # Oyuncudan (senden) terminal üzerinden girdi al
                action = input("Sen: ")
                
                if action.lower() in ['quit', 'exit']:
                    print("Oyundan çıkılıyor...")
                    break

                # Girdiyi sunucuya gönder
                await websocket.send(action)

                print("GM: ", end="", flush=True)
                
                # Sunucudan gelen cevapları dinle
                while True:
                    response = await websocket.recv()
                    
                    # Sunucu akışın bittiğini bildirdiğinde döngüyü kır
                    if response == "[DONE]":
                        print("\n" + "-"*40) # Görsellik için alt tire çiz
                        break
                    
                    # Gelen kelimeleri yan yana (alt satıra inmeden) yazdır
                    print(response, end="", flush=True)
                    
    except ConnectionRefusedError:
        print("Hata: Sunucuya ulaşılamıyor. FastAPI'nin çalıştığından emin ol (uvicorn app.main:app).")

if __name__ == "__main__":
    asyncio.run(test_game_loop())