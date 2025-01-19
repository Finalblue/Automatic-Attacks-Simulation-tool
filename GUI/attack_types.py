from enum import Enum, auto
from dataclasses import dataclass
from typing import Callable

class AttackType(Enum):
   DIRECT = auto()
   PROXY = auto()

@dataclass
class Attack:
   name: str
   type: AttackType
   function: Callable