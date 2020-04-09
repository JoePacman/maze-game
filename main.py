from maze import Maze, Wall
from coordinate import Side, Status, CoordinateArray


class Tracking:
    # need to track each multiple and the directions tried from them
    def __init__(self):
        self.multiples = None

    def add_multiple(self, multiple):
        self.multiples.append(multiple)

    def get_next_direction(self):
        #


class Multiple:
    def __init__(self, x, y, previousDirection):
        self.x = x
        self.y = y
        self.directions_tried = [previousDirection]
        self.no_options = False

    def addDirectionTried(self, side: Side):
        self.directions_tried.append(side)
        if Side.BOTTOM in self.directions_tried and Side.Top in self.directions_tried and Side.LEFT in self.directions_tried and Side.RIGHT in self.directions_tried:
            self.no_options = True


def solve_maze(maze_i: Maze):
    coordinates = CoordinateArray(maze_i.width, maze_i.height)

    x = 0  # start x position
    y = 0  # start y position
    previous_direction = Side.BOTTOM  # entry point
    last_multiple = []
    last_multiple_directions_tried = []
    current_path_from_last_multiple = []
    previous_direction_at_last_multiple = None
    exit_found = False
    i = 0  # temp

    while exit_found is False:

        routes_available = maze.routes_available(coordinates.get_coordinate(x, y), previous_direction)

        if len(routes_available) is 0:
            coordinates.update_coordinate(x, y, Status.X)
            for x_y in current_path_from_last_multiple:
                coordinates.update_coordinate(x_y[0], x_y[1], Status.X)
            x, y = last_multiple

        elif len(routes_available) is 1:
            next_direction = routes_available[0]
            current_path_from_last_multiple.append([x, y])
            coordinates.update_coordinate(x, y, Status.U)
            previous_direction = find_previous_direction(next_direction)
            x, y = move_one(x, y, next_direction)

        if len(routes_available) > 1:
            # ensure that we move in a new direction
            for side in last_multiple_directions_tried:
                if side in routes_available:
                    routes_available.remove(side)

            next_direction = routes_available[0]
            previous_direction = find_previous_direction(next_direction)

            last_multiple = [x, y]
            last_multiple_directions_tried.append(previous_direction)
            last_multiple_directions_tried.append(next_direction)
            current_path_from_last_multiple = []

            coordinates.update_coordinate(x, y, Status.M)
            x, y = move_one(x, y, next_direction)

        maze_i.print_maze(coordinates)

        i += 1
        if i > 100:
            exit_found = True


def find_previous_direction(next_direction: Side) -> Side:
    if next_direction is Side.BOTTOM:
        return Side.TOP
    elif next_direction is Side.TOP:
        return Side.BOTTOM
    elif next_direction is Side.LEFT:
        return Side.RIGHT
    elif next_direction is Side.RIGHT:
        return Side.LEFT


def move_one(x, y, direction: Side) -> [int, int]:
    if direction is Side.BOTTOM:
        return [x, y - 1]
    elif direction is Side.TOP:
        return [x, y + 1]
    elif direction is Side.LEFT:
        return [x - 1, y]
    elif direction is Side.RIGHT:
        return [x + 1, y]


if __name__ == "__main__":
    # maze = Maze(5, 5)
    # maze.print_maze()

    # testing logic to determine if there is a possible route to exit - pre-generating maze
    horizontals = [[False, True, True], [False, True, False], [False, True, False], [True, False, True]]
    verticals = [[True, True, False, True], [True, False, False, True], [True, True, False, True]]
    maze = Maze(3, 3, horizontals, verticals, Wall(1, 2, Side.TOP), Wall(0, 1, Side.BOTTOM))
    solve_maze(maze)
