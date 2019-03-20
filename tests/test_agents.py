import random

import pytest

import rhabm


def test_euclidean_distance():
    point_a = (0, 1)
    point_b = (2, 4)

    distance = rhabm.euclidean_distance(point_a, point_b)
    assert distance == 13


def test_rhino_init():
    park = rhabm.Park()
    rhino_agent = rhabm.Rhino(park=park, value=0.8)

    assert isinstance(rhino_agent.park, rhabm.Park)
    assert isinstance(rhino_agent.location, tuple)

    assert len(rhino_agent.location) == 2
    assert rhino_agent.value == 0.8

    assert rhino_agent.is_mobile
    assert rhino_agent.dead is False


def test_rhino_move():
    park = rhabm.Park()
    rhino_agent = rhabm.Rhino(park=park)

    rhino_agent.location = (1, 1)
    rhino_agent.move()

    assert rhino_agent.location in [(1, 0), (1, 2), (0, 1), (2, 1)]
    assert (
        str(park.occupants[rhino_agent.location[0]][rhino_agent.location[1]])
        == rhabm.RhinoEmoji
    )


def test_rhino_repr():
    park = rhabm.Park()

    rhino_agent = rhabm.Rhino(park=park, value=0.8)
    assert rhino_agent.__repr__() == rhabm.RhinoEmoji

    rhino_agent.dead = True
    assert rhino_agent.__repr__() == rhabm.DeadRhinoEmoji


def test_poacher_init_default():
    park = rhabm.Park()
    poacher_agent = rhabm.Poacher(park=park)

    assert poacher_agent.vision_radius == 3
    assert poacher_agent.movement_radius == 1
    assert poacher_agent.time_to_remove_rhino == 4
    assert poacher_agent.minimum_horn_value_threshold == 0
    assert poacher_agent.target_value == 1

    assert isinstance(poacher_agent.park, rhabm.Park)
    assert isinstance(poacher_agent.location, tuple)

    assert len(poacher_agent.location) == 2

    assert poacher_agent.is_mobile
    assert poacher_agent.caught is False


def test_poacher_init():
    park = rhabm.Park()
    poacher_agent = rhabm.Poacher(
        park=park,
        vision_radius=2,
        movement_radius=2,
        time_to_remove_rhino=5,
        minimum_horn_value_threshold=0.5,
        target_value=2,
    )

    assert poacher_agent.vision_radius == 2
    assert poacher_agent.movement_radius == 2
    assert poacher_agent.time_to_remove_rhino == 5
    assert poacher_agent.minimum_horn_value_threshold == 0.5
    assert poacher_agent.target_value == 2


def test_poacher_move_randomly_with_no_target():
    park = rhabm.Park()

    poacher_agent = rhabm.Poacher(park=park, movement_radius=1)
    poacher_agent.location = (1, 1)
    poacher_agent.move()

    assert poacher_agent.location in [(1, 0), (1, 2), (0, 1), (2, 1)]


def test_poacher_move_towards_rhino():
    park = rhabm.Park(width=5, height=5)
    poacher_agent = rhabm.Poacher(park=park, vision_radius=4, movement_radius=1)
    rhino_agent = rhabm.Rhino(park=park)

    rhino_agent.park.occupants[rhino_agent.location[0]][
        rhino_agent.location[1]
    ] = rhabm.UnoccupiedEmoji
    rhino_agent.location = (0, 0)
    rhino_agent.park.occupants[rhino_agent.location[0]][
        rhino_agent.location[1]
    ] = rhino_agent

    if poacher_agent.location != (0, 0):
        poacher_agent.park.occupants[poacher_agent.location[0]][
            poacher_agent.location[1]
        ] = rhabm.UnoccupiedEmoji
    poacher_agent.location = (2, 2)
    poacher_agent.park.occupants[poacher_agent.location[0]][
        poacher_agent.location[1]
    ] = poacher_agent

    poacher_agent.move()

    assert poacher_agent.location in [(1, 2), (2, 1)]


def test_poacher_can_not_move():
    park = rhabm.Park(width=1, height=1)
    poacher_agent = rhabm.Poacher(park=park)

    current_location = poacher_agent.location
    poacher_agent.move()

    assert current_location == poacher_agent.location


def test_poacher_in_engage_target_state():
    park = rhabm.Park(width=2, height=2)
    poacher_agent = rhabm.Poacher(park=park, movement_radius=2)
    _ = rhabm.Rhino(park=park)

    assert poacher_agent.is_mobile == True

    current_position = poacher_agent.location
    poacher_agent.move()
    assert current_position == poacher_agent.location
    assert poacher_agent.is_mobile is False


def test_engage_target_with_high_target_value():
    park = rhabm.Park(width=2, height=2)
    time_to_remove_rhino = 4
    poacher_agent = rhabm.Poacher(
        park=park,
        movement_radius=2,
        time_to_remove_rhino=time_to_remove_rhino,
        target_value=2,
    )
    _ = rhabm.Rhino(park=park)

    poacher_agent.move()
    for _ in range(4):
        poacher_agent.move()
        time_to_remove_rhino -= 1

        assert poacher_agent.time_to_remove_rhino == time_to_remove_rhino
        assert poacher_agent.is_mobile == False

    for _ in range(100):
        poacher_agent.move()
    assert poacher_agent.is_mobile
    assert set([rhabm.DeadRhinoEmoji, rhabm.PoacherEmoji]).issubset(
        set([occupant.__repr__() for row in park.occupants for occupant in row])
    )


def test_engage_target_with_poacher_leaving_the_park():
    park = rhabm.Park(width=2, height=2)
    time_to_remove_rhino = 4
    poacher_agent = rhabm.Poacher(
        park=park,
        movement_radius=2,
        time_to_remove_rhino=time_to_remove_rhino,
        target_value=1,
    )
    _ = rhabm.Rhino(park=park)

    poacher_agent.move()
    for _ in range(4):
        poacher_agent.move()
        time_to_remove_rhino -= 1

        assert poacher_agent.time_to_remove_rhino == time_to_remove_rhino
        assert poacher_agent.is_mobile == False

    for _ in range(100):
        poacher_agent.move()

    assert set([rhabm.DeadRhinoEmoji]).issubset(
        set([occupant.__repr__() for row in park.occupants for occupant in row])
    )


def test_poacher_rep():
    park = rhabm.Park()

    poacher_agent = rhabm.Poacher(park=park)
    assert poacher_agent.__repr__() == rhabm.PoacherEmoji

    poacher_agent.caught = True
    assert poacher_agent.__repr__() == rhabm.CaughtPoacherEmoji


def test_security_init_default():
    park = rhabm.Park()
    security = rhabm.SecurityOfficer(park=park)

    assert security.vision_radius == 3
    assert security.movement_radius == 1
    assert security.target_agent == None


def test_security_init():
    park = rhabm.Park()
    vision_radius, movement_radius = 2, 2

    security = rhabm.SecurityOfficer(
        park=park, vision_radius=vision_radius, movement_radius=movement_radius
    )

    assert security.vision_radius == 2
    assert security.movement_radius == 2
    assert security.target_agent == None

def test_security_find_individual():
    park = rhabm.Park(width=2, height=2)
    security_agent = rhabm.SecurityOfficer(park=park)

    assert security_agent.find_individual() is False

    poacher_agent = rhabm.Poacher(park=park)
    assert security_agent.find_individual() == poacher_agent.location

def test_security_rep():
    park = rhabm.Park()

    security_agent = rhabm.SecurityOfficer(park=park)
    assert security_agent.__repr__() == rhabm.SecurityEmoji