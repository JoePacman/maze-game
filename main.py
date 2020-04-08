import numpy as np
import random
from enum import Enum


class Side(Enum):
    TOP, BOTTOM, LEFT, RIGHT = range(4)


class Status(Enum):
    P, X, U = range(3)


class Wall:
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = Status.U

    def set_status(self, status_o: Status):
        self.status = status_o

    def __repr__(self):
        return self.status.name


class Maze(object):

    def __init__(self, width, height,
                 horizontals_o=None, verticals_o=None,
                 entry_point_o: Wall = None, exit_point_o: Wall = None):
        self.width = width
        self.height = height
        if horizontals_o is None or verticals_o is None:
            # initialise arrays of horizontals and verticals (walls and ceilings/floors)
            self.horizontals = [[False] * self.width for i in range(self.height + 1)]
            self.verticals = [[False] * (self.width + 1) for i in range(self.height)]
            self.__setup_random_maze()
        else:
            self.horizontals = horizontals_o
            self.verticals = verticals_o
            self.entry_point = entry_point_o
            self.exit_point = exit_point_o

    def __setup_random_maze(self):
        # set edges
        self.__set_row(0, True)
        self.__set_row(-1, True)
        self.__set_column(0, True)
        self.__set_column(-1, True)
        # set entry point
        entry_i = random.randrange(0, self.width - 1)
        self.__set_horizontal(entry_i, 0, False)
        self.entry_point = Wall(entry_i, 0, Side.BOTTOM)
        # set exit point
        exit_i = random.randrange(0, self.width - 1)
        self.__set_horizontal(exit_i, -1, False)
        self.exit_point = Wall(exit_i, self.height, Side.TOP)
        # create exit route
        #self.__create_route()


    def __get_vertical(self, x, y) -> bool:
        return self.verticals[y][x]

    def __set_vertical(self, x, y, value):
        self.verticals[y][x] = value

    def __get_horizontal(self, x, y) -> bool:
        return self.horizontals[y][x]

    def __set_horizontal(self, x, y, value):
        self.horizontals[y][x] = value

    def __set_row(self, x, value):
        self.horizontals[x] = [True for i in range(self.width)]

    def __set_column(self, y, value):
        for i in range(0, self.height):
            self.verticals[i][y] = True

    #def __create_route(self):

    # Assuming there can be no infinite loops (e.g. paths that lead back)
    def check_viable_exit(self, coordinate: Coordinate) -> bool:

        return True

    def __route_available(self, coordinate: Coordinate, side: Side) -> bool:
        if side is Side.BOTTOM:
            return not self.__get_horizontal(coordinate.x, coordinate.y)
        elif side is Side.TOP:
            return not self.__get_horizontal(coordinate.x, coordinate.y + 1)
        elif side is Side.LEFT:
            return not self.__get_vertical(coordinate.x, coordinate.y)
        elif side is Side.RIGHT:
            return not self.__get_vertical(coordinate.x + 1, coordinate.y)


    def print_maze(self):
        # printing rows in backward order so [0, 0] is bottom left of print out.
        for i in range(1, self.height + 1):
            self.__print_row(self.horizontals[-i], ' ───')
            self.__print_row(self.verticals[-i], '|   ')
        self.__print_row(self.horizontals[-self.height - 1], ' ───')

    def __print_row(self, row, value):
        print(''.join(value if elem else '    ' for elem in row))


def solveMaze(maze: Maze):
    # create array of coordinates
    coordinates = []
    for i in range(0, maze.width):
        x_coordinates = []
        for j in range(0, maze.height):
            x_coordinates.append(Coordinate(i, j))
        coordinates.append(x_coordinates)

    print(coordinates)


if __name__ == "__main__":
    #maze = Maze(5, 5)
    #maze.print_maze()

    # testing logic to determine if there is a possible route to exit - pre-generating maze
    horizontals = [[True, False, True], [False, True, False], [True, True, False], [True, False, True]]
    verticals = [[True, False, True, True], [True, False, False, True], [True, False, False, True]]
    maze = Maze(3, 3, horizontals, verticals, Wall(1, 2, Side.TOP), Wall(0, 1, Side.BOTTOM))
    maze.print_maze()
    solveMaze(maze)


