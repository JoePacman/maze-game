from maze import Maze
from coordinate import Side, Status, CoordinateArray


class Multiple:
    def __init__(self, x, y, previous_direction):
        self.x = x
        self.y = y
        self.directions_tried = [previous_direction]
        self.no_options = False

    def get_location(self) -> [int, int]:
        return [self.x, self.y]

    def add_direction_tried(self, side: Side):
        self.directions_tried.append(side)
        if Side.BOTTOM in self.directions_tried and Side.TOP in self.directions_tried \
                and Side.LEFT in self.directions_tried and Side.RIGHT in self.directions_tried:
            self.no_options = True

    def get_direction_untried(self, routes_available):
        if Side.TOP not in self.directions_tried and Side.TOP in routes_available:
            return Side.TOP
        elif Side.BOTTOM not in self.directions_tried and Side.BOTTOM in routes_available:
            return Side.BOTTOM
        elif Side.LEFT not in self.directions_tried and Side.LEFT in routes_available:
            return Side.LEFT
        elif Side.RIGHT not in self.directions_tried and Side.RIGHT in routes_available:
            return Side.RIGHT


class Tracking:
    # need to track each multiple and the directions tried from them
    def __init__(self):
        self.multiples = []
        self.paths_between_multiples = []

    def add_multiple(self, multiple, path_to_multiple=None):
        self.multiples.append(multiple)
        self.paths_between_multiples.append(path_to_multiple)

    # cycles back through multiples finding last one with an untried route
    def get_next_viable_multiple(self, coordinates) -> Multiple:
        if not self.multiples[-1].no_options:
            return self.multiples[-1]
        else:
            for [x, y] in self.paths_between_multiples:
                coordinates.update_coordinate(x, y, Status.X)
            coordinates.update_coordinate(self.multiples[-1].x, self.multiples[-1].y, Status.X)
            del self.multiples[-1]
            return self.multiples[-1]
        # TODO array index out of bounds handling

    def check_coordinates_not_a_previous_multiple(self, x, y) -> bool:
        for multiple in self.multiples:
            if multiple.x is x and multiple.y is y:
                return False
        return True

    def add_direction_trying_from_current_multiple(self, side: Side):
        self.multiples[-1].add_direction_tried(side)


def solve_maze(maze_i: Maze):
    coordinates = CoordinateArray(maze_i.width, maze_i.height)

    x = 0  # start x position
    y = 0  # start y position
    previous_direction = Side.BOTTOM  # entry point
    current_path_after_multiple = []
    exit_found = False
    tracking = Tracking()

    i = 0  # temp

    while exit_found is False:
        routes_available = maze.routes_available(coordinates.get_coordinate(x, y), previous_direction)
        if tracking.check_coordinates_not_a_previous_multiple(x, y):

            # dead end  - find last multiple with remaining routes to try
            if len(routes_available) is 0:
                coordinates.update_coordinate(x, y, Status.X)
                # update all coordinates in the path just taken as X
                for x_y in current_path_after_multiple:
                    coordinates.update_coordinate(x_y[0], x_y[1], Status.X)
                # TODO - if no way out this might throw an error?
                x, y = tracking.get_next_viable_multiple(coordinates).get_location()
                next_direction = tracking.get_next_viable_multiple(coordinates).get_direction_untried(routes_available)
                current_path_after_multiple = []
                continue

            # one route available - continue moving
            elif len(routes_available) is 1:
                next_direction = routes_available[0]
                coordinates.update_coordinate(x, y, Status.U)

            # FIRST time this multiple has been found
            if len(routes_available) > 1:
                next_direction = routes_available[0]
                multiple = Multiple(x, y, previous_direction)
                multiple.add_direction_tried(next_direction)
                tracking.add_multiple(multiple, current_path_after_multiple)
                coordinates.update_coordinate(x, y, Status.M)
                current_path_after_multiple = []

        # SUBSEQUENT time we have returned to this multiple
        else:
            next_direction = tracking.get_next_viable_multiple(coordinates).get_direction_untried(routes_available)
            tracking.add_direction_trying_from_current_multiple(next_direction)
            current_path_after_multiple = []

        current_path_after_multiple.append([x, y])
        x, y = move_one(x, y, next_direction)
        previous_direction = find_previous_direction(next_direction)

        maze_i.print_maze(coordinates)

        i += 1
        if i > 100:
            exit_found = True

        # TODO - check for if outside of 0 , 0 , width, height bounds for whether escaped maze


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
    horizontals = [[False, True, True, True], [False, True, False, False], [False, True, False, False], [True, True, True, False]]
    verticals = [[True, True, False, False, True], [True, False, False, True, True], [True, True, False, True, True]]
    maze = Maze(4, 3, horizontals, verticals)
    solve_maze(maze)
