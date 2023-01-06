from enum import Enum
import json
from validation import is_valid


class Coords:
    def __init__(self, row, column):
        """
            Its job is to initialize the coordinates
        :param row: the row of the coordinates
        :param column:  the column of the coordinates
        """
        self.row = row
        self.column = column

    def __eq__(self, other):
        """
            Its job is to return the result of self == other, in other words, comparison between two coordinates
        :param other: the other coordinates
        :return: True if the two coordinates are equal and False otherwise
        """
        return self.row == other.row and self.column == other.column

    def __lt__(self, other):
        """
            Its job is to return the result of self < other, in other words, comparison between two coordinates
        :param other: the other coordinates
        :return: True if self (a coordinates) is less than other (another coordinates)
        """
        if self.row == other.row:
            return self.column < other.column
        return self.row < other.row

    def __repr__(self):
        """
            Its job is representing the coordinates when it coordinates to be a str or we want to print it.
        :return: the string value of coordinates' info
        """
        return f'({self.row}, {self.column})'


class CellTypes(Enum):
    """
        Types of the cells we have
    """
    Normal = 0
    Source = 1
    Target = 2
    Obstacle = 3


class Cell:
    def __init__(self, coords, cost=1, cell_type=CellTypes.Normal.value):
        """
            Its job is to initialize the object cell with the given or default values
        :param coords: coordinates of the cell
        :param cost: cost of the cell
        :param cell_type: Type of the cell
        """
        self.coords = coords
        self.passed_distance = float("inf")  # Distance from source to the cell
        self.ongoing_distance = float("inf")  # Estimated distance from the cell to the target
        self.total_distance = float("inf")  # Total distance can be related to the two others or not
        self.previous_cell = None  # Parent of the cell
        self.type = cell_type  
        self.cost = cost

    def __repr__(self):
        """
            Its job is representing the cell when it calls to be a str or we want to print it.
        :return: the string value of cell's info
        """
        return f'({self.coords}, {self.type}, {self.total_distance}, {self.passed_distance}, {self.ongoing_distance})'

    def __lt__(self, other):
        """
            Its job is to return the result of self < other, in other words, comparison between two cells
        :param other: The other cell
        :return: True if Self(a cell) is less than Other (another cell)
        """
        return self.coords < other.coords

    def change_type(self, new_type):
        """
            Its job is changing type of a cell
        :param new_type: The new type we want to assign
        :return: None
        """
        self.type = new_type

    def reset(self):
        """
            Its job is to reset the cell's all data to be Normal
        :return: None
        """
        self.passed_distance = float("inf")
        self.ongoing_distance = float("inf")
        self.total_distance = float("inf")
        self.previous_cell = None
        self.change_type(CellTypes.Normal.value)


class Maze:

    def __init__(self, n_rows_, n_columns_, source=None, target=None, cell_list=None):
        """
            Its job is to initialize the maze with the given or default values
        :param n_rows_: number of rows in the maze
        :param n_columns_: number of columns in the maze
        :param source: source cell of the maze
        :param target: target cell of the maze
        :param cell_list: list of the cells of the maze
        """
        self.n_rows = n_rows_
        self.n_columns = n_columns_
        self.source = source
        self.target = target
        self.cell_list = cell_list
        self.n_checked_cells = 0  # number of checked cells in the algorithm will run on the maze

    def set_source(self, cell):
        """
            Its job is to set a cell as the new source of the maze
        :param cell: a cell in the maze
        :return: None
        """
        if self.source is not None:
            self.source.reset()
        self.source = cell
        cell.change_type(CellTypes.Source.value)

    def set_target(self, cell):
        """
            Its job is to set a cell as the new target of the maze
        :param cell: a cell in the maze
        :return: None
        """
        if self.target is not None:
            self.target.reset()
        self.target = cell
        cell.change_type(CellTypes.Target.value)

    def set_obstacle(self, cell):
        """
            Its job is to set a cell as a new obstacle
        :param cell: a cell in the maze
        :return: None
        """
        if cell.type == CellTypes.Obstacle.value:
            return
        cell.reset()
        cell.change_type(CellTypes.Obstacle.value)

    def get_cell(self, coords: Coords):
        """
            Its job is finding a cell in the maze based on its coordinates
        :param coords: coordinates of a cell
        :return: the cell having the given coordinates
        """
        for c in self.cell_list:
            if c.coords == coords:
                return c

    def get_neighbors(self, cell):
        """
            Its job is to find valid neighbors of a given cell (neither out of maze cells nor obstacles)
        :param cell: a cell of the maze
        :return: a lost of valid neighbors
        """
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
        """
            Its job is to reset all distances and computed values to be ready for running again.
        :return: None
        """
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
        """
            Its job is to build an object of maze based on the given dictionary data or input file.
        :param data: a dictionary of data helps building the maze
        :param file_address: a file of data helps building the maze
        :return: The built maze
        """
        if file_address is None:
            if data is None:
                raise Exception("At least one of data and file_address should be given!")
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
                # determining the cell type to build it based on the coordinates
                typ = CellTypes.Obstacle.value if (r, c) in obstacles_coords_list else CellTypes.Normal.value
                if source_tuple == (r, c):
                    typ = CellTypes.Source.value
                elif target_tuple == (r, c):
                    typ = CellTypes.Target.value
                cell = Cell(Coords(r, c), cell_type=typ)
                if typ == CellTypes.Source.value:
                    source_cell = cell  # setting source for building maze
                elif typ == CellTypes.Target.value:
                    target_cell = cell  # setting target for building maze
                cell_list.append(cell)
        maze = Maze(n_rows, n_columns, source_cell, target_cell, cell_list)
        return maze


def calc_path(maze):
    """
        Its job is fidning the path an algorithm found by tracking back from the target.
    :param maze: the solved maze
    :return: The found path in form of a list
    """
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
