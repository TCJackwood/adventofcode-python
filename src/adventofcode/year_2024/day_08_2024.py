from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

def parse_data(input_data: list[str]):
    antennas = dict()

    rows = len(input_data)
    cols = len(input_data[0])

    for row_Id, row in enumerate(input_data):
        for col_Id, char in enumerate(row):
            if char != '.':
                antenna_locs = antennas.setdefault(char, [])
                antenna_locs.append((row_Id, col_Id))

    return antennas, rows, cols

def count_antinodes(antennas: dict, rows: int, cols: int):
    antinodes = set()

    for antenna_type in antennas.keys():
        antenna_locs = antennas[antenna_type]
        for i in range(0, len(antenna_locs) - 1):
            base_antenna = antenna_locs[i]
            for j in range(i + 1, len(antenna_locs)):
                next_antenna = antenna_locs[j]

                row_diff = next_antenna[0] - base_antenna[0]
                col_diff = next_antenna[1] - base_antenna[1]

                # Antinode 1
                antinode_1_row = base_antenna[0] - row_diff
                antinode_1_col = base_antenna[1] - col_diff
                if 0 <= antinode_1_row < rows and 0 <= antinode_1_col < cols:
                    antinodes.add((antinode_1_row, antinode_1_col))

                # Antinode 2
                antinode_2_row = next_antenna[0] + row_diff
                antinode_2_col = next_antenna[1] + col_diff
                if 0 <= antinode_2_row < rows and 0 <= antinode_2_col < cols:
                    antinodes.add((antinode_2_row, antinode_2_col))

    return len(antinodes)


def count_resonant_antinodes(antennas: dict, rows: int, cols: int):
    antinodes = set()

    for antenna_type in antennas.keys():
        antenna_locs = antennas[antenna_type]
        for i in range(0, len(antenna_locs) - 1):
            base_antenna = antenna_locs[i]
            for j in range(i + 1, len(antenna_locs)):
                next_antenna = antenna_locs[j]

                # Add the antennas themselves
                antinodes.add(base_antenna)
                antinodes.add(next_antenna)

                row_diff = next_antenna[0] - base_antenna[0]
                col_diff = next_antenna[1] - base_antenna[1]

                # Climb one direction until we are off of the allowed map
                antinode_row = base_antenna[0] - row_diff
                antinode_col = base_antenna[1] - col_diff
                while 0 <= antinode_row < rows and 0 <= antinode_col < cols:
                    antinodes.add((antinode_row, antinode_col))
                    antinode_row -= row_diff
                    antinode_col -= col_diff

                # Climb the other direction until we are off of the allowed map
                antinode_row = next_antenna[0] + row_diff
                antinode_col = next_antenna[1] + col_diff
                while 0 <= antinode_row < rows and 0 <= antinode_col < cols:
                    antinodes.add((antinode_row, antinode_col))
                    antinode_row += row_diff
                    antinode_col += col_diff

    return len(antinodes)


@register_solution(2024, 8, 1)
def part_one(input_data: list[str]):
    antennas, rows, cols = parse_data(input_data)

    answer = count_antinodes(antennas, rows, cols)

    if not answer:
        raise SolutionNotFoundError(2024, 8, 1)

    return answer


@register_solution(2024, 8, 2)
def part_two(input_data: list[str]):
    antennas, rows, cols = parse_data(input_data)

    answer = count_resonant_antinodes(antennas, rows, cols)

    if not answer:
        raise SolutionNotFoundError(2024, 8, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 8)
    part_one(data)
    part_two(data)
