import random
import os
from coordinate import Side, Coordinate, CoordinateArray


class Wall:
    def __init__(self, x, y, side: Side):
        self.x = x
        self.y = y
        self.side = side


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

    def routes_available(self, coordinate: Coordinate, entry_point: Side) -> [Side]:
        sides = []
        if self.__route_available(coordinate, Side.TOP) and entry_point != Side.TOP:
            sides.append(Side.TOP)
        if self.__route_available(coordinate, Side.BOTTOM) and entry_point != Side.BOTTOM:
            sides.append(Side.BOTTOM)
        if self.__route_available(coordinate, Side.LEFT) and entry_point != Side.LEFT:
            sides.append(Side.LEFT)
        if self.__route_available(coordinate, Side.RIGHT) and entry_point != Side.RIGHT:
            sides.append(Side.RIGHT)
        return sides

    def __route_available(self, coordinate: Coordinate, side: Side) -> bool:
        if side is Side.BOTTOM:
            return not self.__get_horizontal(coordinate.x, coordinate.y)
        elif side is Side.TOP:
            return not self.__get_horizontal(coordinate.x, coordinate.y + 1)
        elif side is Side.LEFT:
            return not self.__get_vertical(coordinate.x, coordinate.y)
        elif side is Side.RIGHT:
            return not self.__get_vertical(coordinate.x + 1, coordinate.y)

    def print_maze(self, coordinates: CoordinateArray = None):
        # clear previous print out
        print ("\n" * 20)

        # printing rows in backward order so [0, 0] is bottom left of print out.
        for i in range(1, self.height + 1):
            self.__print_horizontal_row(self.horizontals[-i])
            if coordinates is None:
                self.__print_vertical_row(self.verticals[-i])
            else:
                self.__print_vertical_row(self.verticals[-i], coordinates.get_row(-i))
        self.__print_horizontal_row(self.horizontals[-self.height - 1])

    def __print_horizontal_row(self, row):
        print(''.join(' ───' if elem else '    ' for elem in row))

    def __print_vertical_row(self, row, coordinates_row=None):
        if coordinates_row is None:
            print(''.join('|   'if elem else '    ' for elem in row))
        else:
            print_row = ""
            final_vertical = '|' if row[-1] else ' '
            for i in range(0, self.width):
                print_row = print_row + "%s %s " % ('|' if row[i] else ' ', coordinates_row[i])
            print("%s%s" % (print_row, final_vertical))