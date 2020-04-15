from coordinate import Side, Status


class Multiple:
    def __init__(self, x, y, directions_tried, routes_available):
        self.x = x
        self.y = y
        self.no_options = False

        self.directions_tried = directions_tried
        # this ensures walls are added to directions_tried
        if Side.TOP not in routes_available:
            self.directions_tried.append(Side.TOP)
        elif Side.BOTTOM not in routes_available:
            self.directions_tried.append(Side.BOTTOM)
        elif Side.LEFT not in routes_available:
            self.directions_tried.append(Side.LEFT)
        elif Side.RIGHT not in routes_available:
            self.directions_tried.append(Side.RIGHT)

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
        self.current_path_after_multiple = []
        self.previous_direction = None
        self.next_direction = None

    def add_multiple(self, multiple):
        if len(self.multiples) != 0:
            self.paths_between_multiples.append(self.current_path_after_multiple)
        self.multiples.append(multiple)

    # cycles back through multiples finding last one with an untried route
    def get_next_viable_multiple(self, coordinates) -> Multiple:
        try:
            if not self.multiples[-1].no_options:
                return self.multiples[-1]
            else:
                for x_y in self.paths_between_multiples[-1]:
                    coordinates.update_coordinate(x_y[0], x_y[1], Status.X)
                coordinates.update_coordinate(self.multiples[-1].x, self.multiples[-1].y, Status.X)
                del self.multiples[-1]
                del self.paths_between_multiples[-1]
                return self.multiples[-1]
        except IndexError:
            raise UnsolvableMazeError("Maze cannot be solved")

    def check_coordinates_not_a_previous_multiple(self, x, y) -> bool:
        for multiple in self.multiples:
            if multiple.x is x and multiple.y is y:
                return False
        return True

    def add_direction_tried_from_current_multiple(self, side: Side):
        self.multiples[-1].add_direction_tried(side)

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class UnsolvableMazeError(Error):
    def __init__(self, message):
        self.message = message
