import math
import re

from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

PART_ONE_MULTI_REGEX = re.compile(r"mul\((\d{1,3},\d{1,3})\)")
PART_TWO_DONT_REGEX = re.compile(r"(don't\(\)).*?(do\(\))")

@register_solution(2024, 3, 1)
def part_one(input_data: list[str]):
    answer = 0

    valid_multis = re.findall(PART_ONE_MULTI_REGEX, ''.join(input_data))

    for multi in valid_multis:
        answer += math.prod([int(factor) for factor in multi.split(',')])

    if not answer:
        raise SolutionNotFoundError(2024, 3, 1)

    return answer


@register_solution(2024, 3, 2)
def part_two(input_data: list[str]):
    answer = 0

    # Find and replace text between valid don't() and do() statements with an empty string, deleting those sections
    valid_input_data = re.sub(PART_TWO_DONT_REGEX, '', ''.join(input_data))
    valid_multis = re.findall(PART_ONE_MULTI_REGEX, ''.join(valid_input_data))

    for multi in valid_multis:
        answer += math.prod([int(factor) for factor in multi.split(',')])


    if not answer:
        raise SolutionNotFoundError(2024, 3, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 3)
    part_one(data)
    part_two(data)
