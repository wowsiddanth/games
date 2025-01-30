from enum import Enum


class Chip:
    class ChipType(Enum):
        RED = "red"
        BLUE = "blue"

    def __init__(self, type: ChipType):
        self.type = type

    def item(self):
        if self.type == self.ChipType.RED:
            return "R"
        else:
            return "B"
