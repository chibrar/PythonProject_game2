from enum import Enum, auto

class EntityType(Enum):
    EMPTY = auto()
    TREASURE = auto()
    HUNTER = auto()
    KNIGHT = auto()
    HIDEOUT = auto()

class TreasureType(Enum):
    BRONZE = (0.03, '#CD7F32')  # (value multiplier, color)
    SILVER = (0.07, '#C0C0C0')
    GOLD = (0.13, '#FFD700')

    @property
    def value_multiplier(self):
        return self.value[0]

    @property
    def color(self):
        return self.value[1]

class HunterSkill(Enum):
    NAVIGATION = auto()
    ENDURANCE = auto()
    STEALTH = auto()

class Action(Enum):
    MOVE = 1
    COLLECT = 2
    FLEE = 3
    REST = 4