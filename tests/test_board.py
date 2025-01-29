import pytest

from chip import Chip
from board import Board, Direction
from exceptions import MaxColumnHeightException


@pytest.fixture
def b():
    return Board()


def test_board_initialization(b):
    assert b.heights == [0] * 7
    assert b.track == {}


def test_board_add_one_chip(b):
    b.place_blue_chip(0)

    assert b.heights == [1] + [0] * 6
    assert b.track == {
        (0, 0, Direction.DOWN): (Chip.ChipType.BLUE, 1),
        (0, 0, Direction.DIAGONALLY_RIGHT): (Chip.ChipType.BLUE, 1),
        (0, 0, Direction.DIAGONALLY_LEFT): (Chip.ChipType.BLUE, 1),
    }

    b = Board()
    b.place(1, chip=Chip(Chip.ChipType.BLUE))

    assert b.heights == [0] + [1] + [0] * 5
    assert b.track == {
        (1, 0, Direction.DOWN): (Chip.ChipType.BLUE, 1),
        (1, 0, Direction.DIAGONALLY_RIGHT): (Chip.ChipType.BLUE, 1),
        (1, 0, Direction.DIAGONALLY_LEFT): (Chip.ChipType.BLUE, 1),
    }


def test_board_exceed_column_height(b):
    with pytest.raises(MaxColumnHeightException):
        b.place_blue_chip(0)
        b.place_blue_chip(0)
        b.place_blue_chip(0)
        b.place_blue_chip(0)
        b.place_blue_chip(0)
        b.place_blue_chip(0)
        b.place_blue_chip(0)

    # Make sure there's no strange logic gap with the red ones...
    with pytest.raises(MaxColumnHeightException):
        b.place_red_chip(0)
        b.place_red_chip(0)
        b.place_red_chip(0)
        b.place_red_chip(0)
        b.place_red_chip(0)
        b.place_red_chip(0)
        b.place_red_chip(0)


"""'
For the following scenario tests, I will assert the BoardResult.

It is a truthy object, and returns true if the game is completed and false otherwise.
"""


def test_board_winning_scenario_1(b):
    assert not b.place_blue_chip(0)
    assert not b.place_red_chip(1)
    assert not b.place_blue_chip(0)
    assert not b.place_red_chip(2)
    assert not b.place_blue_chip(0)
    assert not b.place_red_chip(3)

    res = b.place_blue_chip(0)

    # Need to verify winner type
    assert res
    assert res.winner_type == Chip.ChipType.BLUE


def test_board_red_winner_2(b):
    assert not b.place_blue_chip(0)
    assert not b.place_red_chip(1)
    assert not b.place_blue_chip(0)
    assert not b.place_red_chip(3)
    assert not b.place_blue_chip(2)
    assert not b.place_red_chip(3)
    assert not b.place_blue_chip(1)
    assert not b.place_red_chip(2)
    assert not b.place_blue_chip(0)
    assert not b.place_red_chip(0)
    assert not b.place_blue_chip(3)

    res = b.place_red_chip(1)

    # Need to verify winner type
    assert res
    assert res.winner_type == Chip.ChipType.RED
