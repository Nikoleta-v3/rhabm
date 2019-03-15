import itertools
import random

UnoccupiedEmoji = "🌲"


class Park:
    """ A class to represent the wildlife park which is being simulated.

    Parameters
    ==========

    width : `int`
        The park's width.
    height : `int`
        The park's height.

    Attributes
    ==========
    occupants : `tuple`
        A tuple of (i, j) coordinates. The current location of the rhino in the park.
    coordinates : `bool`
        True when the agent is mobile, False eitherwise. A rhino
        becomes immobile once they meet a poacher.
    """

    def __init__(self, width=5, height=5):
        self.occupants = [
            [UnoccupiedEmoji for _ in range(width)] for _ in range(height)
        ]
        self.width = width
        self.height = height
        self.coordinates = list(itertools.product(range(width), range(height)))

    def get_random_unoccupied_cell(self):
        """
        Returns the coordinates of a random unoccupied cell.
        """
        random.shuffle(self.coordinates)
        for i, j in self.coordinates:
            if self.occupants[i][j] == UnoccupiedEmoji:
                return i, j
        return False

    def get_neighbours(self, i, j, radius=1):
        neighbours = []

        for offset in range(min(self.width - j, radius + 1)):
            for step in range(min(self.height - 1 - i, radius - offset) + 1):
                if (step, offset) != (0, 0):
                    neighbours.append((i + step, j + offset))

        for offset in range(min(self.width - j, radius + 1)):
            for step in range(1, min(i, radius - offset) + 1):
                if (step, offset) != (0, 0):
                    neighbours.append((i - step, j + offset))

        for offset in range(1, min(j, radius + 1) + 1):
            for step in range(min(self.height - 1 - i, radius - offset) + 1):
                if (step, offset) != (0, 0):
                    neighbours.append((i + step, j - offset))

        for offset in range(1, min(j, radius + 1) + 1):
            for step in range(1, min(i, radius - offset) + 1):
                if (step, offset) != (0, 0):
                    neighbours.append((i - step, j - offset))

        return neighbours

    def __len__(self):
        return self.width * self.height

    def __repr__(self):
        repr = ""
        for row in self.occupants:
            repr += f"{str(row)}\n"
        return repr
