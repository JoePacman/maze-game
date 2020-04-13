from maze import Maze
from coordinate import Side, Status, CoordinateArray
from tracking import Tracking, Multiple


def solve_maze(maze_i: Maze, start_x, start_y, entry_direction):
    coordinates = CoordinateArray(maze_i.width, maze_i.height)

    x = start_x
    y = start_y
    previous_direction = entry_direction
    current_path_after_multiple = []
    exit_found = False
    tracking = Tracking()
    maze_i.print_maze(coordinates)

    while exit_found is False:
        routes = maze.routes_available(coordinates.get_coordinate(x, y), previous_direction)
        if tracking.check_coordinates_not_a_previous_multiple(x, y):

            # dead end  - find last multiple with remaining routes to try
            if len(routes) is 0:
                coordinates.update_coordinate(x, y, Status.X)
                # update all coordinates in the path just taken as X
                for x_y in current_path_after_multiple:
                    coordinates.update_coordinate(x_y[0], x_y[1], Status.X)
                # TODO - if no way out this might throw an error?
                x, y = tracking.get_next_viable_multiple(coordinates).get_location()
                # not including previous direction in calculating new route because we don't know previous direction
                # from the last multiple (and when we initialised that multiple we added previous direction at the time
                # to its directions_tried
                routes_new = maze.routes_available(coordinates.get_coordinate(x, y))
                next_direction = tracking.get_next_viable_multiple(coordinates).get_direction_untried(routes_new)
                tracking.add_direction_trying_from_current_multiple(next_direction)
                current_path_after_multiple = []

            # one route available - continue moving
            elif len(routes) is 1:
                next_direction = routes[0]
                coordinates.update_coordinate(x, y, Status.C)
                current_path_after_multiple.append([x, y])

            # FIRST time this multiple has been found
            elif len(routes) > 1:
                next_direction = routes[0]
                multiple = Multiple(x, y, previous_direction)
                multiple.add_direction_tried(next_direction)
                tracking.add_multiple(multiple, current_path_after_multiple)
                coordinates.update_coordinate(x, y, Status.M)
                current_path_after_multiple = []

        # SUBSEQUENT time we have returned to this multiple
        else:
            routes_new = maze.routes_available(coordinates.get_coordinate(x, y))
            next_direction = tracking.get_next_viable_multiple(coordinates).get_direction_untried(routes_new)
            tracking.add_direction_trying_from_current_multiple(next_direction)
            current_path_after_multiple = []

        x, y = move_one(x, y, next_direction)
        previous_direction = find_previous_direction(next_direction)

        maze_i.print_maze(coordinates)

        if x < 0 or x is maze_i.width or y < 0 or y is maze_i.height:
            print("SUCCESS outside maze at position [%s, %s] (bottom left is [0, 0] " % (x, y))
            coordinates.update_path_found()
            maze_i.print_maze(coordinates)
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
    horizontals = [[True, True, True, True, True],
                   [False, False, True, False, False],
                   [False, False, True, False, False],
                   [True, False, False, True, False],
                   [True, True, True, True, False]]
    verticals = [[True, True, True, False, False, True],
                 [True, False, False, False, True, True],
                 [True, True, True, False, True, True],
                 [True, False, True, False, True, True]]
    maze = Maze(5, 4, horizontals, verticals)
    solve_maze(maze, 0, 0, Side.BOTTOM)
