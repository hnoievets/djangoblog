from enum import Enum
from typing import Type, List, Tuple, Any


type Choice = Tuple[Any, str]

def get_choices_from_enum(enum: Type[Enum]) -> List[Choice]:
    return [(member.value, member.name) for member in enum]