from collections import defaultdict

from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

def parse_and_sort_lists(input_data: list[str]):
    list_a, list_b = [], []

    for line in input_data:
        values = line.strip().split()
        list_a.append(int(values[0]))
        list_b.append(int(values[1]))

    list_a.sort()
    list_b.sort()

    return list_a, list_b


@register_solution(2024, 1, 1)
def part_one(input_data: list[str]):
    answer = 0

    sorted_list_a, sorted_list_b = parse_and_sort_lists(input_data)

    for (value_a, value_b) in zip(sorted_list_a, sorted_list_b):
        answer += abs(value_a - value_b)

    if not answer:
        raise SolutionNotFoundError(2024, 1, 1)

    return answer


@register_solution(2024, 1, 2)
def part_two(input_data: list[str]):
    answer = 0

    sorted_list_a, sorted_list_b = parse_and_sort_lists(input_data)

    number_to_indices_a = defaultdict(list)
    for index, number in enumerate(sorted_list_a):
        number_to_indices_a[number].append(index)

    number_to_indices_b = defaultdict(list)
    for index, number in enumerate(sorted_list_b):
        number_to_indices_b[number].append(index)

    unique_numbers_a = list(number_to_indices_a.keys())

    for number in unique_numbers_a:
        a_count = len(number_to_indices_a[number]) or 0
        b_count = len(number_to_indices_b[number]) or 0
        answer += number * a_count * b_count

    if not answer:
        raise SolutionNotFoundError(2024, 1, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 1)
    part_one(data)
    part_two(data)
