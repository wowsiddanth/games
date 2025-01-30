import logging

from chip import Chip
from enum import Enum
from typing import List
from pydantic import BaseModel
from exceptions import MaxColumnHeightException

logging.basicConfig(level=logging.INFO)


class Direction(Enum):
    DOWN = 0
    DIAGONALLY_LEFT = -1
    DIAGONALLY_RIGHT = 1

    def __str__(self):
        return super().__str__()


class BoardResult(BaseModel):
    is_completed: bool
    current_state: List[str]
    winner_type: Chip.ChipType

    def __str__(self):
        if self.is_completed:
            return f"Winner is {self.winner_type}"
        else:
            return f"Game has yet to end."

    def __bool__(self):
        return self.is_completed

    def json(self):
        return {
            "is_completed": self.is_completed,
            "current_state": self.current_state,
            "winner_type": self.winner_type.value,
        }


class Board:
    def __init__(self):
        self.heights = [0] * 7
        self.track = {}
        self.placements = {}

    def __reset__(self):
        self.heights = [0] * 7
        self.track = {}
        self.placements = {}

    def __add_to_board(self, chip: Chip, x: int, y: int, direction: Direction) -> bool:
        """
        Adds a chip to the board w.r.t to a given direction. The direction here
        represents the direction of a directional streak.
        """
        precursor = self.track.get((x + direction.value, y - 1, direction), None)

        if precursor:
            chip_type = precursor[0]
            streak = precursor[1]

            if (
                direction == Direction.DIAGONALLY_LEFT
                or direction == Direction.DIAGONALLY_RIGHT
            ):
                successor = self.track.get(
                    (x - direction.value, y + 1, direction), None
                )

                if successor and successor[0] == chip.type:
                    streak += 1

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

    def place_blue_chip(self, column: int) -> BoardResult:
        return self.place(column, Chip(Chip.ChipType.BLUE))

    def place_red_chip(self, column: int) -> BoardResult:
        return self.place(column, Chip(Chip.ChipType.RED))

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
        self.placements[(x, y)] = chip

        logging.info(f"Placed {chip.type.value} chip at position: {(x, y)}")

        down = self.__add_to_board(chip, x, y, Direction.DOWN)
        right = self.__add_to_board(chip, x, y, Direction.DIAGONALLY_RIGHT)
        left = self.__add_to_board(chip, x, y, Direction.DIAGONALLY_LEFT)

        if down or right or left:
            logging.info(f"Winner is {chip.type.value}!")

        return BoardResult(
            is_completed=down or right or left,
            current_state=self.get_state(),
            winner_type=chip.type,
        )

    def __str__(self):
        rows = []

        for y in range(5, -1, -1):
            row = []

            for x in range(7):
                chip = self.placements.get((x, y))

                if chip:
                    row.append(chip.item())
                else:
                    row.append("#")

            combined_row = " ".join(row)
            rows.append(combined_row)

        combined_rows = "\n".join(rows)

        return combined_rows

    def get_state(self) -> List[str]:
        state = []

        for y in range(5, -1, -1):
            for x in range(7):
                chip = self.placements.get((x, y))

                if chip:
                    state.append(chip.item())
                else:
                    state.append("#")

        return state
