from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel

class ActionRequest(BaseModel):
    action_type: str
    dice_expression: str
    context_modifiers: Dict[str, int] = {}

class ActionResult(BaseModel):
    is_success: bool
    margin: int  # Başarı veya başarısızlık marjı 
    description: str
    roll_data: dict

class BaseRuleEngine(ABC):
    """
    Tüm FRP sistem motorlarının miras alması gereken temel sınıf.
    """
    
    @property
    @abstractmethod
    def system_name(self) -> str:
        pass

    @abstractmethod
    def calculate_target_number(self, base_stat: int, modifiers: Dict[str, int]) -> int:
        """
        Zorluk seviyesini (D&D için DC, CoC için yetenek değeri) hesaplar.
        """
        pass

    @abstractmethod
    def resolve_action(self, character_stats: Dict[str, Any], action_request: ActionRequest) -> ActionResult:
        """
        Karakter yetenekleri ve atılan zara göre aksiyonun sonucunu döner.
        """
        pass