from sklearn.tree import DecisionTreeClassifier
import numpy as np

class HunterDecisionModel:
    def __init__(self):
        # Training data: [stamina, treasure_value, knight_distance]
        X = np.array([
            [80, 0.13, 5],   # MOVE (1)
            [30, 0.07, 2],   # FLEE (3)
            [10, 0.03, 1],   # REST (4)
            [50, 0.13, 8],   # MOVE (1)
            [90, 0.13, 10],  # COLLECT (2)
            [20, 0.07, 3]    # FLEE (3)
        ])
        y = np.array([1, 3, 4, 1, 2, 3])  # Action enum values
        self.model = DecisionTreeClassifier()
        self.model.fit(X, y)

    def predict(self, stamina: float, treasure_value: float, distance: float) -> int:
        """Predict action based on current state"""
        return int(self.model.predict([[stamina, treasure_value, distance]])[0])