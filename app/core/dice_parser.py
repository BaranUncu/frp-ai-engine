import re
import random
from pydantic import BaseModel
from typing import List

class RollResult(BaseModel):
    expression: str
    total: int
    rolls: List[int]
    modifier: int
    is_fate: bool = False

def roll_dice(expression: str) -> RollResult:
    """
    Standart poliedrik ve Fate (dF) zarlarını ayrıştırıp hesaplar.
    """
    expression_clean = expression.replace(" ", "").lower()
    # Örüntü: Opsiyonel sayı, 'd', 'f' veya sayı, opsiyonel işaret ve modifiye
    pattern = r'^(\d+)?d(f|\d+)(?:([\+\-])(\d+))?$'
    match = re.match(pattern, expression_clean)

    if not match:
        raise ValueError(f"Geçersiz zar formatı: {expression}")

    num_dice_str, die_type, sign, modifier_str = match.groups()
    
    num_dice = int(num_dice_str) if num_dice_str else 1
    modifier = int(modifier_str) if modifier_str else 0
    if sign == '-':
        modifier = -modifier

    rolls = []
    is_fate = (die_type == 'f')

    for _ in range(num_dice):
        if is_fate:
            # Fate zarları: -1, 0, +1
            rolls.append(random.randint(-1, 1))
        else:
            sides = int(die_type)
            if sides < 2:
                raise ValueError(f"Geçersiz zar yüzeyi: {sides}")
            rolls.append(random.randint(1, sides))

    total = sum(rolls) + modifier

    return RollResult(
        expression=expression_clean,
        total=total,
        rolls=rolls,
        modifier=modifier,
        is_fate=is_fate
    )