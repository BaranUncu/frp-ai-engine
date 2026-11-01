import uuid
from typing import List, Dict, Any, Literal, Optional
from pydantic import BaseModel, Field

# --- VERİ ŞEMALARI (MODELS) ---

class PlayerPreferences(BaseModel):
    """Oyuncunun oyun dışı konfor alanını (kırmızı çizgilerini) tutar."""
    lines: List[str] = Field(default_factory=list)
    veils: List[str] = Field(default_factory=list)
    playstyle_focus: str = Field(default="Dengeli")

class Player(BaseModel):
    """Fiziksel oyuncuyu temsil eder."""
    player_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    preferences: PlayerPreferences

class CharacterBase(BaseModel):
    """Sistemden bağımsız temel karakter verisini tutar."""
    character_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    player_id: str
    name: str
    system: Literal['dnd5e', 'coc', 'fate']
    backstory: str
    motivations: List[str]
    attributes: Dict[str, Any] = Field(default_factory=dict)

class Campaign(BaseModel):
    """Oyunun geçtiği evrenin ve hikayenin ana çerçevesini tutar."""
    campaign_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    active_system: Literal['dnd5e', 'coc', 'fate']
    tone: str
    setting_description: str

class SessionZeroConfig(BaseModel):
    """Tüm Session 0 verisini tek bir pakette tutan ana konfigürasyon."""
    campaign: Campaign
    players: List[Player] = Field(default_factory=list)
    characters: List[CharacterBase] = Field(default_factory=list)


# --- İŞ MANTIĞI (BUSINESS LOGIC) ---

class SessionZeroManager:
    """
    Session 0 sürecini yöneten, verileri doğrulayan ve birleştiren ana kontrolcü sınıf.
    """
    def __init__(self, campaign: Campaign):
        """Yeni bir Session 0 süreci başlatır ve boş listeler oluşturur."""
        self.config = SessionZeroConfig(
            campaign=campaign,
            players=[],
            characters=[]
        )

    def add_player(self, name: str, lines: List[str], veils: List[str], focus: str) -> Player:
        """Yeni bir oyuncu oluşturur ve konfigürasyona ekler."""
        prefs = PlayerPreferences(lines=lines, veils=veils, playstyle_focus=focus)
        new_player = Player(name=name, preferences=prefs)
        
        self.config.players.append(new_player)
        return new_player

    def add_character(self, player_id: str, name: str, backstory: str, motivations: List[str], attributes: Dict[str, Any]) -> CharacterBase:
        """
        Karakter oluşturur. Öncesinde oyuncunun var olup olmadığını ve
        sistemin campaign sistemiyle uyuşup uyuşmadığını kontrol eder.
        """
        # Oyuncu sistemde kayıtlı mı kontrolü
        player_exists = any(p.player_id == player_id for p in self.config.players)
        if not player_exists:
            raise ValueError(f"Hata: {player_id} ID'li oyuncu bulunamadı. Önce oyuncuyu ekleyin.")

        new_character = CharacterBase(
            player_id=player_id,
            name=name,
            system=self.config.campaign.active_system, # Sistemi campaign'den otomatik çeker
            backstory=backstory,
            motivations=motivations,
            attributes=attributes
        )
        
        self.config.characters.append(new_character)
        return new_character

    def get_ai_context(self) -> str:
        """
        Oluşturulan tüm Session 0 verisini, yapay zekaya (LLM) prompt olarak 
        verilebilecek özet bir metne dönüştürür.
        """
        context = f"Campaign: {self.config.campaign.title} ({self.config.campaign.tone})\n"
        context += f"Setting: {self.config.campaign.setting_description}\n"
        context += f"System: {self.config.campaign.active_system}\n\n"
        
        context += "--- PLAYERS & BOUNDARIES ---\n"
        for p in self.config.players:
            context += f"Player: {p.name} | Lines: {', '.join(p.preferences.lines)} | Veils: {', '.join(p.preferences.veils)}\n"
            
        context += "\n--- CHARACTERS ---\n"
        for c in self.config.characters:
            context += f"Character: {c.name} | Motivations: {', '.join(c.motivations)}\n"
            context += f"Backstory: {c.backstory[:100]}...\n" # Hikayenin ilk 100 karakteri
            
        return context