from typing import List, Dict, Tuple
from eldoria.enums import EntityType


class Grid:
    def __init__(self, size: int = 20):
        self.size = size
        self.cells = [[EntityType.EMPTY for _ in range(size)] for _ in range(size)]

    def add_entity(self, x: int, y: int, entity_type: EntityType):
        self.cells[x % self.size][y % self.size] = entity_type

    def get_adjacent(self, x: int, y: int) -> Dict[Tuple[int, int], EntityType]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return {
            ((x + dx) % self.size, (y + dy) % self.size): self.cells[(x + dx) % self.size][(y + dy) % self.size]
            for dx, dy in directions
        }

    def find_nearest(self, start: Tuple[int, int], target: EntityType) -> Tuple[int, int]:
        from collections import deque
        queue = deque([start])
        visited = set()

        while queue:
            x, y = queue.popleft()
            if self.cells[x][y] == target:
                return (x, y)
            for (nx, ny), _ in self.get_adjacent(x, y).items():
                if (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return (-1, -1)