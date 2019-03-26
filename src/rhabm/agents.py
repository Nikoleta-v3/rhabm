"""A file which contains classes for the agents involved in the simulation."""
import random
import rhabm

RhinoEmoji = "🦏"
DeadRhinoEmoji = "💀"
PoacherEmoji = "🔪"
CaughtPoacherEmoji = "⛓️"
SecurityEmoji = "🚓"


def euclidean_distance(point_a, point_b):
    """
    Returns the euclidean distance between two points with (i, j) coordinates.
    """
    return (point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2


class Rhino:
    """ A class to represent a rhino agent within the simulation.

    Parameters
    ==========

    park : `Park` instance
        A park instance. The park which is being simulated.
    value : `float`
        The value of the rhino's horn. Value is in [0, 1]. A non dehorn
        rhino has a value of 1.

    Attributes
    ==========
    location : `tuple`
        A tuple of (i, j) coordinates. The current location of the rhino in the park.
    is_mobile : `bool`
        True when the agent is mobile, False eitherwise. A rhino
        becomes immobile once they meet a poacher.
    dead : `bool`
        False when the rhino is alive, True otherwise.
    """

    def __init__(self, park, value=1):
        self.location = park.get_random_unoccupied_cell()
        self.park = park
        self.value = value
        self.park.occupants[self.location[0]][self.location[1]] = self
        self.is_mobile = True
        self.dead = False

    def move(self):
        """
        Method for moving. A rhino identifies whether there are unoccupied cells
        it can move to, and then randomly moves to one.
        """
        if self.is_mobile:
            try:
                new_location = random.choice(
                    [
                        (i, j)
                        for i, j in self.park.get_neighbours(*self.location)
                        if self.park.occupants[i][j].__repr__()
                        == rhabm.UnoccupiedEmoji
                    ]
                )

                self.park.occupants[self.location[0]][
                    self.location[1]
                ] = rhabm.Unoccupied()
                self.location = new_location
                self.park.occupants[self.location[0]][self.location[1]] = self
            except IndexError:
                pass

    def __repr__(self):
        if self.dead is False:
            return RhinoEmoji
        return DeadRhinoEmoji


class Poacher(Rhino):
    """ A class to represent a poacher agent within the simulation.

    Parameters
    ==========

    park : `Park` instance
        A park instance. The park which is being simulated.
    vision_radius : `int`
        The vision radius of a poacher.
    movement_radius : `int`
        The moving radius of a poacher.
    time_to_remove_rhino : `int`
        Time units the poacher needs to remove a horn.
    minimum_horn_value_threshold : `float`
        The threshold for which a poacher will behave selective.
    target_value : `int`
        The amount of rhino horn value the poacher needs to collect before
        leaving the park.

    Attributes
    ==========
    location : `tuple`
        A tuple of (i, j) coordinates. The current location of the poacher in the park.
    is_mobile : `bool`
        True when the agent is mobile, False eitherwise. A poacher
        becomes immobile once they meet a rhino.
    caught : `bool`
        True when the poacher is caught by security, False otherwise.
    """

    def __init__(
        self,
        park,
        vision_radius=3,
        movement_radius=1,
        time_to_remove_rhino=4,
        minimum_horn_value_threshold=0,
        target_value=1,
    ):

        self.vision_radius = vision_radius
        self.time_to_remove_rhino = time_to_remove_rhino
        self.movement_radius = movement_radius
        self.target_agent = None
        self.target_value = target_value
        self.minimum_horn_value_threshold = minimum_horn_value_threshold
        self.caught = False
        super().__init__(park)

    def find_individual(self, target=RhinoEmoji):
        """
        A method for finding target.

        First, poachers check wheather there are rhinos within their radius of
        vision.

        If there are, they check wheather the rhino horn's value is bigger than
        their threshold.

        If there are more than a single rhino that satisfy these conditions,
        then target the rhino which is closer to their current location.

        Method returns `False` if no targets are within the radius of vision.
        """
        target_cells_in_vision = [
            (i, j)
            for i, j in self.park.get_neighbours(
                *self.location, radius=self.vision_radius
            )
            if (self.park.occupants[i][j].__repr__() == target)
            and (
                self.park.occupants[i][j].value
                > self.minimum_horn_value_threshold
            )
        ]
        if len(target_cells_in_vision) > 0:
            target_cells_in_vision.sort(
                key=lambda cell: euclidean_distance(cell, self.location)
            )
            return target_cells_in_vision[0]
        return False

    def move(self):
        """
        A method for moving. A poacher will move towards the closest target
        within their vision.

        If there are no targets within their vision, they move randomly. If
        poachers are next to a rhino they engage the target.
        """
        if self.is_mobile:
            target_cell_in_vision = self.find_individual()
            neighbours = [
                (i, j)
                for i, j in self.park.get_neighbours(
                    *self.location, radius=self.movement_radius
                )
                if self.park.occupants[i][j].__repr__() == rhabm.UnoccupiedEmoji
            ]
            if target_cell_in_vision is not False:
                if target_cell_in_vision in self.park.get_neighbours(
                    *self.location, radius=self.movement_radius
                ):
                    target_agent = self.park.occupants[
                        target_cell_in_vision[0]
                    ][target_cell_in_vision[1]]
                    if target_agent.is_mobile:
                        self.is_mobile = False
                        self.target_agent = target_agent
                        self.target_agent.is_mobile = False
                        return None

                best_next_distance = min(
                    [
                        euclidean_distance(cell, target_cell_in_vision)
                        for cell in neighbours
                    ]
                )
                potential_cells = [
                    cell
                    for cell in neighbours
                    if euclidean_distance(cell, target_cell_in_vision)
                    == best_next_distance
                ]

            else:
                potential_cells = neighbours

            try:
                new_location = random.choice(potential_cells)
                self.park.occupants[self.location[0]][
                    self.location[1]
                ] = rhabm.Unoccupied()
                self.location = new_location
                self.park.occupants[self.location[0]][self.location[1]] = self
            except (IndexError, ValueError) as error:
                pass

        else:
            self.engage_target()

    def engage_target(self):
        """
        If poachers are next to a target they start hunting. While the rhino is
        alive a poacher stays immobile. Once the horn has been removed a poacher
        checks whether the target value has been satisfied. If yes the poacher
        starts exiting the park, otherwise the poacher keeps on hunting.
        """
        if self.caught is False:
            if self.time_to_remove_rhino > 0:
                self.time_to_remove_rhino -= 1
            elif not self.target_agent.dead:
                self.target_agent.dead = True
                self.target_value -= self.target_agent.value
            elif self.target_value <= 0:
                new_location = min(
                    (
                        self.location[0],
                        (
                            self.location[0] - self.movement_radius,
                            self.location[1],
                        ),
                    ),
                    (
                        self.location[1],
                        (
                            self.location[0],
                            self.location[1] - self.movement_radius,
                        ),
                    ),
                    (
                        self.park.width - self.location[0],
                        (
                            self.location[0] + self.movement_radius,
                            self.location[1],
                        ),
                    ),
                    (
                        self.park.height - self.location[1],
                        (
                            self.location[0],
                            self.location[1] + self.movement_radius,
                        ),
                    ),
                    key=lambda pair: pair[0],
                )[1]

                self.park.occupants[self.location[0]][
                    self.location[1]
                ] = rhabm.Unoccupied()
                if (
                    0 <= new_location[0] < self.park.width
                    and 0 <= new_location[1] < self.park.height
                ):
                    self.location = new_location
                    self.park.occupants[self.location[0]][
                        self.location[1]
                    ] = self
            else:
                self.is_mobile = True

    def __repr__(self):
        if self.caught:
            return CaughtPoacherEmoji
        return PoacherEmoji


class SecurityOfficer(Poacher):
    """ A class to represent a security agent within the simulation.

    Parameters
    ==========

    park : `Park` instance
        A park instance. The park which is being simulated.
    vision_radius : `int`
        The vision radius of a security guard.
    movement_radius : `int`
        The moving radius of a security guard.

    Attributes
    ==========
    target_agent : `NoneType` or `Poacher` instance
        None if the security guards has not spotted a poacher. A poacher
        instance once the guard has identify a poacher in the park.
    """

    def __init__(self, park, vision_radius=3, movement_radius=1):

        self.vision_radius = vision_radius
        self.movement_radius = movement_radius
        self.target_agent = None
        super().__init__(park, vision_radius, movement_radius)

    def find_individual(self, target=PoacherEmoji):
        return super().find_individual(target=target)

    def engage_target(self):
        """
        Security guards will engage poachers once they are within their
        neighbourhood.
        
        Poachers are instantly caught and then security continue their watch.
        """
        self.target_agent.caught = True

        try:
            self.target_agent.target_agent.is_mobile = True
        except AttributeError:
            pass

        self.is_mobile = True

    def __repr__(self):
        return SecurityEmoji
