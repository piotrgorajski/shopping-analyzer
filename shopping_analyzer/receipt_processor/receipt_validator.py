import logging

from functional import seq


def validate_receipts(receipts):
    seq(receipts).for_each(lambda receipt: validate_single_receipt)


def validate_single_receipt(receipt):
    validate_receipt_total_amount(receipt)
    validate_receipt_items(receipt)


def validate_receipt_total_amount(receipt):
    receipt_items_cost_sum = seq(receipt.items).map(lambda receipt_item: receipt_item.cost).sum()
    valid = receipt_items_cost_sum == receipt.total_amount
    if not valid:
        logging.error(f'Invalid receipt total amount detected: {receipt.source_file_name}. '
                      f'Sum is: {receipt_items_cost_sum} while total is: {receipt_items_cost_sum}')


def validate_receipt_items(receipt):
    seq(receipt.items) \
        .filter(lambda receipt_item: is_regular_item(receipt_item)) \
        .for_each(lambda receipt_item: validate_single_receipt_item)


def is_regular_item(receipt_item):
    # For discounts quantity will be None.
    # TODO Think of design improvement (type or flags for different item types)
    return receipt_item.quantity


def validate_single_receipt_item(receipt_item):
    valid = receipt_item.quantity * receipt_item.price == receipt_item.cost
    if not valid:
        logging.error(f'Invalid receipt item detected: {receipt_item}')
