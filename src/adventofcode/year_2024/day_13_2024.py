from concurrent.futures import ThreadPoolExecutor, as_completed
from math import floor

from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

MAX_PRESSES = 100
A_BUTTON_COST = 3
B_BUTTON_COST = 1

class Coords:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Problem:
    def __init__(self, a_button: Coords, b_button: Coords, prize: Coords):
        self.a_button = a_button
        self.b_button = b_button
        self.prize = prize

def break_down_problems(input_data: list[str]):
    problems = []

    for x in range(0, len(input_data), 4):
        a_button = input_data[x]
        a_button = a_button.split(':')[1].split(',')
        a_button_x = a_button[0].strip().split('+')[1]
        a_button_y = a_button[1].strip().split('+')[1]
        a_button = Coords(int(a_button_x), int(a_button_y))

        b_button = input_data[x + 1]
        b_button = b_button.split(':')[1].split(',')
        b_button_x = b_button[0].strip().split('+')[1]
        b_button_y = b_button[1].strip().split('+')[1]
        b_button = Coords(int(b_button_x), int(b_button_y))

        prize = input_data[x + 2]
        prize = prize.split(':')[1].split(',')
        prize_x = prize[0].strip().split('=')[1]
        prize_y = prize[1].strip().split('=')[1]
        prize = Coords(int(prize_x), int(prize_y))

        problems.append(Problem(a_button, b_button, prize))

    return problems

def solve_prize_problem(problem):
    minimum_tokens = 0

    # maximize B, minimize A
    max_b_x = floor(problem.prize.x / problem.b_button.x)
    max_b_y = floor(problem.prize.y / problem.b_button.y)
    max_b = min(max_b_x, max_b_y)

    for b in range(max_b, 0, -1):
        print(b)
        leftover_x = problem.prize.x - (b * problem.b_button.x)
        leftover_y = problem.prize.y - (b * problem.b_button.y)
        if ((leftover_x % problem.a_button.x) == 0
                and (leftover_y % problem.a_button.y) == 0
                and leftover_x / problem.a_button.x == leftover_y / problem.a_button.y):
            a = leftover_x / problem.a_button.x
            minimum_tokens += int((a * A_BUTTON_COST) + (b * B_BUTTON_COST))
            break

    if minimum_tokens > 0:
        print(f'Token Solution: {minimum_tokens}')
    else:
        print('NO SOLUTION')

    return minimum_tokens


@register_solution(2024, 13, 1)
def part_one(input_data: list[str]):
    answer = 0

    problems = break_down_problems(input_data)

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        future_to_solution = {executor.submit(solve_prize_problem, problem): problem for problem in problems}
        for future in as_completed(future_to_solution):
            try:
                answer += future.result()
            except Exception as e:
                print(f"Error: {str(e)}")  # Handle any errors

    if not answer:
        raise SolutionNotFoundError(2024, 13, 1)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 13)
    part_one(data)
