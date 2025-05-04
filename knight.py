import random
from eldoria.enums import EntityType
from eldoria.ai.pathfinding import a_star

class Knight:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.energy = 100.0

    def patrol(self, grid):
        """Knight's movement behavior"""
        if self.energy <= 20:
            self._return_to_garrison(grid)
        else:
            self._random_move(grid)

    def _random_move(self, grid):
        """Move randomly when patrolling"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = (self.x + dx) % grid.size
            new_y = (self.y + dy) % grid.size
            if grid.cells[new_x][new_y] == EntityType.EMPTY:
                grid.cells[self.x][self.y] = EntityType.EMPTY
                self.x, self.y = new_x, new_y
                grid.cells[new_x][new_y] = EntityType.KNIGHT
                self.energy = max(0, self.energy - 10)
                break

    def _return_to_garrison(self, grid):
        """Return to nearest hideout to recover energy"""
        garrison = grid.find_nearest((self.x, self.y), EntityType.HIDEOUT)
        if garrison != (-1, -1):
            path = a_star(grid, (self.x, self.y), garrison)
            if path and len(path) > 0:
                grid.cells[self.x][self.y] = EntityType.EMPTY
                self.x, self.y = path[0]
                grid.cells[self.x][self.y] = EntityType.KNIGHT
        self.energy = min(100, self.energy + 5)