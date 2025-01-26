import logging

from pydantic import BaseModel
from enum import Enum
from chip import Chip
from exceptions import MaxColumnHeightException, CellExistsAtPositionException

logging.basicConfig(level=logging.INFO)


class Direction(Enum):
    DOWN = 0
    DIAGONALLY_LEFT = -1
    DIAGONALLY_RIGHT = 1

    def __str__(self):
        return super().__str__()


class BoardResult(BaseModel):
    is_completed: bool
    winner_type: Chip.ChipType

    def __str__(self):
        if self.is_completed:
            return f"Winner is {self.winner_type}"
        else:
            return f"Game has yet to end."


class Board:
    def __init__(self):
        self.heights = [0] * 7
        self.track = {}

    def __add_to_board(self, chip: Chip, x: int, y: int, direction: Direction) -> bool:
        """
        Adds a chip to the board w.r.t to a given direction. The direction here
        represents the direction of a directional streak.
        """
        precursor = self.track.get((x, y + direction.value, direction), None)

        if precursor:
            chip_type = precursor[0]
            streak = precursor[1]

            if chip_type == chip.type:
                if streak + 1 == 4:
                    return True
                else:
                    self.track[(x, y, direction)] = (chip.type, streak + 1)
            else:
                self.track[(x, y, direction)] = (chip.type, 1)
        else:
            self.track[(x, y, direction)] = (chip.type, 1)

        return False

    def place(self, column: int, chip: Chip) -> BoardResult:
        """
        Places a specified chip in a given column.
        """

        x = column
        y = self.heights[column]

        # Column is full
        if y == 6:
            raise MaxColumnHeightException

        self.heights[column] += 1
        logging.info(f"Placed {chip.type.value} chip at position: {(x, y)}")

        down = self.__add_to_board(chip, x, y, Direction.DOWN)
        right = self.__add_to_board(chip, x, y, Direction.DIAGONALLY_RIGHT)
        left = self.__add_to_board(chip, x, y, Direction.DIAGONALLY_LEFT)

        return BoardResult(is_completed=down or right or left, winner_type=chip.type)


b = Board()

b.place(0, Chip(Chip.ChipType.BLUE))
b.place(0, Chip(Chip.ChipType.BLUE))
b.place(0, Chip(Chip.ChipType.BLUE))
print(b.place(0, Chip(Chip.ChipType.BLUE)))
