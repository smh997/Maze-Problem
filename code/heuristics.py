from enum import Enum


class HeuristicTypes(Enum):
    Chebyshev = 0
    Manhattan = 1
    Euclidean = 2


def chebyshev_distance(cell, target):
    """
        Returns the distance from the given node to the given target
    """
    return max(abs(cell.coords.column - target.coords.column), abs(cell.coords.row - target.coords.row))


def manhattan_distance(cell, target):
    """
        Returns the distance from the given node to the given target
    """
    return abs(cell.coords.column - target.coords.column) + abs(cell.coords.row - target.coords.row)


def euclidean_distance(cell, target):
    """
        Returns the distance from the given node to the given target
    """
    return ((cell.coords.column - target.coords.column) ** 2 + (cell.coords.row - target.coords.row) ** 2) ** 0.5
