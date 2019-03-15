import pytest

import rhabm


def test_init():
    park = rhabm.Park(width=2, height=2)
    assert park.width == 2
    assert park.height == 2
    assert set([occupant for row in park.occupants for occupant in row]) == set(
        rhabm.UnoccupiedEmoji
    )
    assert park.coordinates == [(0, 0), (0, 1), (1, 0), (1, 1)]


def test_get_random_unoccupied_cell():
    park = rhabm.Park(width=2, height=2)
    assert park.get_random_unoccupied_cell() in park.coordinates


def test_get_neighbours():
    current_location = (1, 1)
    park = rhabm.Park(width=2, height=2)
    assert set(park.get_neighbours(*current_location)) == set([(0, 1), (1, 0)])

    park = rhabm.Park(width=3, height=3)
    assert set(park.get_neighbours(*current_location)) == set(
        [(0, 1), (1, 0), (2, 1), (1, 2)]
    )

    current_location = (2, 2)
    park = rhabm.Park(width=5, height=5)
    assert set(park.get_neighbours(*current_location)) == set(
        [(1, 2), (2, 1), (3, 2), (2, 3)]
    )


def test_len():
    park = rhabm.Park()
    assert park.__len__() == 25


def test_repr():
    park = rhabm.Park()
    isinstance(park.__repr__(), str)
