from enum import Enum
import json
from validation import is_valid


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
        self.ongoing_distance = float("inf")
        self.total_distance = float("inf")
        self.previous_cell = None  
        self.type = cell_type  
        self.cost = cost

    def __repr__(self):
        return f'({self.coords}, {self.type}, {self.total_distance}, {self.passed_distance}, {self.ongoing_distance})'

    def __lt__(self, other):
        return self.coords < other.coords

    def change_type(self, new_type):
        self.type = new_type

    def reset(self):
        self.passed_distance = float("inf")
        self.ongoing_distance = float("inf")
        self.total_distance = float("inf")
        self.previous_cell = None
        self.change_type(CellTypes.Normal.value)


class Maze:

    def __init__(self, n_rows_, n_columns_, source=None, target=None, cell_list=None):
        self.n_rows = n_rows_
        self.n_columns = n_columns_
        self.source = source
        self.target = target
        self.cell_list = cell_list
        self.n_checked_cells = 0

    def set_source(self, cell):
        if self.source is not None:
            self.source.reset()
        self.source = cell
        cell.change_type(CellTypes.Source.value)

    def set_target(self, cell):
        if self.target is not None:
            self.target.reset()
        self.target = cell
        cell.change_type(CellTypes.Target.value)

    def set_obstacle(self, cell):
        if cell.type == CellTypes.Obstacle.value:
            return
        cell.reset()
        cell.change_type(CellTypes.Obstacle.value)

    def set_cell_list(self, cell_list):
        self.cell_list = cell_list

    def get_cell(self, coords: Coords):
        for c in self.cell_list:
            if c.coords == coords:
                return c

    def get_neighbors(self, cell):
        neighbors_coords = [Coords(cell.coords.row, cell.coords.column - 1),
                            Coords(cell.coords.row + 1, cell.coords.column),
                            Coords(cell.coords.row, cell.coords.column + 1),
                            Coords(cell.coords.row - 1, cell.coords.column)]
        
        in_maze_neighbors_coords = [coords for coords in neighbors_coords if
                                    (0 <= coords.column < self.n_columns and 0 <= coords.row < self.n_rows)]
        
        valid_neighbors = [cell for cell in self.cell_list if
                           cell.type != CellTypes.Obstacle.value and cell.coords in in_maze_neighbors_coords]
        
        return valid_neighbors

    def reset_distances(self):
        if self.cell_list is None:
            raise Exception("Cell_list is still empty!")
        for cell in self.cell_list:
            cell.passed_distance = float("inf")
            cell.ongoing_distance = float("inf")
            cell.total_distance = float("inf")
            cell.previous_cell = None
        self.n_checked_cells = 0

    @staticmethod
    def build(data=None, file_address=None):
        if file_address is None:
            if data is None:
                pass  # TODO: error
        else:
            with open(file_address, 'r') as json_file:
                data = json.load(json_file)
        if not is_valid(data):
            return None
        obstacles_coords_list = data.get("obstacles")
        for i, obstacle_coords in enumerate(obstacles_coords_list):
            obstacles_coords_list[i] = tuple(obstacle_coords)
        n_rows, n_columns = data.get("n_rows"), data.get("n_columns")
        source_tuple, target_tuple = tuple(data.get("source")), tuple(data.get("target"))
        source_cell, target_cell = None, None
        cell_list = []
        for r in range(n_rows):
            for c in range(n_columns):
                typ = CellTypes.Obstacle.value if (r, c) in obstacles_coords_list else CellTypes.Normal.value
                if source_tuple == (r, c):
                    typ = CellTypes.Source.value
                elif target_tuple == (r, c):
                    typ = CellTypes.Target.value
                cell = Cell(Coords(r, c), cell_type=typ)
                if typ == CellTypes.Source.value:
                    source_cell = cell
                elif typ == CellTypes.Target.value:
                    target_cell = cell
                cell_list.append(cell)
        maze = Maze(n_rows, n_columns, source_cell, target_cell, cell_list)
        return maze


def calc_path(maze):
    reversed_path = [maze.target]
    last_cell = maze.target
    while True:
        last_cell = last_cell.previous_cell
        if maze.source == last_cell:
            reversed_path.append(last_cell)
            path = reversed_path[::-1]
            return path
        else:
            reversed_path.append(last_cell)
