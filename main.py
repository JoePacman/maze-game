import numpy as np


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.horizontals = [[False] * width for i in range(height + 1)]
        self.verticals = [[False] * (width + 1) for i in range(height)]

        self.setup_maze()

    def print_maze(self):
        # printing rows in backward order so [0, 0] is bottom left of print out.
        for i in range(1, self.height + 1):
            print_row(self.horizontals[-i], ' ───')
            print_row(self.verticals[-i], '|   ')
        print_row(self.horizontals[-self.height - 1], ' ───')

    def setup_maze(self):
        # set edges
        self.horizontals[0] = [True for i in range(self.width)]
        self.horizontals[self.height] = [True for i in range(self.width)]
        for i in range(0, self.height):
            self.verticals[i][0] = True
            self.verticals[i][self.width] = True

        # set entry point
        self.horizontals[0][0] = False
        # set exit point
        self.verticals[self.height - 1][self.width] = False




def print_row(row, value):
    print(''.join(value if elem else '    ' for elem in row))


if __name__ == "__main__":
    maze = Maze(15, 12)
    maze.print_maze()
