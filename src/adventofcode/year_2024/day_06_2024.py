from enum import Enum

from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

DIRECTION_CHARS = ['^','>','v','<']
OBSTACLE_CHAR = '#'

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @staticmethod
    def get_guard_direction_from_char(guard_char):
        guard_dir = None
        if guard_char == '^':
            guard_dir = Direction.NORTH
        elif guard_char == '>':
            guard_dir = Direction.EAST
        elif guard_char == 'v':
            guard_dir = Direction.SOUTH
        elif guard_char == '<':
            guard_dir = Direction.WEST
        return guard_dir

    def turn_right(self):
        return Direction((self.value + 1) % 4)

class Guard:
    def __init__(self, row: int, col: int, direction: Direction):
        self.row = row
        self.col = col
        self.direction = direction

    def curr_pos(self):
        return f'[{self.row},{self.col}]'

    def take_a_step(self, obstacle_positions):
        next_row, next_col = self.row, self.col

        if self.direction == Direction.NORTH:
            next_row -= 1
        elif self.direction == Direction.EAST:
            next_col += 1
        elif self.direction == Direction.SOUTH:
            next_row += 1
        elif self.direction == Direction.WEST:
            next_col -= 1

        if [next_row, next_col] in obstacle_positions:
            self.direction = self.direction.turn_right()
        else:
            self.row, self.col = next_row, next_col

def parse_inputs(input_data: list[str]):
    map_matrix = []
    guard_row = -1
    guard_col = -1
    guard_dir = None
    obstacle_positions = []

    for row_idx, row in enumerate(input_data):
        map_matrix.append(list(row))

        for col_idx, character in enumerate(row):
            # Search for the guard's initial position
            if character in DIRECTION_CHARS:
                guard_dir = Direction.get_guard_direction_from_char(character)
                guard_row, guard_col = row_idx, col_idx

            # Build obstacle positions list
            if character == OBSTACLE_CHAR:
                obstacle_positions.append([row_idx, col_idx])

    guard_vector = Guard(guard_row, guard_col, guard_dir)

    max_row, max_col = len(input_data), len(input_data[0])

    return map_matrix, guard_vector, obstacle_positions, max_row, max_col


@register_solution(2024, 6, 1)
def part_one(input_data: list[str]):

    map_matrix, guard_vector, obstacle_positions, max_row, max_col = parse_inputs(input_data)
    unique_position_set = set()

    print('Guard', '[', guard_vector.row, ',', guard_vector.col, ']', guard_vector.direction)

    def guard_in_play():
        return -1 < guard_vector.row < max_row and -1 < guard_vector.col < max_col

    while guard_in_play():
        unique_position_set.add(guard_vector.curr_pos())
        guard_vector.take_a_step(obstacle_positions)

    answer = len(unique_position_set)

    if not answer:
        raise SolutionNotFoundError(2024, 6, 1)

    return answer


# @register_solution(2024, 6, 2)
# def part_two(input_data: list[str]):
#     answer = ...
#
#     if not answer:
#         raise SolutionNotFoundError(2024, 6, 2)
#
#     return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 6)
    part_one(data)
    # part_two(data)
