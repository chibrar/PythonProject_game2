import pytest
from eldoria.models.grid import Grid
from eldoria.enums import EntityType


class TestGrid:
    @pytest.fixture
    def grid(self):
        return Grid(20)

    def test_grid_initialization(self, grid):
        assert len(grid.cells) == 20
        assert all(cell == EntityType.EMPTY for row in grid.cells for cell in row)

    def test_add_entity(self, grid):
        grid.add_entity(5, 5, EntityType.HUNTER)
        assert grid.cells[5][5] == EntityType.HUNTER

    def test_wrap_around(self, grid):
        grid.add_entity(25, 25, EntityType.KNIGHT)
        assert grid.cells[5][5] == EntityType.KNIGHT