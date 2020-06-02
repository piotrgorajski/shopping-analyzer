import logging

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
            f'Sum is: {receipt_items_cost_sum} while total is: {receipt_items_cost_sum}')


def validate_receipt_items(receipt):
    seq(receipt.items) \
        .filter(lambda receipt_item: is_regular_item(receipt_item)) \
        .for_each(lambda receipt_item: validate_single_receipt_item(receipt_item, receipt.source_file_name))


def is_regular_item(receipt_item):
    # For discounts quantity will be None.
    # TODO Think of design improvement (type or flags for different item types)
    return receipt_item.quantity


def validate_single_receipt_item(receipt_item, source_file_name):
    valid = receipt_item.quantity * receipt_item.price == receipt_item.cost
    if not valid:
        global invalid_receipt_items_count
        invalid_receipt_items_count += 1
        logging.error(f'[{source_file_name}] [{invalid_receipt_items_count}] '
                      f'Invalid receipt item detected: {receipt_item}')
