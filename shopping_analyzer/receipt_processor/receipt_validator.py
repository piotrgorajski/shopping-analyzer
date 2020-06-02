import logging
from decimal import Decimal
from itertools import product

from functional import seq

invalid_receipt_items_count = 0
invalid_receipt_total_amounts = 0


def validate_receipts(receipts):
    seq(receipts).for_each(lambda receipt: validate_single_receipt(receipt))


def validate_single_receipt(receipt):
    validate_receipt_total_amount(receipt)
    validate_receipt_items(receipt)


def validate_receipt_total_amount(receipt):
    receipt_items_cost_sum = seq(receipt.items).map(lambda receipt_item: receipt_item.cost).sum()
    valid = receipt_items_cost_sum == receipt.total_amount
    if not valid:
        global invalid_receipt_total_amounts
        invalid_receipt_total_amounts += 1
        logging.error(
            f'[{receipt.source_file_name}] [{invalid_receipt_total_amounts}] Invalid receipt total amount detected. '
            f'Sum is: {receipt_items_cost_sum} while total is: {receipt.total_amount}')


def validate_receipt_items(receipt):
    seq(receipt.items) \
        .filter(lambda receipt_item: is_regular_item(receipt_item)) \
        .for_each(lambda receipt_item: validate_single_receipt_item(receipt_item, receipt.source_file_name))


def is_regular_item(receipt_item):
    # For discounts quantity will be None.
    # TODO Think of design improvement (type or flags for different item types)
    return receipt_item.quantity


def validate_single_receipt_item(receipt_item, source_file_name):
    valid = round(receipt_item.quantity * receipt_item.price, 2) == receipt_item.cost
    if not valid:
        global invalid_receipt_items_count
        invalid_receipt_items_count += 1
        logging.error(f'[{source_file_name}] [{invalid_receipt_items_count}] '
                      f'Invalid receipt item detected: {receipt_item}')
        fix_receipt_item_values(receipt_item.quantity, receipt_item.price, receipt_item.cost)


# TODO Refactor the code below
def fix_receipt_item_values(quantity, price, cost):
    equation = f'{quantity}|{price}|{cost}'
    all_eights_in_equation = equation.count('8')
    possible_combinations_count = 2 ** all_eights_in_equation
    # logging.info(f'Found {all_eights_in_equation} eight(s) in equation. '
    #              f'There will be {possible_combinations_count} possible combinations')
    combinations = set(product('08', repeat=all_eights_in_equation))
    # logging.info(f'Possible combinations are: {combinations}')

    foo = []
    for comb in combinations:
        counter = 0
        new_eq = equation
        # TODO There is some issue with this code. Combinations are repeated
        for i in range(0, len(equation)):
            if equation[i] == '8':
                new_eq = new_eq[:i] + comb[counter] + new_eq[i + 1:]
                foo.append(new_eq)
                counter += 1
        # logging.info(f'And the winner is: {new_eq}')
    # logging.info(f'Combinations: {foo}')
    bar = set()
    for new_eq in foo:
        eq_elems = new_eq.split('|')
        q = Decimal(eq_elems[0])
        p = Decimal(eq_elems[1])
        c = Decimal(eq_elems[2])
        # logging.info(f'candidate: {q} * {p} = {c}, so {q * p}')
        if round(q * p, 2) == c:
            bar.add(f'{q} * {p} = {c}')

    logging.info(f'And here is the fix: {bar}')
    # str(quantity).fin
