from enum import Enum

class Coords:
    	def __init__(self, row, column):
		self.row = row
		self.column = column


class CellTypes(Enum):
    	Normal = 0
	Start = 1
	Target = 2
	Obstacle = 3


class Cell:
	def __init__(self, coords, cost=1, cell_type=CellTypes.Normal.value):
		self.coords = coords
		self.distance_from_start = float("inf")
		self.previous_node = None
		self.type = cell_type
		self.cost = cost


class Maze:

	def __init__(self, n_rows_, n_columns_, source=None, target=None, cell_list=None):
		self.n_rows = n_rows_
		self.n_columns = n_columns_
		self.source = source
		self.target = target
		self.cell_list = cell_list

	def set_source(self, cell):
		self.source = cell

	def set_target(self, cell):
		self.target = cell

	def set_cell_list(self, cell_list):
		self.cell_list = cell_list

	def get_neighbors(self, cell):
    		
		neighbors_coords = [Coords(cell.coord.row, cell.coord.column - 1), Coords(cell.coord.row + 1, cell.coord.column), Coords(cell.coord.row, cell.coord.column + 1), Coords(cell.coord.row - 1, cell.coord.column)]

		in_maze_neighbors_coords = [coords for coords in neighbors_coords if (0 <= coords.column < len(self.cell_list) and 0 <= coords.row < len(self.cell_list[0]))]

		valid_neighbors = [self.cell_list[coords.row][coords.column] for coords in in_maze_neighbors_coords if self.cell_list[coords.row][coords.column].type != CellTypes.Obstacle.value]

		return valid_neighbors
