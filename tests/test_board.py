import pytest

from chip import Chip
from board import Board, Direction
from exceptions import MaxColumnHeightException


def test_board_initialization():
    b = Board()

    assert b.heights == [0] * 7
    assert b.track == {}


def test_board_add_one_chip():
    b = Board()
    b.place(0, chip=Chip(Chip.ChipType.BLUE))
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


def test_board_exceed_column_height():
    b = Board()

    with pytest.raises(MaxColumnHeightException):
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
        b.place(0, chip=Chip(Chip.ChipType.BLUE))
