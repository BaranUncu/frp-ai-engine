class TTSManager {
    constructor() {
        this.synth = window.speechSynthesis;
        this.voice = null;
        this.queue = [];
        this.isPlaying = false;
        this.initVoice();
    }

    initVoice() {
        // Tarayıcıdaki Türkçe veya varsayılan İngilizce sesi seçer
        const setVoice = () => {
            const voices = this.synth.getVoices();
            this.voice = voices.find(v => v.lang.includes('tr')) || voices[0];
        };
        
        setVoice();
        if (this.synth.onvoiceschanged !== undefined) {
            this.synth.onvoiceschanged = setVoice;
        }
    }

    speak(text) {
        if (!text || text.trim() === '') return;
        this.queue.push(text.trim());
        this.processQueue();
    }

    processQueue() {
        if (this.isPlaying || this.queue.length === 0) return;
        this.isPlaying = true;

        const text = this.queue.shift();
        const utterance = new SpeechSynthesisUtterance(text);
        
        if (this.voice) utterance.voice = this.voice;
        utterance.rate = 1.0; // Konuşma hızı
        utterance.pitch = 1.0; // Ses tonu

        utterance.onend = () => {
            this.isPlaying = false;
            this.processQueue(); // Kuyruktaki sonraki cümleye geç
        };

        utterance.onerror = (e) => {
            console.error("TTS Hatası:", e);
            this.isPlaying = false;
            this.processQueue();
        };

        this.synth.speak(utterance);
    }

    stop() {
        this.synth.cancel();
        this.queue = [];
        this.isPlaying = false;
    }
}

// Global olarak erişilebilir örnek
const gameMasterTTS = new TTSManager();