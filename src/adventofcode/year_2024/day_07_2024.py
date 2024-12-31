from adventofcode.util.exceptions import SolutionNotFoundError
from adventofcode.registry.decorators import register_solution
from adventofcode.util.input_helpers import get_input_for_day

def check_statement(statement: str, allow_concat = False):
    answer, equation = statement.strip().split(':')
    answer = int(answer)
    numeric_values = equation.strip().split(' ')

    return answer if check_statement_recursive(answer, numeric_values, allow_concat) else 0


'''
This version follows an "eval as you go" pattern, evaluating as we walk the recursive tree
instead of building a string and evaluating once at the end.

Turns out this is also faster than the old version at the bottom of this file, likely due to less string manipulation?
Or maybe due to less memory access / allocation?
'''
def check_statement_recursive(answer: int, numeric_values: list[str], allow_concat = False, previous_equation = ''):
    curr_eval = eval(previous_equation + numeric_values[0])

    # Check if this is the last numeric value, and evaluate if so.
    if len(numeric_values) == 1:
        return answer == curr_eval

    # Check plus '+', force ordering with parenthesis
    next_equation = str(curr_eval) + '+'
    if check_statement_recursive(answer, numeric_values[1:], allow_concat, next_equation):
        return True

    # Check times '*'
    next_equation = str(curr_eval) + '*'
    if check_statement_recursive(answer, numeric_values[1:], allow_concat, next_equation):
        return True

    if allow_concat:
        # Check concat operator '||'
        next_equation = str(curr_eval)
        if check_statement_recursive(answer, numeric_values[1:], allow_concat, next_equation):
            return True

    return False


@register_solution(2024, 7, 1)
def part_one(input_data: list[str]):
    answer = 0

    for statement in input_data:
        answer += check_statement(statement)

    if not answer:
        raise SolutionNotFoundError(2024, 7, 1)

    return answer


@register_solution(2024, 7, 2)
def part_two(input_data: list[str]):
    answer = 0

    for statement in input_data:
        answer += check_statement(statement, True)

    if not answer:
        raise SolutionNotFoundError(2024, 7, 2)

    return answer


if __name__ == '__main__':
    data = get_input_for_day(2024, 7)
    part_one(data)
    part_two(data)


'''
This was an older version building the full equation and only evaluating at the end. 
This process would be useful if the left-to-right forced ordering was no longer necessary.

This started to fall apart after I realized I needed to evaluate concat operators left-to-right like everything else, 
instead of before solving the normal math operators.
'''
# def check_statement_recursive(answer: int, numeric_values: list[str], allow_concat = False, previous_equation = ''):
#     # Check if this is the last numeric value, and evaluate if so.
#     if len(numeric_values) == 1:
#         previous_equation += numeric_values[0]
#         return answer == eval(previous_equation)
#
#     # Check plus '+', force ordering with parenthesis
#     next_equation = '(' + previous_equation + numeric_values[0] + ')+'
#     if check_statement_recursive(answer, numeric_values[1:], allow_concat, next_equation):
#         return True
#
#     # Check times '*', force ordering with parenthesis
#     next_equation = '(' + previous_equation + numeric_values[0] + ')*'
#     if check_statement_recursive(answer, numeric_values[1:], allow_concat, next_equation):
#         return True
#
#     if allow_concat:
#         # Check concat operator '||', evaluate the previous chunk to retain left-to-right ordering
#         left_eval = eval(previous_equation.rstrip('+*')) if len(previous_equation) > 0 else ''
#         next_equation = '' + str(left_eval) + numeric_values[0]
#         if check_statement_recursive(answer, numeric_values[1:], allow_concat, next_equation):
#             return True
#
#     return False