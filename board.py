from enum import Enum
from chip import Chip
from exceptions import MaxColumnHeightException, CellExistsAtPositionException

class Direction(Enum):
	DOWN = 'down'
	DIAGONALLY_LEFT = 'left'
	DIAGONALLY_RIGHT = 'right'

	def __str__(self):
		return super().__str__()


class Board:
	def __init__(self):
		self.heights = [0] * 7
		self.track = {}

	def place(self, column: int, chip: Chip):
		x = column
		y = self.heights[column]

		# Will exceed the board!
		if y == 6:
			raise MaxColumnHeightException
		
		self.heights[column] += 1

		# Add streaks ============================================

		# Down
		down = self.track.get((x, y - 1, Direction.DOWN), None) 

		if down:
			chip_type = down[0]
			streak = down[1]

			if chip_type == chip.type:
				if streak + 1 == 4:
					return f"Winner is {chip.type}!"
				else:
					print(chip_type, streak + 1, x , y)
					self.track[(x, y, Direction.DOWN)] = (chip.type, streak + 1)
			else:
				self.track[(x, y, Direction.DOWN)] = (chip.type, 1)
		else:
			self.track[(x, y, Direction.DOWN)] = (chip.type, 1)

		# Diagonally right
		right = self.track.get((x + 1, y - 1, Direction.DIAGONALLY_RIGHT), None) 

		if right:
			chip_type = right[0]
			streak = right[1]

			if chip_type == chip.type:
				if streak + 1 == 4:
					return f"Winner is {chip.type}!"
				else:
					self.track[(x, y, Direction.DIAGONALLY_RIGHT)] = (chip.type, streak + 1)
			else:
				self.track[(x, y, Direction.DIAGONALLY_RIGHT)] = (chip.type, 1)
		else:
			self.track[(x, y, Direction.DIAGONALLY_RIGHT)] = (chip.type, 1)

		# Diagonally left
		left = self.track.get((x - 1, y - 1, Direction.DIAGONALLY_LEFT), None) 

		if left:
			chip_type = left[0]
			streak = left[1]

			if chip_type == chip.type:
				if streak + 1 == 4:
					return f"Winner is {chip.type}!"
				else:
					self.track[(x, y, Direction.DIAGONALLY_LEFT)] = (chip.type, streak + 1)
			else:
				self.track[(x, y, Direction.DIAGONALLY_LEFT)] = (chip.type, 1)
		else:
			self.track[(x, y, Direction.DIAGONALLY_LEFT)] = (chip.type, 1)

		return f"Placed chip at position: {(x, y)}"


b = Board()	

result = b.place(0, Chip(Chip.ChipType.BLUE))
print(result)
