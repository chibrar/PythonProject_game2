import math
from typing import List, Tuple, Dict
from heapq import heappop, heappush
from eldoria.enums import EntityType

def a_star(grid, start: Tuple[int, int], goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    """A* pathfinding algorithm"""
    open_set = []
    heappush(open_set, (0, start))
    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score = {start: 0}
    f_score = {start: math.dist(start, goal)}

    while open_set:
        _, current = heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for neighbor, cell_type in grid.get_adjacent(*current).items():
            if cell_type == EntityType.KNIGHT:  # Avoid knights
                continue
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + math.dist(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))
    return []  # No path found