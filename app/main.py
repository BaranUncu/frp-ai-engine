# Tüm import'lar dosyanın en üstünde olmak zorundadır
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.router_ws import router as ws_router

# 1. FastAPI Uygulamasını Başlat
app = FastAPI(
    title="FRP AI Game Master Engine",
    description="Multi-System FRP AI GM with WebSockets and RAG Memory",
    version="1.0.0"
)

# 2. ÖNCE WebSocket ve API rotalarını ekle
app.include_router(ws_router)

# 3. Kök dizin (/) için basit bir kontrol fonksiyonu (Sistemin çalıştığını görmek için)
@app.get("/status")
async def root():
    return {"status": "ok", "message": "FRP Engine aktif. WebSocket: ws://localhost:8000/ws/game"}

# 4. EN SON statik dosyaları (HTML, JS, CSS) ekle.
# (Bunu en sona yazıyoruz ki, yukarıdaki rotalarla çakışmasın)
app.mount("/", StaticFiles(directory="static", html=True), name="static")