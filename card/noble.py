from typing import Dict

from marshmallow_dataclass import dataclass as mmdc


@mmdc
class Noble:
    points: int
    # CardColor
    cost: Dict[str, int]
