from eldoria.enums import TreasureType

class Treasure:
    def __init__(self, x: int, y: int, treasure_type: TreasureType):
        self.x = x
        self.y = y
        self.type = treasure_type
        self.value = 100.0  # Base value

    def decay(self) -> bool:
        """Reduce treasure value by 0.1% each step"""
        self.value = max(0, self.value - 0.1)
        return self.value > 0

    def get_value(self) -> float:
        """Get current value with type multiplier"""
        return self.value * self.type.value_multiplier