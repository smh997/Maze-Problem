import heuristics
import heapq
import time


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


def a_star(maze, cell=None, h=heuristics.manhattan_distance, *args):
    start_time = time.process_time()
    if cell is None:
        cell = maze.source
        if maze.source is None:
            raise Exception("Maze is not complete to start! Source is not determined.")

    def g(prev_cell, nxt_cell):
        return prev_cell.passed_distance + nxt_cell.cost

    def add(pq, val):
        heapq.heappush(pq, val)

    def pop(pq):
        return heapq.heappop(pq)[1]

    cell.passed_distance = 0
    cell.ongoing_distance = h(cell, maze.target)
    cell.total_distance = cell.passed_distance + cell.ongoing_distance
    frontier = [(cell.total_distance, cell)]
    heapq.heapify(frontier)

    while len(frontier):
        cell = pop(frontier)
        if cell == maze.target:
            break
        for neighbor_cell in maze.get_neighbors(cell):
            if neighbor_cell.total_distance == float(
                    "inf") or neighbor_cell.total_distance > g(cell, neighbor_cell) + h(neighbor_cell, maze.target):
                neighbor_cell.ongoing_distance = h(neighbor_cell, maze.target)
                neighbor_cell.passed_distance = g(cell, neighbor_cell)
                neighbor_cell.total_distance = neighbor_cell.passed_distance + neighbor_cell.ongoing_distance
                add(frontier, (neighbor_cell.total_distance, neighbor_cell))
                neighbor_cell.previous_cell = cell

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    return {"total_distance": maze.target.total_distance, "time": elapsed_time}


def greedy_best_first_search(maze, cell, h):
    pass
