import random
from sklearn.cluster import KMeans
from eldoria.models.grid import Grid
from eldoria.models.hunter import TreasureHunter
from eldoria.models.knight import Knight
from eldoria.models.treasure import Treasure
from eldoria.models.hideout import Hideout
from eldoria.enums import EntityType, HunterSkill, TreasureType, Action
from eldoria.ai.pathfinding import a_star


class EldoriaSimulation:
    def __init__(self, size=20):
        self.grid = Grid(size)
        self.hunters = []
        self.knights = []
        self.treasures = []
        self.hideouts = []
        self.score = 0
        self.game_over = False
        self._initialize_world()

    def _initialize_world(self):
        """Initialize game world with entities"""
        positions = [(x, y) for x in range(self.grid.size) for y in range(self.grid.size)]
        kmeans = KMeans(n_clusters=3, n_init='auto').fit(positions)

        # Create hideouts at cluster centers
        for center in kmeans.cluster_centers_:
            x, y = int(center[0]), int(center[1])
            hideout = Hideout(x, y)
            self.hideouts.append(hideout)
            self.grid.add_entity(x, y, EntityType.HIDEOUT)

        # Spawn hunters (2 per hideout)
        skills = list(HunterSkill)
        for hideout in self.hideouts:
            for _ in range(2):
                x, y = self._find_empty_cell_near(hideout.x, hideout.y)
                if x is not None:
                    hunter = TreasureHunter(x, y, random.choice(skills))
                    self.hunters.append(hunter)
                    self.grid.add_entity(x, y, EntityType.HUNTER)

        # Spawn knights (5 total)
        for _ in range(5):
            x, y = self._find_empty_cell()
            if x is not None:
                knight = Knight(x, y)
                self.knights.append(knight)
                self.grid.add_entity(x, y, EntityType.KNIGHT)

        # Place treasures (20 total)
        for _ in range(20):
            x, y = self._find_empty_cell()
            if x is not None:
                treasure_type = random.choices(
                    list(TreasureType),
                    weights=[0.5, 0.3, 0.2]
                )[0]
                treasure = Treasure(x, y, treasure_type)
                self.treasures.append(treasure)
                self.grid.add_entity(x, y, EntityType.TREASURE)

    def _find_empty_cell(self):
        """Find random empty cell"""
        for _ in range(100):
            x, y = random.randint(0, self.grid.size - 1), random.randint(0, self.grid.size - 1)
            if self.grid.cells[x][y] == EntityType.EMPTY:
                return x, y
        return None, None

    def _find_empty_cell_near(self, center_x, center_y, radius=3):
        """Find empty cell near specified location"""
        for _ in range(50):
            x = (center_x + random.randint(-radius, radius)) % self.grid.size
            y = (center_y + random.randint(-radius, radius)) % self.grid.size
            if self.grid.cells[x][y] == EntityType.EMPTY:
                return x, y
        return None, None

    def run_step(self):
        """Run one simulation step"""
        if self.game_over:
            return

        # Update treasures (decay)
        for treasure in self.treasures[:]:
            if not treasure.decay():
                self.treasures.remove(treasure)
                self.grid.cells[treasure.x][treasure.y] = EntityType.EMPTY

        # Update hunters
        for hunter in self.hunters[:]:
            # Handle stamina and survival
            if hunter.stamina <= 0:
                hunter.survival_timer -= 1
                if hunter.survival_timer <= 0:
                    self._remove_hunter(hunter)
                continue

            # Check if in hideout (resting)
            in_hideout = any((hunter.x, hunter.y) == (h.x, h.y) for h in self.hideouts)
            if in_hideout:
                hunter.stamina = min(100, hunter.stamina + 1)  # Recover stamina
            else:
                # Deduct movement stamina cost
                cost = 1 if hunter.skill == HunterSkill.ENDURANCE else 2
                hunter.stamina = max(0, hunter.stamina - cost)

            # Handle treasure collection
            if hunter.carried_treasure is None:
                for treasure in self.treasures[:]:
                    if (hunter.x, hunter.y) == (treasure.x, treasure.y):
                        hunter.carried_treasure = treasure
                        self.treasures.remove(treasure)
                        self.grid.cells[treasure.x][treasure.y] = EntityType.EMPTY
                        break

            # Handle treasure deposit
            if hunter.carried_treasure is not None:
                for hideout in self.hideouts:
                    if (hunter.x, hunter.y) == (hideout.x, hideout.y):
                        self.score += hunter.carried_treasure.get_value()
                        hunter.carried_treasure = None
                        break

            # Handle knight encounters
            for knight in self.knights[:]:
                if (hunter.x, hunter.y) == (knight.x, knight.y):
                    if hunter.carried_treasure is not None:
                        # Drop treasure
                        dropped = hunter.carried_treasure
                        dropped.x, dropped.y = hunter.x, hunter.y
                        self.treasures.append(dropped)
                        self.grid.cells[hunter.x][hunter.y] = EntityType.TREASURE
                        hunter.carried_treasure = None

                    hunter.stamina = max(0, hunter.stamina - 20)
                    if hunter.stamina <= 0:
                        hunter.survival_timer = 3  # Reset survival timer
                    break

            # AI movement decision
            if not in_hideout and hunter.stamina > 0:
                nearest_knight = self.grid.find_nearest((hunter.x, hunter.y), EntityType.KNIGHT)
                action = hunter.decide_action(self, nearest_knight)

                if action == Action.MOVE:
                    target = self._get_hunter_target(hunter)
                    if target != (-1, -1):
                        hunter.move_toward(self.grid, target)
                elif action == Action.REST:
                    nearest_hideout = self.grid.find_nearest((hunter.x, hunter.y), EntityType.HIDEOUT)
                    if nearest_hideout != (-1, -1):
                        hunter.move_toward(self.grid, nearest_hideout)

        # Update knights
        for knight in self.knights:
            knight.patrol(self.grid)

        # Check game over conditions
        self._check_game_over()

    def _remove_hunter(self, hunter):
        """Remove hunter from simulation"""
        self.hunters.remove(hunter)
        self.grid.cells[hunter.x][hunter.y] = EntityType.EMPTY

    def _get_hunter_target(self, hunter):
        """Determine hunter's target based on current state"""
        if hunter.carried_treasure:
            return self.grid.find_nearest((hunter.x, hunter.y), EntityType.HIDEOUT)
        return self.grid.find_nearest((hunter.x, hunter.y), EntityType.TREASURE)

    def _check_game_over(self):
        """Check if game should end"""
        no_treasures = not self.treasures
        no_carried = all(h.carried_treasure is None for h in self.hunters)

        if (no_treasures and no_carried) or not self.hunters:
            self.game_over = True