from enum import Enum


class Side(Enum):
    TOP, BOTTOM, LEFT, RIGHT = range(4)


class Status(Enum):
    P, X, U, M = range(4)
    # P = path to exit
    # X = dead end
    # U = unknown
    # M = multiple paths to explore


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.status = None

    def set_status(self, status_o: Status):
        self.status = status_o

    def __repr__(self):
        if self.status is None:
            return ' '
        else:
            return self.status.name


class CoordinateArray:
    def __init__(self, maze_width, maze_height):
        # create array of coordinates
        self.coordinates = []
        for j in range(0, maze_height):
            x_coordinates = []
            for i in range(0, maze_width):
                x_coordinates.append(Coordinate(i, j))
            self.coordinates.append(x_coordinates)

    def update_coordinate(self, x, y, status: Status):
        self.coordinates[y][x].set_status(status)

    def get_coordinate(self, x, y) -> Coordinate:
        return self.coordinates[y][x]

    def get_row(self, y):
        return self.coordinates[y]
