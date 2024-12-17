from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

DIRECTIONAL_HELPER_LIST = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
X_DIRECTIONAL_HELPER_LIST = [[[-1,-1],[1,1]],[[-1,1],[1,-1]]]

def parse_puzzle_matrix(input_data: list[str]):
    puzzle_matrix = []

    for row in input_data:
        puzzle_matrix.append(list(row))

    return puzzle_matrix


def count_xmas(puzzle_matrix: list[list[str]]):
    xmas_count = 0

    for row in range(len(puzzle_matrix)):
        for col in range(len(puzzle_matrix[0])):
            if puzzle_matrix[row][col] == 'X':
                for row_delta, col_delta in DIRECTIONAL_HELPER_LIST:
                    try:
                        if ((row + (row_delta * 3)) >= 0 # Prevent negative wrap-around
                                and (col + (col_delta * 3)) >= 0 # Prevent negative wrap-around
                                and puzzle_matrix[row + row_delta][col + col_delta] == 'M'
                                and puzzle_matrix[row + (row_delta * 2)][col + (col_delta * 2)] == 'A'
                                and puzzle_matrix[row + (row_delta * 3)][col + (col_delta * 3)] == 'S'):
                            xmas_count += 1
                    except IndexError:
                        # Do nothing and keep checking; we hit the border of the puzzle!
                        pass

    return xmas_count

def count_x_mas(puzzle_matrix: list[list[str]]):
    x_mas_count = 0

    for row in range(len(puzzle_matrix)):
        for col in range(len(puzzle_matrix[0])):
            if puzzle_matrix[row][col] == 'A':
                correct_arm = 0 # Check for two correct "arms" to the X-MAS
                for x_dir in X_DIRECTIONAL_HELPER_LIST:
                    has_m = False
                    has_s = False
                    for row_delta, col_delta in x_dir:
                        try:
                            if ((row + row_delta) >= 0 # Prevent negative wrap-around
                                    and (col + col_delta) >= 0): # Prevent negative wrap-around
                                has_m = has_m or puzzle_matrix[row + row_delta][col + col_delta] == 'M'
                                has_s = has_s or puzzle_matrix[row + row_delta][col + col_delta] == 'S'
                        except IndexError:
                            # Do nothing and keep checking; we hit the border of the puzzle!
                            pass
                    if has_m and has_s: correct_arm += 1
                if correct_arm == 2: x_mas_count += 1

    return x_mas_count


@register_solution(2024, 4, 1)
def part_one(input_data: list[str]):
    puzzle_matrix = parse_puzzle_matrix(input_data)

    answer = count_xmas(puzzle_matrix)

    if not answer:
        raise SolutionNotFoundError(2024, 4, 1)

    return answer


@register_solution(2024, 4, 2)
def part_two(input_data: list[str]):

    puzzle_matrix = parse_puzzle_matrix(input_data)

    answer = count_x_mas(puzzle_matrix)

    if not answer:
        raise SolutionNotFoundError(2024, 4, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 4)
    part_one(data)
    part_two(data)
