import logging
import re
from decimal import Decimal
from itertools import product

from shopping_analyzer.receipt_processor.receipt import ReceiptItem


def fix_receipt_item_values(receipt_item):
    equation = f'{receipt_item.quantity}*{receipt_item.price}={receipt_item.cost}'
    combinations = prepare_possible_zero_eight_combinations(equation)
    alternative_equations = prepare_new_equations_for_each_combination(combinations, equation)
    valid_alternative_equation = find_valid_alternative_equation(alternative_equations)
    if valid_alternative_equation:
        return produce_fixed_receipt_item(receipt_item, valid_alternative_equation)


def prepare_possible_zero_eight_combinations(equation):
    all_eights_in_equation = equation.count('8')
    return set(product('08', repeat=all_eights_in_equation))


def prepare_new_equations_for_each_combination(combinations, equation):
    alternative_equations = []
    for combination in combinations:
        counter = 0
        alternative_equation = equation
        for i in range(0, len(equation)):
            if equation[i] == '8':
                alternative_equation = alternative_equation[:i] + combination[counter] + alternative_equation[i + 1:]
                counter += 1
        alternative_equations.append(alternative_equation)
    return alternative_equations


def find_valid_alternative_equation(alternative_equations):
    valid_equations = set()
    for alternative_equation in alternative_equations:
        equation_elements = re.split('[*=]', alternative_equation)
        quantity = Decimal(equation_elements[0])
        price = Decimal(equation_elements[1])
        cost = Decimal(equation_elements[2])
        if round(quantity * price, 2) == cost:
            valid_equations.add(f'{quantity}*{price}={cost}')
    if len(valid_equations) == 1:
        return valid_equations.pop()
    elif len(valid_equations) > 1:
        logging.warning(f"Multiple valid alternative equations found: {valid_equations}")


def produce_fixed_receipt_item(receipt_item, valid_alternative_equation):
    equation_elements = re.split('[*=]', valid_alternative_equation)
    return ReceiptItem(receipt_item.name, equation_elements[0], equation_elements[1], equation_elements[2])
