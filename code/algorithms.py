import heuristics
import heapq
import time
from enum import Enum


class AlgorithmTypes(Enum):
    """
        Types of algorithms we have
    """
    DFS = 0
    BFS = 1
    GreedyBFS = 2
    A_star = 3


iteration = 0  # used for calculating depth of DFS
max_iteration = 0  # used for store maximum depth of DFS


def dfs(maze, cell=None, *args):
    """
        Its job is doing DFS algorithm
    :param maze: The given maze
    :param cell: The current cell
    :param args: other arguments like ui object or others functions heuristic function
    :return: The result of performing DFS
    """
    global iteration, max_iteration

    ui = None
    if len(args) > 1:
        ui = args[1]
    source = False
    elapsed_time = 0
    if cell is None:  # if cell is None, it means its the first time function is calling so we need initializing
        source = True
        iteration = 0
        start_time = time.process_time()
        cell = maze.source
        cell.passed_distance = 0
        cell.total_distance = cell.passed_distance
        if maze.source is None:
            raise Exception("Maze is not complete to start! Source is not determined.")
    iteration += 1
    if cell == maze.target:  # if we found target its done
        max_iteration = max(iteration, max_iteration)
        return {"total_distance": maze.target.total_distance, "time": elapsed_time,
                "checked_cells_no": maze.n_checked_cells, "memory": max_iteration}
    if iteration > 2500:  # the threshold for dfs to perform recursion before os stops the process
        max_iteration = max(iteration, max_iteration)
        return {"total_distance": maze.target.total_distance, "time": elapsed_time,
                "checked_cells_no": maze.n_checked_cells, "memory": max_iteration}
    for neighbor_cell in maze.get_neighbors(cell):
        if neighbor_cell.passed_distance == float("inf"):  # Not visited
            neighbor_cell.previous_cell = cell
            neighbor_cell.passed_distance = cell.passed_distance + neighbor_cell.cost
            neighbor_cell.total_distance = neighbor_cell.passed_distance
            maze.n_checked_cells += 1
            if ui is not None:
                ui.draw_checking_cell(neighbor_cell)
                ui.draw_visited_cell(cell)
            res = dfs(maze, neighbor_cell, *args)
            iteration -= 1
            if res.get("total_distance") != float("inf"):  # we found the target and its time to come back.
                break
    if source:
        end_time = time.process_time()
        elapsed_time = end_time - start_time  # calculating the time
    max_iteration = max(iteration, max_iteration)
    return {"total_distance": maze.target.total_distance, "time": elapsed_time,
            "checked_cells_no": maze.n_checked_cells, "memory": max_iteration}


def bfs(maze, cell=None, *args):
    """
        Its job is doing BFS algorithm
    :param maze: The given maze
    :param cell: The current cell
    :param args: other arguments like ui object or others functions heuristic function
    :return: The result of performing DFS
    """
    ui = None
    if len(args) > 1:
        ui = args[1]
    start_time = time.process_time()
    if cell is None:
        cell = maze.source
        if maze.source is None:
            raise Exception("Maze is not complete to start! Source is not determined.")

    cell.passed_distance = 0
    cell.total_distance = cell.passed_distance
    queue = [cell]
    memory = len(queue)
    while queue:
        cell = queue.pop(0)
        if cell == maze.target:
            break
        for neighbor_cell in maze.get_neighbors(cell):
            if neighbor_cell.passed_distance == float("inf"):
                neighbor_cell.previous_cell = cell
                neighbor_cell.passed_distance = cell.passed_distance + neighbor_cell.cost
                neighbor_cell.total_distance = neighbor_cell.passed_distance
                queue.append(neighbor_cell)
                maze.n_checked_cells += 1

                if ui is not None:
                    ui.draw_checking_cell(neighbor_cell)
        if ui is not None:
            ui.draw_visited_cell(cell)

        memory = max(memory, len(queue))

    end_time = time.process_time()
    elapsed_time = end_time - start_time

    return {"total_distance": maze.target.total_distance, "time": elapsed_time,
            "checked_cells_no": maze.n_checked_cells, "memory": memory}


def a_star(maze, cell=None, h=heuristics.manhattan_distance, *args):
    """
        Its job is doing A* algorithm
    :param maze: The given maze
    :param cell: The current cell
    :param h: given heuristic function
    :param args: other arguments like ui object
    :return: The result of performing A*
    """
    ui = args[0]
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
    memory = len(frontier)

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
                maze.n_checked_cells += 1

                if ui is not None:
                    ui.draw_checking_cell(neighbor_cell)
        if ui is not None:
            ui.draw_visited_cell(cell)

        memory = max(memory, len(frontier))

    end_time = time.process_time()
    elapsed_time = end_time - start_time
    return {"total_distance": maze.target.total_distance, "time": elapsed_time,
            "checked_cells_no": maze.n_checked_cells, "memory": memory}


def greedy_best_first_search(maze, cell=None, h=heuristics.manhattan_distance, *args):
    """
        Its job is doing Greedy Best-First Search algorithm
    :param maze: The given maze
    :param cell: The current cell
    :param h: given heuristic function
    :param args: other arguments like ui object
    :return: The result of performing Greedy Best-First Search
    """
    ui = args[0]
    start_time = time.process_time()
    if cell is None:
        cell = maze.source
        if maze.source is None:
            raise Exception("Maze is not complete to start! Source is not determined.")

    def add(pq, val):
        heapq.heappush(pq, val)

    def pop(pq):
        return heapq.heappop(pq)[1]

    cell.passed_distance = 0
    cell.total_distance = cell.ongoing_distance = h(cell, maze.target)
    frontier = [(cell.total_distance, cell)]
    heapq.heapify(frontier)
    memory = len(frontier)

    while len(frontier):
        cell = pop(frontier)
        if cell == maze.target:
            break
        for neighbor_cell in maze.get_neighbors(cell):
            if neighbor_cell.total_distance == float("inf"):
                neighbor_cell.passed_distance = cell.passed_distance + neighbor_cell.cost
                neighbor_cell.total_distance = neighbor_cell.ongoing_distance = h(neighbor_cell, maze.target)
                add(frontier, (neighbor_cell.total_distance, neighbor_cell))
                neighbor_cell.previous_cell = cell
                maze.n_checked_cells += 1

                if ui is not None:
                    ui.draw_checking_cell(neighbor_cell)
        if ui is not None:
            ui.draw_visited_cell(cell)

        memory = max(memory, len(frontier))
    end_time = time.process_time()
    elapsed_time = end_time - start_time
    return {"total_distance": maze.target.passed_distance, "time": elapsed_time,
            "checked_cells_no": maze.n_checked_cells, "memory": memory}
