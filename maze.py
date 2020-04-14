import random
import os
import time
from coordinate import Side, Coordinate, CoordinateArray


class Maze(object):

    def __init__(self, width, height,
                 horizontals_o=None, verticals_o=None):
        self.width = width
        self.height = height
        if horizontals_o is None or verticals_o is None:
            # initialise arrays of horizontals and verticals (walls and ceilings/floors)
            self.horizontals = [[False] * self.width for i in range(self.height + 1)]
            self.verticals = [[False] * (self.width + 1) for i in range(self.height)]
            self.__setup_random_maze()
        else:
            self.__check_sizes(width, height, horizontals_o, verticals_o)
            self.horizontals = horizontals_o
            self.verticals = verticals_o

    def __check_sizes(self, width, height, horizontals_o: list, verticals_o: list):
        if len(horizontals_o)is not height + 1:
            raise IndexError('Incorrect number of horizontals rows - should be height + 1')
        if len(verticals_o) is not height:
            raise IndexError('Incorrect number of verticals rows - should be height')
        for row in horizontals_o:
            if len(row) is not width:
                raise IndexError('One or more horizontals rows missing/ exceeding values')
        for row in verticals_o:
            if len(row) is not width + 1:
                raise IndexError('One or more verticals rows missing/ exceeding values')


    def __setup_random_maze(self):
        # set edges
        self.__set_row(0, True)
        self.__set_row(-1, True)
        self.__set_column(0, True)
        self.__set_column(-1, True)
        # set entry point
        entry_i = random.randrange(0, self.width - 1)
        self.__set_horizontal(entry_i, 0, False)
        # set exit point
        exit_i = random.randrange(0, self.width - 1)
        self.__set_horizontal(exit_i, -1, False)
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

    def routes_available(self, coordinate: Coordinate, previous_direction: Side = None) -> [Side]:
        sides = []
        if self.__route_available(coordinate, Side.TOP) and (previous_direction != Side.TOP or None):
            sides.append(Side.TOP)
        if self.__route_available(coordinate, Side.BOTTOM) and (previous_direction != Side.BOTTOM or None):
            sides.append(Side.BOTTOM)
        if self.__route_available(coordinate, Side.LEFT) and (previous_direction != Side.LEFT or None):
            sides.append(Side.LEFT)
        if self.__route_available(coordinate, Side.RIGHT) and (previous_direction != Side.RIGHT or None):
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
        # clear previous print out and short pause for display purposes
        #time.sleep(.450)
        os.system('clear')

        # printing rows in backward order so [0, 0] is bottom left of print out.
        for i in range(1, self.height + 1):
            self.__print_horizontal_row(self.horizontals[-i])
            if coordinates is None:
                self.__print_vertical_row(self.verticals[-i])
            else:
                self.__print_vertical_row(self.verticals[-i], coordinates.get_row(-i))
        # top row - one more horizontal row than vertical due to top and bottom
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