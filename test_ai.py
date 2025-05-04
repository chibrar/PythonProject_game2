import pytest
from eldoria.ai.decision_tree import HunterDecisionModel
import numpy as np

class TestAI:
    def test_decision_tree(self):
        model = HunterDecisionModel()
        prediction = model.predict(50, 0.13, 3)
        assert prediction in [0, 1, 2, 3]  # COLLECT, MOVE, FLEE, REST