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
    maze.reset_distances()
    result = algorithm(maze, None, h, ui)
    if result["total_distance"] != float("inf"):
        path = structures.calc_path(maze)
        result["path"] = path
    return result


sys.setrecursionlimit(10**6)
if len(sys.argv) < 2:
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
                    if c >= ui.maze.n_columns or r >= ui.maze.n_rows:
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
            # Keyboard input
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ui.clean_display()
                    res = solve(ui.maze, algorithms_list[algorithm_mode], heuristics_list[heuristic], ui)
                    ui.draw_result(res)
            # Modify nodes
            elif event.type == pygame.MOUSEMOTION:
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
    for algo in algorithms_list:
        res = solve(maze, algo)
        print(algo.__name__ + ' -> ' + 'Result:')
        print(res)

