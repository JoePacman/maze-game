from maze import Maze
from coordinate import Side, Status, CoordinateArray
from tracking import Tracking, Multiple, UnsolvableMazeError


def solve_maze(maze_i: Maze, start_x, start_y):

    coordinates = CoordinateArray(maze_i.width, maze_i.height)
    x = start_x
    y = start_y
    tracking = Tracking()
    exit_found = False

    def multiple_paths_actions():
        routes_new = maze.routes_available(coordinates.get_coordinate(x, y))
        tracking.next_direction = tracking.get_next_viable_multiple(coordinates).get_direction_untried(routes_new)
        tracking.add_direction_tried_from_current_multiple(tracking.next_direction)
        tracking.current_path_after_multiple = []

    while exit_found is False:
        if tracking.check_coordinates_not_a_previous_multiple(x, y):
            routes_available = maze.routes_available(coordinates.get_coordinate(x, y), tracking.previous_direction)

            # dead end  - find last multiple with remaining routes to try
            if len(routes_available) is 0:
                coordinates.update_coordinate(x, y, Status.X)
                # update all coordinates in current path to X (don't include the M)
                for x_y in tracking.current_path_after_multiple:
                     coordinates.update_coordinate(x_y[0], x_y[1], Status.X)
                # reset x, y back to multiples position
                x, y = tracking.get_next_viable_multiple(coordinates).get_location()
                coordinates.update_coordinate(x, y, Status.M)
                multiple_paths_actions()

            # one route available - continue moving
            elif len(routes_available) is 1:
                tracking.next_direction = routes_available[0]
                coordinates.update_coordinate(x, y, Status.C)
                tracking.current_path_after_multiple.append([x, y])

            # more than one route available - (FIRST time) multiple found
            elif len(routes_available) > 1:
                tracking.next_direction = routes_available[0]
                coordinates.update_coordinate(x, y, Status.M)
                tracking.add_multiple(Multiple(x, y, [tracking.previous_direction, tracking.next_direction],
                                               routes_available))

        # SUBSEQUENT time we have returned to this multiple
        else:
            multiple_paths_actions()

        x, y = move_one(x, y, tracking.next_direction)
        tracking.previous_direction = find_previous_direction(tracking.next_direction)

        maze_i.print_maze(coordinates)

        if x < 0 or x is maze_i.width or y < 0 or y is maze_i.height:
            coordinates.update_path_found()
            maze_i.print_maze(coordinates)
            print("SUCCESS outside maze at position [%s, %s] (bottom left is [0, 0])" % (x, y))
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
    horizontals = [[True, True, True, True, True, True, True, True],
                   [False, False, False, True, False, False, True, False],
                   [False, False, False, True, False, False, False, True],
                   [False, True, False, False, True, False, True, False],
                   [True, True, True, True, True, True, False, True]]
    verticals = [[True, True, True, True, False, False, True, False, True],
                 [True, True, False, False, False, True, True, False, True],
                 [True, False, True, True, False, True, False, False, True],
                 [True, True, False, True, False, True, True, False, True]]
    maze = Maze(8, 4, horizontals, verticals)
    try:
        solve_maze(maze, 1, 0)
    except UnsolvableMazeError:
        print("FAILURE - cannot find way out!")
