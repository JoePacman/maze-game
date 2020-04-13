from coordinate import Side, Status


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

    def check_coordinates_not_a_previous_multiple(self, x, y) -> bool:
        for multiple in self.multiples:
            if multiple.x is x and multiple.y is y:
                return False
        return True

    def add_direction_trying_from_current_multiple(self, side: Side):
        self.multiples[-1].add_direction_tried(side)