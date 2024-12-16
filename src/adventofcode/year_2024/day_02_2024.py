import string

from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

'''
The levels are either all increasing or all decreasing.
Any two adjacent levels differ by at least one and at most three.
'''

'''
This one got away from me... My initial solution was fairly straight-forward and worked well, then I missed a few 
small edge cases on Part 2: Allowing for a report to pass as SAFE if removing a single value in the list worked.

I DON'T like my tolerance implementation here, and this should be redone to properly check for these missed cases:
 - 26 28 27 29 31 (remove 28 and this works)
 - 26 28 27 26 25 (remove 26 and this works, but removing 28 doesn't)
'''

def is_safe_report(report: str, tolerance = 0):
    report_list = report.strip().split(' ')

    last_value = -1
    ascending = None
    for idx, value_str in enumerate(report_list):
        value = int(value_str)

        # Grab first value in list if necessary
        if last_value < 0:
            last_value = value
            continue

        level_delta = abs(value - last_value)

        # Safety Checks
        if ascending == True and value <= last_value:
            # Ascending list, but this value fails the ordering check. Unsafe report.
            # print(f'FAIL: ASC list, but {last_value} and {value} fail.')
            if tolerance > 0:
                alternate_a = report_list.copy()
                alternate_b = report_list.copy()
                alternate_c = report_list.copy()
                alternate_a.pop(idx - 1)
                alternate_b.pop(idx)
                alternate_c.pop(0)
                print(f'RERUN Report: {report}')
                return is_safe_report(' '.join(alternate_a), tolerance - 1) or is_safe_report(' '.join(alternate_b), tolerance - 1) or is_safe_report(' '.join(alternate_c), tolerance - 1)
            else:
                print(f'FAIL Report: {report}')
                return False

        elif ascending == False and value >= last_value:
            # Descending list, but this value fails the ordering check. Unsafe report.
            # print(f'FAIL: DESC list, but {last_value} and {value} fail.')
            if tolerance > 0:
                alternate_a = report_list.copy()
                alternate_b = report_list.copy()
                alternate_c = report_list.copy()
                alternate_a.pop(idx - 1)
                alternate_b.pop(idx)
                alternate_c.pop(0)
                print(f'RERUN Report: {report}')
                return is_safe_report(' '.join(alternate_a), tolerance - 1) or is_safe_report(' '.join(alternate_b), tolerance - 1) or is_safe_report(' '.join(alternate_c), tolerance - 1)
            else:
                print(f'FAIL Report: {report}')
                return False
        elif level_delta < 1 or level_delta > 3:
            # print(f'FAIL: Level Delta between {last_value} and {value} fails.')
            if tolerance > 0:
                alternate_a = report_list.copy()
                alternate_b = report_list.copy()
                alternate_c = report_list.copy()
                alternate_a.pop(idx - 1)
                alternate_b.pop(idx)
                alternate_c.pop(0)
                print(f'RERUN Report: {report}')
                return is_safe_report(' '.join(alternate_a), tolerance - 1) or is_safe_report(' '.join(alternate_b), tolerance - 1) or is_safe_report(' '.join(alternate_c), tolerance - 1)
            else:
                print(f'FAIL Report: {report}')
                return False
        elif ascending is None:
            # Undecided on direction; make the decision and track for the next values.
            ascending = value > last_value

        # Update last_value for next iteration
        last_value = value

    # All conditions passed, so this is a safe report.
    print(f'SAFE Report: {report}')
    return True

@register_solution(2024, 2, 1)
def part_one(input_data: list[str]):
    answer = 0

    for report in input_data:
        answer += int(is_safe_report(report))

    if not answer:
        raise SolutionNotFoundError(2024, 2, 1)

    return answer


@register_solution(2024, 2, 2)
def part_two(input_data: list[str]):
    answer = 0

    for report in input_data:
        answer += int(is_safe_report(report, 1))

    if not answer:
        raise SolutionNotFoundError(2024, 2, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 2)
    part_one(data)
    part_two(data)
