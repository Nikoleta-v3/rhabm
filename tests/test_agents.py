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
