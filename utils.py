import random
from typing import Tuple, Set
from eldoria.enums import EntityType

def generate_random_position(grid_size: int, existing_positions: Set[Tuple[int, int]]) -> Tuple[int, int]:
    while True:
        x, y = random.randint(0, grid_size-1), random.randint(0, grid_size-1)
        if (x, y) not in existing_positions:
            return x, y

def calculate_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5