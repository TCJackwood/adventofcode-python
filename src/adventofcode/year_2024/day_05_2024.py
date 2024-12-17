from math import floor

from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

class Rule:
    def __init__(self, rule_code: str):
        self.initial_page, self.following_page = rule_code.strip().split('|')

    def check(self, update: str):
        try:
            last_initial_page_index = update.rindex(self.initial_page)
            return False if update.find(self.following_page, 0, last_initial_page_index) > -1 else True
        except ValueError:
            # Either or both pages aren't in the update, so the update passes this rule check
            return True

    def apply_fix(self, update: str):
        update_page_list = update.strip().split(',')

        # Assume pages don't occur multiple times
        # Assume there are no impossible rule combinations
        first_page_index = update_page_list.index(self.initial_page)
        second_page_index = update_page_list.index(self.following_page)

        update_page_list[first_page_index], update_page_list[second_page_index] = update_page_list[second_page_index], update_page_list[first_page_index]

        return ','.join(update_page_list)


def parse_inputs(input_data: list[str]):
    rule_data: [Rule] = []
    update_data: [str] = []

    for line in input_data:
        if line.find('|') > -1:
            rule_data.append(Rule(line))
        elif len(line) > 0:
            update_data.append(line)

    return rule_data, update_data


def get_middle_page_num(update: str):
    update_pages = update.split(',')
    return int(update_pages[floor(len(update_pages)/2)])


@register_solution(2024, 5, 1)
def part_one(input_data: list[str]):
    rule_data, update_data = parse_inputs(input_data)

    answer = 0

    for update in update_data:
        valid_update = True
        for rule in rule_data:
            if not rule.check(update):
                valid_update = False
                break
        if valid_update:
            answer += get_middle_page_num(update)

    if not answer:
        raise SolutionNotFoundError(2024, 5, 1)

    return answer


'''
Messy recursion here; TODO would be to clean this up and make it much more readable. But it works!
'''
@register_solution(2024, 5, 2)
def part_two(input_data: list[str]):
    rule_data, update_data = parse_inputs(input_data)

    answer = 0

    def recheck_and_apply_rules(update):
        for rule in rule_data:
            if not rule.check(update):
                update = rule.apply_fix(update)
                update = recheck_and_apply_rules(update)

        return update

    for update in update_data:
        valid_update = True
        for rule in rule_data:
            if not rule.check(update):
                valid_update = False
                update = rule.apply_fix(update)
                update = recheck_and_apply_rules(update)
        if not valid_update:
            answer += get_middle_page_num(update)

    if not answer:
        raise SolutionNotFoundError(2024, 5, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 5)
    part_one(data)
    part_two(data)
