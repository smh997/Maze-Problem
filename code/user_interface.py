import pygame
import structures
from algorithms import AlgorithmTypes
from heuristics import HeuristicTypes
import os
import time


class UI:

    def __init__(self, rect_size=structures.Coords(14, 14), margin=1, screen_size=(1050, 690),
                 background_color=pygame.Color("gray"), maze=None):
        """
            Its job is to initialize UI object with given or default values
        :param rect_size: size of each cell in display
        :param margin: length of margin
        :param screen_size: size if the screen
        :param background_color: color of the background
        :param maze: the given maze
        """
        self.rect_size = rect_size
        self.margin = margin
        self.screen_size = screen_size
        self.background_color = background_color
        self.maze = maze
        self.delay = 0.1  # amount of delay in showing next step
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (90, 90)
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.font = pygame.font.SysFont("calibri", 18)

        # Default location of buttons
        self.source_mode_rb = ((120, self.screen.get_height() - int(7.4 * self.rect_size.row)), 10)
        self.target_mode_rb = ((120, self.screen.get_height() - int(5.4 * self.rect_size.row)), 10)
        self.obstacle_mode_rb = ((135, self.screen.get_height() - int(3.4 * self.rect_size.row)), 10)
        self.erase_mode_rect = pygame.Rect(110, self.screen.get_height() - int(1.9 * self.rect_size.row),
                                           self.rect_size.column,
                                           self.rect_size.row)

        self.dfs_algo_rb = ((self.source_mode_rb[0][0] + 100, self.source_mode_rb[0][1]), self.source_mode_rb[1])
        self.bfs_algo_rb = ((self.target_mode_rb[0][0] + 100, self.target_mode_rb[0][1]), self.target_mode_rb[1])
        self.gbfs_algo_rb = ((self.obstacle_mode_rb[0][0] + 130, self.obstacle_mode_rb[0][1]), self.obstacle_mode_rb[1])
        self.astar_algo_rb = ((self.erase_mode_rect.left + self.erase_mode_rect.width // 2 + 105,
                               self.erase_mode_rect.top + self.erase_mode_rect.height // 2), self.obstacle_mode_rb[1])

        self.chebyshev_heu_rb = ((self.bfs_algo_rb[0][0] + 205, self.bfs_algo_rb[0][1]), self.bfs_algo_rb[1])
        self.manhattan_heu_rb = ((self.gbfs_algo_rb[0][0] + 161, self.gbfs_algo_rb[0][1]), self.gbfs_algo_rb[1])
        self.euclidean_heu_rb = ((self.astar_algo_rb[0][0] + 205, self.astar_algo_rb[0][1]), self.astar_algo_rb[1])

        self.reset_rect = pygame.Rect(520, self.screen.get_height() - int(6 * self.rect_size.row), 100, 50)
        self.run_rect = pygame.Rect(650, self.screen.get_height() - int(6 * self.rect_size.row), 100, 50)

    def calculate_pos(self, cell):
        """
            Its job is to calculate position of a given cell in the pygame screen
        :param cell: the given cell
        :return: the position of the cell
        """
        return structures.Coords(cell.coords.row * (self.rect_size.row + self.margin),
                                 cell.coords.column * (self.rect_size.column + self.margin))

    def draw_all(self):
        """
            Its job is to draw all elements
        :return: None
        """
        self.screen.fill(self.background_color)
        for cell in self.maze.cell_list:
            self.draw(cell)
        self.draw_buttons()

    def draw(self, cell, color=None):
        """
            Its job is to draw a cell with a given color
        :param cell: the given cell
        :param color: the given color
        :return: None
        """
        if color is None:
            color = self.get_color(cell)
        pos = self.calculate_pos(cell)
        pygame.draw.rect(self.screen, color,
                         pygame.Rect(pos.column, pos.row, self.rect_size.column, self.rect_size.row))

    def change_color(self, cell, new_color):
        """
            Its job is to change the color of a given cell
        :param cell: the given cell
        :param new_color: the new color
        :return: None
        """
        self.draw(cell, new_color)

    def get_color(self, cell):
        """
            Its job is to get a cell's color based on its type
        :param cell: the given cell
        :return: cell' color
        """
        if cell.type == structures.CellTypes.Normal.value:
            return pygame.Color("white")
        if cell.type == structures.CellTypes.Source.value:
            return pygame.Color("orange")
        if cell.type == structures.CellTypes.Target.value:
            return pygame.Color("Purple")
        if cell.type == structures.CellTypes.Obstacle.value:
            return pygame.Color("brown")

    def reset_all(self):
        """
            Its job is to reset all the cells of the maze
        :return: None
        """
        for cell in self.maze.cell_list:
            typ = structures.CellTypes.Normal.value
            if cell.type in (structures.CellTypes.Source.value, structures.CellTypes.Target.value):
                typ = cell.type
            cell.reset()
            cell.type = typ

    def modify_cell(self, pos, new_type):
        """
            Its job is to change type of a cell with the given position
        :param pos: position of a cell
        :param new_type: new type of the cell
        :return: None
        """
        c = int(pos.column / (self.rect_size.column + self.margin))
        r = int(pos.row / (self.rect_size.row + self.margin))
        if c >= self.maze.n_columns or r >= self.maze.n_rows:
            return
        cell = self.maze.get_cell(structures.Coords(r, c))
        if cell.type in (structures.CellTypes.Source.value, structures.CellTypes.Target.value):
            return
        if new_type == structures.CellTypes.Source.value:
            prev_source = self.maze.source
            self.maze.set_source(cell)
            self.draw(prev_source)
        elif new_type == structures.CellTypes.Target.value:
            prev_target = self.maze.target
            self.maze.set_target(cell)
            self.draw(prev_target)
        elif new_type == structures.CellTypes.Obstacle.value:
            self.maze.set_obstacle(cell)
        else:
            cell.reset()
        self.draw(cell)

    def draw_buttons(self):
        """
            Its job is to draw all the buttons for the first time after running program
        :return: None
        """
        self.draw_source_mode_rb(True)
        self.draw_target_mode_rb(True)
        self.draw_obstacle_mode_rb(True)
        self.draw_erase_mode_cb(True)

        self.draw_dfs_algo_rb(True)
        self.draw_bfs_algo_rb(True)
        self.draw_gbfs_algo_rb(True)
        self.draw_astar_algo_rb(True)

        text = self.font.render("Heuristics:", True, pygame.Color("Black"))
        self.screen.blit(text, (330, self.screen.get_height() - 8 * self.rect_size.row))
        self.draw_chebyshev_heu_rb(True)
        self.draw_manhattan_heu_rb(True)
        self.draw_euclidean_heu_rb(True)

        self.draw_reset_btn()
        self.draw_run_btn()

    def draw_source_mode_rb(self, first=False):
        """
            Its job is drawing or redrawing source mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Source Mode", True, pygame.Color("Black"))
            self.screen.blit(text, (10, self.screen.get_height() - 8 * self.rect_size.row))
        center, radius = self.source_mode_rb[0], self.source_mode_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Orange"), center, radius, 3)

    def draw_target_mode_rb(self, first=False):
        """
            Its job is drawing or redrawing target mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Target Mode", True, pygame.Color("Black"))
            self.screen.blit(text, (10, self.screen.get_height() - 6 * self.rect_size.row))
        center, radius = self.target_mode_rb[0], self.target_mode_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Purple"), center, radius, 3)

    def draw_obstacle_mode_rb(self, first=False):
        """
            Its job is drawing or redrawing obstacle mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Obstacle Mode", True, pygame.Color("Black"))
            self.screen.blit(text, (10, self.screen.get_height() - 4 * self.rect_size.row))
        center, radius = self.obstacle_mode_rb[0], self.obstacle_mode_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Brown"), center, radius, 3)

    def draw_erase_mode_cb(self, first=False):
        """
            Its job is drawing or redrawing erase mode checkbox
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Erase Mode", True, pygame.Color("Black"))
            self.screen.blit(text, (10, self.screen.get_height() - 2 * self.rect_size.row))
        pygame.draw.rect(self.screen, self.background_color, self.erase_mode_rect)
        pygame.draw.rect(self.screen, pygame.Color("Black"), self.erase_mode_rect, 3)

    def draw_dfs_algo_rb(self, first=False):
        """
            Its job is drawing or redrawing dfs algorithm mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("DFS", True, pygame.Color("Black"))
            self.screen.blit(text, (170, self.screen.get_height() - 8 * self.rect_size.row))
        center, radius = self.dfs_algo_rb[0], self.dfs_algo_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_bfs_algo_rb(self, first=False):
        """
            Its job is drawing or redrawing bfs algorithm mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("BFS", True, pygame.Color("Black"))
            self.screen.blit(text, (170, self.screen.get_height() - 6 * self.rect_size.row))
        center, radius = self.bfs_algo_rb[0], self.bfs_algo_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_gbfs_algo_rb(self, first=False):
        """
            Its job is drawing or redrawing greedy BFS algorithm mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("GreedyBFS", True, pygame.Color("Black"))
            self.screen.blit(text, (170, self.screen.get_height() - 4 * self.rect_size.row))
        center, radius = self.gbfs_algo_rb[0], self.gbfs_algo_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_astar_algo_rb(self, first=False):
        """
            Its job is drawing or redrawing A* algorithm mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("A*", True, pygame.Color("Black"))
            self.screen.blit(text, (170, self.screen.get_height() - 2 * self.rect_size.row))
        center, radius = self.astar_algo_rb[0], self.astar_algo_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_chebyshev_heu_rb(self, first=False):
        """
            Its job is drawing or redrawing Chebyshev heuristic mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Chebyshev", True, pygame.Color("Black"))
            self.screen.blit(text, (330, self.screen.get_height() - 6 * self.rect_size.row))
        center, radius = self.chebyshev_heu_rb[0], self.chebyshev_heu_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_manhattan_heu_rb(self, first=False):
        """
            Its job is drawing or redrawing Manhattan heuristic mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Manhattan", True, pygame.Color("Black"))
            self.screen.blit(text, (330, self.screen.get_height() - 4 * self.rect_size.row))
        center, radius = self.manhattan_heu_rb[0], self.manhattan_heu_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_euclidean_heu_rb(self, first=False):
        """
            Its job is drawing or redrawing Euclidean heuristic mode radio button
        :param first: is it the first time to draw or it is redraw
        :return: None
        """
        if first:
            text = self.font.render("Euclidean", True, pygame.Color("Black"))
            self.screen.blit(text, (330, self.screen.get_height() - 2 * self.rect_size.row))
        center, radius = self.euclidean_heu_rb[0], self.euclidean_heu_rb[1]
        pygame.draw.circle(self.screen, self.background_color, center, radius)
        pygame.draw.circle(self.screen, pygame.Color("Black"), center, radius, 2)

    def draw_reset_btn(self):
        """
            Its job is drawing or redrawing reset button
        :return: None
        """
        text = self.font.render("Reset", True, pygame.Color("Black"))
        pygame.draw.rect(self.screen, pygame.Color("Yellow"), self.reset_rect)
        pygame.draw.rect(self.screen, pygame.Color(139, 128, 0, 255), self.reset_rect, 2)
        self.screen.blit(text, (self.reset_rect.left + 30, self.reset_rect.top + self.reset_rect.height // 3))

    def draw_run_btn(self):
        """
            Its job is drawing or redrawing run button
        :return: None
        """
        text = self.font.render("Run", True, pygame.Color("Black"))
        pygame.draw.rect(self.screen, pygame.Color("Green"), self.run_rect)
        pygame.draw.rect(self.screen, pygame.Color("darkgreen"), self.run_rect, 2)
        self.screen.blit(text, (self.run_rect.left + 35, self.run_rect.top + self.run_rect.height // 3))

    def fill_source_mode_rb(self):
        """
            Its job is to fill source mode radio button
        :return: None
        """
        center, radius = self.source_mode_rb[0], self.source_mode_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Orange"), center, radius)

    def fill_target_mode_rb(self):
        """
            Its job is to fill target mode radio button
        :return: None
        """
        center, radius = self.target_mode_rb[0], self.target_mode_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Purple"), center, radius)

    def fill_obstacle_mode_rb(self):
        """
            Its job is to fill obstacle mode radio button
        :return: None
        """
        center, radius = self.obstacle_mode_rb[0], self.obstacle_mode_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Brown"), center, radius)

    def fill_erase_mode_cb(self):
        """
            Its job is to fill erase mode checkbox
        :return: None
        """
        pygame.draw.rect(self.screen, pygame.Color("Green"), self.erase_mode_rect)

    def fill_dfs_algo_rb(self):
        """
            Its job is to fill dfs algorithm mode radio button
        :return: None
        """
        center, radius = self.dfs_algo_rb[0], self.dfs_algo_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def fill_bfs_algo_rb(self):
        """
            Its job is to fill bfs algorithm mode radio button
        :return: None
        """
        center, radius = self.bfs_algo_rb[0], self.bfs_algo_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def fill_gbfs_algo_rb(self):
        """
            Its job is to fill greedy BFS algorithm mode radio button
        :return: None
        """
        center, radius = self.gbfs_algo_rb[0], self.gbfs_algo_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def fill_astar_algo_rb(self):
        """
            Its job is to fill A* algorithm mode radio button
        :return: None
        """
        center, radius = self.astar_algo_rb[0], self.astar_algo_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def fill_chebyshev_heu_rb(self):
        """
            Its job is to fill Chebyshev heuristic mode radio button
        :return: None
        """
        center, radius = self.chebyshev_heu_rb[0], self.chebyshev_heu_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def fill_manhattan_heu_rb(self):
        """
            Its job is to fill Manhattan heuristic mode radio button
        :return: None
        """
        center, radius = self.manhattan_heu_rb[0], self.manhattan_heu_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def fill_euclidean_heu_rb(self):
        """
            Its job is to fill Euclidean heuristic mode radio button
        :return: None
        """
        center, radius = self.euclidean_heu_rb[0], self.euclidean_heu_rb[1]
        pygame.draw.circle(self.screen, pygame.Color("Green"), center, radius)

    def click_button(self, pos, draw_mode, algo_mode, heuristic, erase_mode=False):
        """
            Its job is to determine which button is clicked and do the appropriate action
        :param pos: the position of the click
        :param draw_mode: the mode of draw (one of the types of cells)
        :param algo_mode: the chosen algorithm
        :param heuristic: the chosen heuristic
        :param erase_mode: erase mode that indicate we are in removing mode or putting mode
        :return: updated draw_mode, updated algo_mode, updated heuristic, updated erase_mode, and is_run which shows whether the run button is clicked
        """
        is_run = False
        if self.source_mode_rb[0][0] - self.source_mode_rb[1] <= pos.column <= self.source_mode_rb[0][0] + \
                self.source_mode_rb[1] and self.source_mode_rb[0][1] - self.source_mode_rb[1] <= pos.row <= \
                self.source_mode_rb[0][1] + self.source_mode_rb[1]:
            if draw_mode != structures.CellTypes.Source.value:
                draw_mode = structures.CellTypes.Source.value
                self.fill_source_mode_rb()
                self.draw_target_mode_rb()
                self.draw_obstacle_mode_rb()
        elif self.target_mode_rb[0][0] - self.target_mode_rb[1] <= pos.column <= self.target_mode_rb[0][0] + \
                self.target_mode_rb[1] and self.target_mode_rb[0][1] - self.target_mode_rb[1] <= pos.row <= \
                self.target_mode_rb[0][1] + self.target_mode_rb[1]:
            if draw_mode != structures.CellTypes.Target.value:
                draw_mode = structures.CellTypes.Target.value
                self.draw_source_mode_rb()
                self.fill_target_mode_rb()
                self.draw_obstacle_mode_rb()
        elif self.obstacle_mode_rb[0][0] - self.obstacle_mode_rb[1] <= pos.column <= self.obstacle_mode_rb[0][0] + \
                self.obstacle_mode_rb[1] and self.obstacle_mode_rb[0][1] - self.obstacle_mode_rb[1] <= pos.row <= \
                self.obstacle_mode_rb[0][1] + self.obstacle_mode_rb[1]:
            if draw_mode != structures.CellTypes.Obstacle.value:
                draw_mode = structures.CellTypes.Obstacle.value
                self.draw_source_mode_rb()
                self.draw_target_mode_rb()
                self.fill_obstacle_mode_rb()
        elif self.erase_mode_rect.left <= pos.column <= self.erase_mode_rect.left + self.erase_mode_rect.width and self.erase_mode_rect.top <= pos.row <= self.erase_mode_rect.top + self.erase_mode_rect.height:
            if erase_mode:
                erase_mode = False
                self.draw_erase_mode_cb()
            else:
                erase_mode = True
                self.fill_erase_mode_cb()
        elif self.dfs_algo_rb[0][0] - self.dfs_algo_rb[1] <= pos.column <= self.dfs_algo_rb[0][0] + self.dfs_algo_rb[
            1] and self.dfs_algo_rb[0][1] - self.dfs_algo_rb[1] <= pos.row <= self.dfs_algo_rb[0][1] + self.dfs_algo_rb[
            1]:
            if algo_mode != AlgorithmTypes.DFS.value:
                algo_mode = AlgorithmTypes.DFS.value
                self.fill_dfs_algo_rb()
                self.draw_bfs_algo_rb()
                self.draw_gbfs_algo_rb()
                self.draw_astar_algo_rb()
        elif self.bfs_algo_rb[0][0] - self.bfs_algo_rb[1] <= pos.column <= self.bfs_algo_rb[0][0] + self.bfs_algo_rb[
            1] and self.bfs_algo_rb[0][1] - self.bfs_algo_rb[1] <= pos.row <= self.bfs_algo_rb[0][1] + self.bfs_algo_rb[
            1]:
            if algo_mode != AlgorithmTypes.BFS.value:
                algo_mode = AlgorithmTypes.BFS.value
                self.draw_dfs_algo_rb()
                self.fill_bfs_algo_rb()
                self.draw_gbfs_algo_rb()
                self.draw_astar_algo_rb()
        elif self.gbfs_algo_rb[0][0] - self.gbfs_algo_rb[1] <= pos.column <= self.gbfs_algo_rb[0][0] + \
                self.gbfs_algo_rb[1] and self.gbfs_algo_rb[0][1] - self.gbfs_algo_rb[1] <= pos.row <= \
                self.gbfs_algo_rb[0][1] + self.gbfs_algo_rb[1]:
            if algo_mode != AlgorithmTypes.GreedyBFS.value:
                algo_mode = AlgorithmTypes.GreedyBFS.value
                self.draw_dfs_algo_rb()
                self.draw_bfs_algo_rb()
                self.fill_gbfs_algo_rb()
                self.draw_astar_algo_rb()
        elif self.astar_algo_rb[0][0] - self.astar_algo_rb[1] <= pos.column <= self.astar_algo_rb[0][0] + \
                self.astar_algo_rb[1] and self.astar_algo_rb[0][1] - self.astar_algo_rb[1] <= pos.row <= \
                self.astar_algo_rb[0][1] + self.astar_algo_rb[1]:
            if algo_mode != AlgorithmTypes.A_star.value:
                algo_mode = AlgorithmTypes.A_star.value
                self.draw_dfs_algo_rb()
                self.draw_bfs_algo_rb()
                self.draw_gbfs_algo_rb()
                self.fill_astar_algo_rb()
        elif self.chebyshev_heu_rb[0][0] - self.chebyshev_heu_rb[1] <= pos.column <= self.chebyshev_heu_rb[0][0] + \
                self.chebyshev_heu_rb[1] and self.chebyshev_heu_rb[0][1] - self.chebyshev_heu_rb[1] <= pos.row <= \
                self.chebyshev_heu_rb[0][1] + self.chebyshev_heu_rb[1]:
            if heuristic != HeuristicTypes.Chebyshev.value:
                heuristic = HeuristicTypes.Chebyshev.value
                self.fill_chebyshev_heu_rb()
                self.draw_manhattan_heu_rb()
                self.draw_euclidean_heu_rb()
        elif self.manhattan_heu_rb[0][0] - self.manhattan_heu_rb[1] <= pos.column <= self.manhattan_heu_rb[0][0] + \
                self.manhattan_heu_rb[1] and self.manhattan_heu_rb[0][1] - self.manhattan_heu_rb[1] <= pos.row <= \
                self.manhattan_heu_rb[0][1] + self.manhattan_heu_rb[1]:
            if heuristic != HeuristicTypes.Manhattan.value:
                heuristic = HeuristicTypes.Manhattan.value
                self.draw_chebyshev_heu_rb()
                self.fill_manhattan_heu_rb()
                self.draw_euclidean_heu_rb()
        elif self.euclidean_heu_rb[0][0] - self.euclidean_heu_rb[1] <= pos.column <= self.euclidean_heu_rb[0][0] + \
                self.euclidean_heu_rb[1] and self.euclidean_heu_rb[0][1] - self.euclidean_heu_rb[1] <= pos.row <= \
                self.euclidean_heu_rb[0][1] + self.euclidean_heu_rb[1]:
            if heuristic != HeuristicTypes.Euclidean.value:
                heuristic = HeuristicTypes.Euclidean.value
                self.draw_chebyshev_heu_rb()
                self.draw_manhattan_heu_rb()
                self.fill_euclidean_heu_rb()
        elif self.reset_rect.left <= pos.column <= self.reset_rect.left + self.reset_rect.width and self.reset_rect.top <= pos.row <= self.reset_rect.top + self.reset_rect.height:
            self.reset_all()
            erase_mode = False
            draw_mode = structures.CellTypes.Source.value
            algo_mode = AlgorithmTypes.DFS.value
            heuristic = HeuristicTypes.Manhattan.value
            self.draw_all()
            self.fill_dfs_algo_rb()
            self.fill_source_mode_rb()
            self.fill_manhattan_heu_rb()
        elif self.run_rect.left <= pos.column <= self.run_rect.left + self.run_rect.width and self.run_rect.top <= pos.row <= self.run_rect.top + self.run_rect.height:
            is_run = True
        return draw_mode, algo_mode, heuristic, erase_mode, is_run

    def clean_display(self):
        """
            Its job is to clean the results text of previous run
        :return: None
        """
        for cell in self.maze.cell_list:
            self.draw(cell)
        pygame.draw.rect(self.screen, self.background_color,
                         pygame.Rect(800, self.screen.get_height() - 8 * self.rect_size.row, 230, 110))

    def draw_result(self, res, t):
        """
            Its job is to draw the results of running an algorithm on the maze
        :param res: The result which is a dictionary of data
        :param t: CPU time of execution
        :return: None
        """
        path = res.get("path")
        d = res.get("total_distance")
        n_checked_cells = res.get("checked_cells_no")
        if path is not None:
            for cell in path:
                if cell.type not in (structures.CellTypes.Source.value, structures.CellTypes.Target.value):
                    self.draw(cell, pygame.Color("Darkgreen"))
            d = str(int(d))
        else:
            d = "Not Reachable!"
        t = str(round(t, 3))
        memory = res.get("memory")
        length_of_path_text = self.font.render(f"Total Length: {d}", True, pygame.Color("Black"))
        self.screen.blit(length_of_path_text, (800, self.screen.get_height() - 8 * self.rect_size.row))
        time_str = self.font.render(f"Time: {t}", True, pygame.Color("Black"))
        self.screen.blit(time_str, (800, self.screen.get_height() - 6 * self.rect_size.row))
        n_checked_cells_str = self.font.render(f"Checked Cells NO: {n_checked_cells}", True, pygame.Color("Black"))
        self.screen.blit(n_checked_cells_str, (800, self.screen.get_height() - 4 * self.rect_size.row))
        memory_str = self.font.render(f"Memory: {memory}", True, pygame.Color("Black"))
        self.screen.blit(memory_str, (800, self.screen.get_height() - 2 * self.rect_size.row))

    def draw_checking_cell(self, cell):
        """
            Its job is to draw the cells which are in the queue of checking
        :param cell: the given cell
        :return: None
        """
        if cell.type in (structures.CellTypes.Source.value, structures.CellTypes.Target.value):
            return
        self.draw(cell, pygame.Color(135, 197, 233, 255))

    def draw_visited_cell(self, cell):
        """
            Its job is to draw the cells which are popped from the queue
        :param cell: the given cell
        :return: None
        """
        if cell.type in (structures.CellTypes.Source.value, structures.CellTypes.Target.value):
            return
        self.draw(cell, pygame.Color(102, 255, 178, 255))

        start = time.time()
        while time.time() - start < self.delay:
            pass
        pygame.display.flip()
