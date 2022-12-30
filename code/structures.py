import colors
from enum import Enum


class Coords:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __lt__(self, other):
        if self.row == other.row:
            return self.column < other.column
        return self.row < other.row

    def __repr__(self):
        return f'({self.row}, {self.column})'


class CellTypes(Enum):
    Normal = 0
    Source = 1
    Target = 2
    Obstacle = 3


class Cell:
    def __init__(self, coords, cost=1, cell_type=CellTypes.Normal.value):
        self.coords = coords
        self.passed_distance = float("inf")
        self.previous_cell = None
        self.type = cell_type
        self.cost = cost

    def __repr__(self):
        return f'({self.coords}, {self.type})'

    def __lt__(self, other):
        return self.coords < other.coords


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
        neighbors_coords = [Coords(cell.coords.row, cell.coords.column - 1),
                            Coords(cell.coords.row + 1, cell.coords.column),
                            Coords(cell.coords.row, cell.coords.column + 1),
                            Coords(cell.coords.row - 1, cell.coords.column)]
        
		in_maze_neighbors_coords = [coords for coords in neighbors_coords if
                                    (0 <= coords.column < self.n_columns and 0 <= coords.row < self.n_rows)]
        
        valid_neighbors = [cell for cell in self.cell_list if
                           cell.type != CellTypes.Obstacle and cell.coords in in_maze_neighbors_coords]
        
        return valid_neighbors

    def reset_distances(self):
        if self.cell_list is None:
            raise Exception("Cell_list is still empty!")
        for cell in self.cell_list:
            cell.passed_distance = float("inf")


def calc_path(maze):
    reversed_path = [maze.target]
    last_cell = maze.target
    while True:
        last_cell = last_cell.previous_cell
        if maze.source == last_cell:
            path = reversed_path[::-1]
            return path
        else:
            reversed_path.append(last_cell)
