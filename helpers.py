class Position(object):
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __repr__(self):
        return "%s (%d,%d)" % (self.__class__.__name__, self.row, self.column)

    def moveUp(self):
        return Position(row=self.row-1, column=self.column)

    def moveDown(self):
        return Position(row=self.row+1, column=self.column)

    def moveRight(self):
        return Position(row=self.row, column=self.column+1)

    def moveLeft(self):
        return Position(row=self.row, column=self.column-1)


class Reward(object):
    def __init__(self, value, row, column, name):
        self.value = value
        self.position = Position(row, column)
        self.name = name


class Movement(object):
    def __init__(self, current_position, desired_position):
        self.current_position = current_position
        self.desired_position = desired_position

    def __eq__(self, other):
        return self.current_position == other.current_position and self.desired_position == other.desired_position

    def __repr__(self):
        return "%s from %s to %s" % (self.__class__.__name__, self.current_position, self.desired_position)

    def reverse(self):
        return Movement(current_position=self.desired_position, desired_position=self.current_position)
