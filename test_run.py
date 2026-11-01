from app.core.dice_parser import roll_dice
# İçe aktarma yolu klasör yapına (systems) uygun olarak düzeltildi:
from app.core.systems.base_system import BaseRuleEngine, ActionRequest, ActionResult
from app.core.session_zero import Campaign, SessionZeroManager

print("="*40)
print("1. ZAR MOTORU (DICE PARSER) TESTİ")
print("="*40)
try:
    print(f"D&D Zarı (1d20+5): {roll_dice('1d20+5').model_dump()}")
    print(f"Fate Zarı (4df): {roll_dice('4df').model_dump()}")
    print(f"CoC Zarı (1d100): {roll_dice('1d100').model_dump()}")
except Exception as e:
    print(f"Zar Motoru Hatası: {e}")

print("\n" + "="*40)
print("2. BASE SYSTEM (SOYUT SINIF) TESTİ")
print("="*40)
class DummyTestEngine(BaseRuleEngine):
    @property
    def system_name(self) -> str:
        return "Dummy Test Sistemi"

    def calculate_target_number(self, base_stat: int, modifiers: dict) -> int:
        return base_stat + sum(modifiers.values())

    def resolve_action(self, character_stats: dict, action_request: ActionRequest) -> ActionResult:
        return ActionResult(
            is_success=True,
            margin=5,
            description="Test motoru aksiyonu başarıyla çözdü.",
            roll_data={"zar_sonucu": 15}
        )

try:
    engine = DummyTestEngine()
    req = ActionRequest(action_type="gözlem", dice_expression="1d20", context_modifiers={"isik": -2})
    res = engine.resolve_action(character_stats={"algı": 14}, action_request=req)
    
    print(f"Sistem Adı: {engine.system_name}")
    print(f"Aksiyon Sonucu: Başarılı mı? {res.is_success} | Detay: {res.description}")
except Exception as e:
    print(f"Sistem Motoru Hatası: {e}")

print("\n" + "="*40)
print("3. SESSION 0 VE VERİ YÖNETİMİ TESTİ")
print("="*40)
try:
    campaign = Campaign(
        title="Unutulmuş Diyarlar",
        active_system="dnd5e",
        tone="Karanlık Fantezi",
        setting_description="Büyünün yozlaştığı, tehlikeli bir krallık."
    )
    manager = SessionZeroManager(campaign)

    player = manager.add_player(
        name="Baran", 
        lines=["Çocuk istismarı"], 
        veils=["Aşırı vahşet/gore"], 
        focus="%60 Rol yapma, %40 Taktiksel savaş"
    )
    print(f"Oyuncu Eklendi: {player.name} (ID: {player.player_id})")

    character = manager.add_character(
        player_id=player.player_id,
        name="Kael",
        backstory="Eski bir paralı asker, şimdi günahlarına kefaret arıyor.",
        motivations=["Bağışlanmak", "Krallığı devirmek"],
        attributes={"STR": 16, "DEX": 14, "CON": 15, "INT": 10, "WIS": 12, "CHA": 8}
    )
    print(f"Karakter Eklendi: {character.name} (Sistem: {character.system})")

    print("\n--- AI (LLM) İÇİN OLUŞTURULAN BAĞLAM (CONTEXT) ---")
    print(manager.get_ai_context())

except Exception as e:
    print(f"Session 0 Hatası: {e}")