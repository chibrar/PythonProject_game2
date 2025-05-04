from eldoria.enums import HunterSkill
from typing import List, Tuple
import random

class Hideout:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.hunters: List[Tuple[int, HunterSkill]] = []  # (hunter_id, skill)
        self.stored_treasure = 0.0
        self.capacity = 5

    def add_hunter(self, hunter_id: int, skill: HunterSkill) -> bool:
        """Add hunter to hideout if space available"""
        if len(self.hunters) < self.capacity:
            self.hunters.append((hunter_id, skill))
            return True
        return False

    def remove_hunter(self, hunter_id: int) -> bool:
        """Remove hunter from hideout"""
        initial_count = len(self.hunters)
        self.hunters = [h for h in self.hunters if h[0] != hunter_id]
        return len(self.hunters) < initial_count

    def store_treasure(self, value: float):
        """Add treasure value to hideout"""
        self.stored_treasure += value

    def try_recruit(self) -> bool:
        """Attempt to recruit new hunter (20% chance with diverse skills)"""
        if 3 <= len(self.hunters) < self.capacity:
            unique_skills = {skill for _, skill in self.hunters}
            return random.random() < 0.2 and len(unique_skills) >= 2
        return False