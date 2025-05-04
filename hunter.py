from typing import Tuple, Dict, Optional
from eldoria.enums import Action, HunterSkill, EntityType
from eldoria.models.treasure import Treasure
from eldoria.ai.decision_tree import HunterDecisionModel
from eldoria.ai.pathfinding import a_star
import math


class TreasureHunter:
    def __init__(self, x: int, y: int, skill: HunterSkill):
        self.x = x
        self.y = y
        self.skill = skill
        self.stamina = 100.0
        self.carried_treasure: Optional[Treasure] = None
        self.memory: Dict[Tuple[int, int], float] = {}
        self.decision_model = HunterDecisionModel()
        self.survival_timer = 3

    def decide_action(self, simulation, nearest_knight: Tuple[int, int]) -> Action:
        """Use simulation object instead of grid to access treasures"""
        # Update memory with visible treasures
        for (x, y), cell_type in simulation.grid.get_adjacent(self.x, self.y).items():
            if cell_type == EntityType.TREASURE:
                for treasure in simulation.treasures:
                    if (x, y) == (treasure.x, treasure.y):
                        self.memory[(x, y)] = treasure.get_value()

        nearest_treasure = simulation.grid.find_nearest((self.x, self.y), EntityType.TREASURE)
        if nearest_treasure == (-1, -1):
            return Action.REST

        knight_dist = math.dist((self.x, self.y), nearest_knight) if nearest_knight != (-1, -1) else float('inf')
        treasure_value = self.memory.get(nearest_treasure, 0)

        action_code = self.decision_model.predict(
            self.stamina,
            treasure_value,
            knight_dist
        )

        try:
            return Action(action_code)
        except ValueError:
            return Action.REST

    def move_toward(self, grid, target: Tuple[int, int]) -> bool:
        if target == (-1, -1):
            return False

        path = a_star(grid, (self.x, self.y), target)
        if path and len(path) > 0:
            new_x, new_y = path[0]

            if grid.cells[new_x][new_y] in [EntityType.EMPTY, EntityType.TREASURE]:
                grid.cells[self.x][self.y] = EntityType.EMPTY
                self.x, self.y = new_x, new_y
                grid.cells[self.x][self.y] = EntityType.HUNTER
                return True
        return False