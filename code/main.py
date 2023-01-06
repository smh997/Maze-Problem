import os
import sys
import heuristics
import structures
import pygame
from user_interface import UI
from algorithms import dfs, bfs, a_star, greedy_best_first_search, AlgorithmTypes
from heuristics import chebyshev_distance, manhattan_distance, euclidean_distance, HeuristicTypes

algorithms_list = [dfs, bfs, greedy_best_first_search, a_star]
heuristics_list = [chebyshev_distance, manhattan_distance, euclidean_distance]


def solve(maze, algorithm, h=heuristics.manhattan_distance, ui=None):
    """
        Its job is to solve the maze using the given algorithm and data
    :param maze: the given maze
    :param algorithm: the chosen algorithm
    :param h: the selected heuristic function
    :param ui: the given user interface
    :return: result of the algorithm in solving the maze
    """
    maze.reset_distances()
    result = algorithm(maze, None, h, ui)
    if result["total_distance"] != float("inf") and result["total_distance"] != -1:
        path = structures.calc_path(maze)
        result["path"] = path
    return result


# setting recursion for running dfs as a recursive function is required in python
sys.setrecursionlimit(10**6)
if len(sys.argv) < 2:
    # default set-up of UI
    data = {
        "n_rows": 38,
        "n_columns": 70,
        "source": (10, 10),
        "target": (20, 40),
        "obstacles": []
    }
    maze = structures.Maze.build(data)
    ui = UI(maze=maze)
    mouse_button_down = False
    erase_mode = False
    draw_mode = structures.CellTypes.Source.value
    algorithm_mode = AlgorithmTypes.DFS.value
    heuristic = HeuristicTypes.Manhattan.value
    ui.reset_all()
    ui.draw_all()
    ui.fill_dfs_algo_rb()
    ui.fill_source_mode_rb()
    ui.fill_manhattan_heu_rb()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    p = pygame.mouse.get_pos()
                    pcoords = structures.Coords(column=p[0], row=p[1])
                    c = int(pcoords.column / (ui.rect_size.column + ui.margin))
                    r = int(pcoords.row / (ui.rect_size.row + ui.margin))
                    if c >= ui.maze.n_columns or r >= ui.maze.n_rows:  # it means no cell is clicked and maybe a buttion is clicked
                        draw_mode, algorithm_mode, heuristic, erase_mode, is_run = ui.click_button(pcoords, draw_mode, algorithm_mode, heuristic, erase_mode)
                        if is_run:
                            ui.clean_display()
                            res = solve(ui.maze, algorithms_list[algorithm_mode], heuristics_list[heuristic], ui)
                            res2 = solve(ui.maze, algorithms_list[algorithm_mode], heuristics_list[heuristic])
                            t = res2.get("time")
                            ui.draw_result(res, t)
                    else:
                        mouse_button_down = True
                        if erase_mode:
                            ui.modify_cell(pcoords, structures.CellTypes.Normal.value)
                        else:
                            ui.modify_cell(pcoords, draw_mode)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_button_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ui.clean_display()
                    res = solve(ui.maze, algorithms_list[algorithm_mode], heuristics_list[heuristic], ui)
                    res2 = solve(ui.maze, algorithms_list[algorithm_mode], heuristics_list[heuristic])
                    t = res2.get("time")
                    ui.draw_result(res, t)
            elif event.type == pygame.MOUSEMOTION:  # for smoothly putting and removing obstacles
                p = pygame.mouse.get_pos()
                pcoords = structures.Coords(column=p[0], row=p[1])
                if mouse_button_down:
                    if erase_mode:
                        ui.modify_cell(pcoords, structures.CellTypes.Normal.value)
                    else:
                        ui.modify_cell(pcoords, draw_mode)
        pygame.display.flip()

elif len(sys.argv) != 2:
    print(
        "Missing or additional arguments! Please run again and if you want to run program on a test provide its relative address.")
    exit(0)
else:
    maze = structures.Maze.build(file_address=sys.argv[1])
    if maze is None:
        print("The test data is not valid!")
        exit(0)

    output_lines = []
    for algo in algorithms_list:
        h_list = [heuristics_list[1]]
        if algo in [greedy_best_first_search, a_star]:
            h_list = heuristics_list
        for h in h_list:
            res = solve(maze, algo, h)
            output_lines.append(algo.__name__ + (' ' + h.__name__ if algo in [greedy_best_first_search, a_star] else '') + ' -> ' + 'Result:\n')
            for key in res:
                if key == "total_distance":
                    if res.get(key) == float("inf"):
                        output_lines.append(f'{key}: Not Reachable\n')
                    else:
                        output_lines.append(f'{key}: {int(res.get(key))}\n')
                elif key == "time":
                    output_lines.append(f'{key}: {round(res.get(key), 10)}\n')
                else:
                    output_lines.append(f'{key}: {res.get(key)}\n')
            output_lines.append('\n')
    if not os.path.isdir("./outputs/"):
        os.mkdir("./outputs/")
    output_file_name = sys.argv[1][8:-4] + 'txt'
    with open("./outputs/" + output_file_name, "w") as output_file:
        for line in output_lines:
            output_file.write(line)
