import DiceBox from '/dice-box.es.min.js';
// DOM Elementleri
const chatContainer = document.getElementById('chat-container');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

// State
let ttsBuffer = "";
let ws;
let currentAiMessageDiv = null;
let currentAiMessageContent = null;
let diceReady = false; // Zar motorunun aktif olup olmadığını takip edeceğiz


// 1. WebSocket'i HEMEN BAŞLAT (Zarları bekleme!)
initWebSocket();

// Zar Motoru Konfigürasyonu
const diceBox = new DiceBox({
    container: "#dice-box",
    assetPath: "/assets/", 
    theme: "default",
    themeColor: "#4f46e5",
    scale: 6
});

// 2. Zar motorunu arka planda başlat, hata olursa yakala
diceBox.init().then(() => {
    console.log("3D Zarlar başarıyla yüklendi.");
    diceReady = true;
}).catch((error) => {
    console.error("Zar motoru yüklenirken güvenlik/CORS hatası oluştu:", error);
    addMessage("Sistem Uyarı: 3D Zar görselleştirmesi yüklenemedi. Zarlar düz metin olarak hesaplanacak.", 'system');
});

function initWebSocket() {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    // Dinamik host, doğru adresi bulmasını sağlar
    ws = new WebSocket(`ws://${window.location.host}/ws/game`);

    ws.onopen = () => {
        chatContainer.innerHTML = ''; 
        addMessage("Sistem: Bağlantı kuruldu. AI Game Master hazır.", 'system');
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // 1. EĞER GELEN VERİ METİN İSE (Token)
        if (data.type === 'token') {
            // Daktilo efekti UI başlangıcı
            if (!currentAiMessageDiv) {
                currentAiMessageDiv = addMessage("", 'ai', true);
                currentAiMessageContent = currentAiMessageDiv.querySelector('.msg-content');
            }
            
            // UI'a kelimeyi ekle
            const chunk = data.content;
            currentAiMessageContent.textContent += chunk;
            scrollToBottom();

            // TTS Seslendirme İçin Tampona Ekle
            ttsBuffer += chunk;
            // Cümle bitiş işaretini görüyorsa oku ve tamponu sıfırla
            if (/[.?!]\s*$/.test(ttsBuffer)) {
                // Eğer gameMasterTTS tanımlıysa (audio.js yüklenmişse) çalıştır
                if (typeof gameMasterTTS !== 'undefined') {
                    gameMasterTTS.speak(ttsBuffer);
                }
                ttsBuffer = "";
            }
        } 
        
        // 2. EĞER GELEN VERİ GÖRSEL İSE (Arkaplanı Değiştir)
        else if (data.type === 'image') {
            const bgElement = document.getElementById('scene-background');
            if (bgElement) {
                bgElement.style.backgroundImage = `url('${data.url}')`;
            }
        }
        
        // 3. EĞER GELEN VERİ "BİTTİ" SİNYALİ İSE
        else if (data.type === 'done') {
            if (currentAiMessageDiv) {
                currentAiMessageDiv.classList.remove('cursor');
                currentAiMessageDiv = null;
                currentAiMessageContent = null;
            }
        }
    };

    ws.onclose = () => {
        addMessage("Sistem: Bağlantı koptu. Lütfen sayfayı yenileyin.", 'system');
    };
}

function addMessage(text, sender, isStreaming = false) {
    const msgDiv = document.createElement('div');
    
    msgDiv.className = `p-3 rounded-lg max-w-[80%] ${
        sender === 'user' ? 'bg-indigo-600 text-white self-end rounded-br-none' : 
        sender === 'ai' ? 'bg-gray-700 text-gray-200 self-start rounded-bl-none' : 
        'bg-gray-800 text-gray-400 self-center text-sm w-full text-center'
    }`;

    if (isStreaming) {
        msgDiv.classList.add('cursor');
    }

    const contentSpan = document.createElement('span');
    contentSpan.className = 'msg-content whitespace-pre-wrap';
    contentSpan.textContent = text;
    
    msgDiv.appendChild(contentSpan);
    chatContainer.appendChild(msgDiv);
    scrollToBottom();
    
    return msgDiv;
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function handleSend() {
    const text = chatInput.value.trim();
    if (!text) return;

    chatInput.value = '';
    
    const rollMatch = text.match(/^\/roll\s+(.+)$/i);
    if (rollMatch) {
        const notation = rollMatch[1];
        addMessage(`Sen: Zar atılıyor (${notation})...`, 'user');
        
        if (diceReady) {
            try {
                const result = await diceBox.roll(notation);
                console.log("Zar Motoru Çıktısı:", result); // F12 Konsolunda yapıyı görmek için
                
                let total = 0;
                let individualRolls = [];
                
                // Kütüphane bazen objeyi dizi, bazen tek obje döner. İkisini de kapsayalım:
                const groups = Array.isArray(result) ? result : [result];
                
                groups.forEach(group => {
                    // Eğer group.value varsa direkt toplamı verir, detaylar group.rolls içindedir
                    if (group.rolls && Array.isArray(group.rolls)) {
                        group.rolls.forEach(roll => {
                            individualRolls.push(roll.value);
                        });
                    }
                    total += group.value || 0; // Kütüphane toplamı direkt group.value içinde saklar
                });

                const detailText = individualRolls.length > 1 ? ` [${individualRolls.join(', ')}]` : '';
                addMessage(`Zar Sonucu: ${total}${detailText}`, 'system');
                
                // Sonucu backend'e ilet (sadece total gitmesi şimdilik yeterli)
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({ type: "roll_result", notation: notation, total: total }));
                }
                
                // 4. Zarları 2 saniye (2000 milisaniye) sonra ekrandan sil
                setTimeout(() => {
                    diceBox.clear();
                }, 2000);

            } catch (error) {
                console.error("Zar Hatası:", error);
                addMessage("Zar formülünü (örn: 1d20, 2d6) yanlış yazdın.", 'system');
                // Hata durumunda da ekranda sıkışan zar kaldıysa temizle
                diceBox.clear(); 
            }
        } else {
            addMessage(`(3D Kapalı) Sistem zarı manuel olarak arka planda işleyecek.`, 'system');
        }
    } else {
        addMessage(text, 'user');
        if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "chat", content: text }));
        }
    }
}

sendBtn.addEventListener('click', handleSend);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleSend();
});