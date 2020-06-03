import logging

from functional import seq

from shopping_analyzer.receipt_processor.zero_eight_fixer import fix_receipt_item_values

invalid_receipt_items_count = 0
invalid_receipt_total_amounts = 0


def validate_receipts(receipts):
    return seq(receipts).map(lambda receipt: validate_single_receipt(receipt)).to_list()


def validate_single_receipt(receipt):
    fixed_receipt_items = validate_receipt_items(receipt)
    fixed_receipt = receipt.replace_receipt_items(fixed_receipt_items)
    validate_receipt_total_amount(fixed_receipt)
    return fixed_receipt


def validate_receipt_total_amount(receipt):
    receipt_items_cost_sum = seq(receipt.items).map(lambda receipt_item: receipt_item.cost).sum()
    valid = receipt_items_cost_sum == receipt.total_amount
    if not valid:
        global invalid_receipt_total_amounts
        invalid_receipt_total_amounts += 1
        # logging.error(
        #     f'[{receipt.source_file_name}] [{invalid_receipt_total_amounts}] Invalid receipt total amount detected. '
        #     f'Sum is: {receipt_items_cost_sum} while total is: {receipt.total_amount}')


def validate_receipt_items(receipt):
    return seq(receipt.items) \
        .map(lambda receipt_item: validate_single_receipt_item(receipt_item, receipt.source_file_name)) \
        .to_list()


def validate_single_receipt_item(receipt_item, source_file_name):
    if is_regular_item(receipt_item):
        valid = round(receipt_item.quantity * receipt_item.price, 2) == receipt_item.cost
        if not valid:
            fixed_receipt_item = fix_receipt_item_values(receipt_item)
            if fixed_receipt_item:
                return fixed_receipt_item
            else:
                global invalid_receipt_items_count
                invalid_receipt_items_count += 1
                logging.error(f'[{source_file_name}] [{invalid_receipt_items_count}] '
                              f'Invalid receipt item detected: {receipt_item}')
                return receipt_item.mark_as_invalid()
    return receipt_item


def is_regular_item(receipt_item):
    # For discounts quantity will be None.
    # TODO Think of design improvement (type or flags for different item types)
    return receipt_item.quantity
