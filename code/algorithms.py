from collections import defaultdict

import structures


def dfs(maze, cell=None):
    for vertex in maze.get_neighbors(maze, cell):
        if vertex.passed_distance == float("inf"):
            vertex.previous_cell(cell)
            vertex.passed_distance = cell.passed_distance + vertex.cost
            dfs(maze, vertex)
    return maze.target


def bfs(maze, cell=None):
    queue = []

    queue.append(cell)

    while queue:
        m = queue.pop(0)

        for neighbour in maze.get_neighbors(maze, m):
            if neighbour.passed_distance == float("inf"):
                neighbour.previous_cell(cell)
                neighbour.passed_distance = cell.passed_distance + neighbour.cost
                queue.append(neighbour)


def a_star(maze, cell, h):
    pass


def greedy_best_first_search(maze, cell, h):
    pass
