import re

from functional import seq

from shopping_analyzer.receipt_processor.receipt import ReceiptItem, Receipt

item_pattern = re.compile(r"(?P<name>.+)\s+(?P<quantity>\d+)\s*\*\s+(?P<price>\d+,\d{2})\s+(?P<cost>\d+,\d{2})\s*.*")


def process_text_receipts(text_receipts):
    return list(map(lambda text_receipt: process_single_text_receipt(text_receipt), text_receipts))


def process_single_text_receipt(text_receipt):
    date = extract_receipt_date(text_receipt)
    total_amount = extract_receipt_total_amount(text_receipt)
    receipt_items = extract_receipt_items(text_receipt)
    # TODO Perform validation on items sum vs total amount
    # TODO Log as error any issues in the data
    return Receipt(date, receipt_items, total_amount)


def extract_receipt_date(text_receipt):
    return re.findall(r".*www\.lidl\.pl\s*(\d{4}-\d{2}-\d{2}).*", text_receipt)


def extract_receipt_total_amount(text_receipt):
    return re.findall(r".*RAZEM PLN\s+(\d+,\d{2}).*", text_receipt)


def extract_receipt_items(text_receipt):
    text_receipt_items = re.findall(r".*www\.lidl\.pl\s*\d{4}-\d{2}-\d{2}(.*)PTU A.*", text_receipt, re.DOTALL)
    if not text_receipt_items:
        # TODO Figure out the issue here and apply a fix (IndexError: list index out of range)
        return []
    else:
        text_receipt_item_lines = text_receipt_items[0].splitlines()
        # no_blanks_items = filter(lambda item: not item, text_receipt_item_lines)
        return seq(text_receipt_item_lines) \
            .map(lambda text_receipt_item: parse_single_receipt_item(text_receipt_item)) \
            .filter(None) \
            .to_list()


def parse_single_receipt_item(text_receipt_item):
    item_match = re.match(item_pattern, text_receipt_item)
    # TODO Add more complex filtering (lidl discounts)
    if item_match:
        return parse_matching_text_receipt_item(item_match)


def parse_matching_text_receipt_item(item_match):
    # TODO Perform validation on items like if the a * b = c
    # TODO Log as error any issues in the data
    name = item_match.group('name')
    quantity = item_match.group('quantity')
    price = item_match.group('price')
    cost = item_match.group('cost')
    # print(f"printed: {name}: {quantity} * {price} = {cost}")
    return ReceiptItem(name, quantity, price, cost)
