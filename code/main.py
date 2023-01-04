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
    maze.reset_distances()
    result = algorithm(maze, None, h, ui)
    if result["total_distance"] != float("inf") and result["total_distance"] != -1:
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
    # data = {"n_rows": 60, "n_columns": 60, "source": [0, 59], "target": [29, 5], "obstacles": [[46, 46], [16, 57], [38, 31], [46, 8], [34, 6], [11, 9], [29, 45], [18, 49], [14, 32], [26, 38], [11, 33], [1, 18], [6, 28], [23, 29], [28, 8], [6, 6], [3, 57], [1, 33], [27, 55], [13, 19], [52, 2], [5, 55], [5, 57], [2, 11], [19, 58], [31, 31], [1, 9], [54, 20], [52, 12], [1, 29], [44, 42], [7, 40], [11, 8], [27, 26], [1, 49], [34, 53], [0, 48], [28, 41], [9, 8], [21, 10], [22, 7], [13, 31], [38, 58], [47, 53], [3, 54], [47, 43], [11, 5], [2, 59], [1, 15], [4, 12], [10, 58], [4, 56], [15, 29], [18, 1], [22, 24], [49, 46], [34, 25], [30, 46], [16, 54], [3, 56], [53, 8], [8, 35], [25, 7], [21, 24], [45, 28], [47, 8], [35, 22], [19, 7], [51, 20], [19, 28], [22, 30], [54, 6], [27, 59], [45, 22], [56, 40], [45, 20], [10, 12], [46, 56], [28, 22], [36, 33], [42, 38], [0, 32], [10, 53], [30, 40], [29, 2], [14, 20], [7, 48], [2, 2], [57, 42], [26, 32], [46, 18], [36, 39], [11, 32], [44, 58], [18, 46], [18, 18], [18, 12], [12, 33], [13, 44], [43, 7], [31, 22], [22, 57], [14, 29], [0, 36], [53, 34], [59, 44], [43, 17], [19, 11], [39, 46], [43, 25], [32, 34], [20, 15], [37, 55], [58, 20], [32, 16], [49, 3], [40, 14], [18, 24], [45, 52], [7, 2], [22, 13], [20, 42], [24, 24], [14, 49], [51, 7], [12, 34], [25, 37], [26, 20], [20, 57], [15, 52], [32, 55], [37, 48], [10, 21], [26, 17], [7, 51], [18, 57], [25, 32], [30, 2], [36, 10], [52, 23], [57, 58], [30, 32], [54, 1], [39, 8], [3, 11], [26, 26], [43, 32], [52, 27], [9, 18], [2, 44], [52, 40], [35, 30], [52, 31], [37, 34], [8, 58], [0, 23], [43, 36], [5, 41], [42, 19], [40, 29], [13, 6], [54, 2], [41, 44], [59, 16], [33, 47], [50, 9], [16, 36], [55, 52], [48, 20], [27, 29], [59, 24], [46, 17], [2, 43], [42, 10], [33, 11], [31, 33], [26, 55], [24, 46], [18, 56], [24, 7], [50, 4], [18, 31], [0, 51], [27, 44], [45, 7], [34, 3], [19, 37], [56, 6], [27, 38], [24, 9], [34, 47], [19, 13], [45, 6], [9, 35], [7, 20], [19, 46], [6, 21], [6, 25], [1, 41], [35, 53], [8, 39], [29, 23], [49, 28], [9, 37], [23, 13], [36, 31], [11, 12], [13, 39], [58, 24], [29, 58], [24, 56], [55, 1], [35, 7], [7, 52], [30, 51], [51, 45], [41, 43], [26, 16], [32, 18], [31, 11], [46, 55], [48, 21], [53, 31], [35, 40], [48, 44], [42, 45], [33, 34], [35, 42], [28, 48], [48, 11], [21, 57], [17, 48], [35, 49], [14, 44], [55, 42], [53, 28], [36, 13], [35, 27], [34, 45], [28, 46], [49, 36], [27, 15], [40, 59], [44, 46], [50, 42], [6, 11], [24, 16], [50, 57], [16, 34], [48, 51], [57, 30], [25, 24], [23, 22], [20, 50], [2, 35], [14, 15], [43, 52], [40, 47], [26, 4], [10, 16], [5, 49], [55, 30], [39, 41], [43, 59], [26, 14], [2, 29], [4, 4], [1, 44], [43, 56], [22, 31], [2, 47], [12, 10], [49, 57], [43, 55], [54, 40], [32, 39], [12, 18], [34, 26], [3, 25], [52, 3], [40, 2], [19, 22], [19, 45], [31, 47], [8, 7], [16, 17], [53, 30], [31, 0], [10, 2], [43, 34], [53, 32], [18, 13], [6, 49], [51, 29], [5, 32], [9, 56], [22, 53], [35, 1], [1, 10], [40, 30], [23, 46], [42, 36], [53, 48], [1, 28], [33, 17], [33, 14], [33, 37], [31, 44], [29, 0], [52, 15], [10, 44], [9, 36], [52, 7], [31, 52], [45, 35], [5, 12], [19, 50], [37, 18], [33, 32], [13, 29], [16, 51], [22, 9], [53, 54], [11, 20], [59, 33], [28, 2], [12, 47], [35, 25], [53, 25], [13, 16], [28, 32], [15, 57], [56, 45], [52, 58], [54, 0], [49, 15], [7, 47], [49, 29], [7, 44], [19, 31], [35, 4], [46, 25], [51, 5], [20, 19], [16, 8], [26, 8], [39, 37], [52, 59], [39, 13], [59, 40], [46, 59], [25, 6], [18, 32], [58, 9], [21, 22], [32, 8], [11, 4], [2, 24], [22, 46], [17, 22]]}
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    ui.clean_display()
                    res = solve(ui.maze, algorithms_list[algorithm_mode], heuristics_list[heuristic], ui)
                    ui.draw_result(res)
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

    output_lines = []
    for algo in algorithms_list:
        res = solve(maze, algo)
        output_lines.append(algo.__name__ + ' -> ' + 'Result:\n')
        for key in res:
            if key == "total_distance":
                if res.get(key) == float("inf"):
                    output_lines.append(f'{key}: Not Reachable\n')
                else:
                    output_lines.append(f'{key}: {res.get(key)}\n')
            elif key == "time":
                output_lines.append(f'{key}: {round(res.get(key), 10)}\n')
            else:
                output_lines.append(f'{key}: {res.get(key)}\n')
        output_lines.append('\n')
    if not os.path.isdir("./outputs/"):
        os.mkdir("./outputs/")
    output_file_name = sys.argv[1][6:-4] + '.txt'
    with open("./outputs/" + output_file_name, "w") as output_file:
        for line in output_lines:
            output_file.write(line)


