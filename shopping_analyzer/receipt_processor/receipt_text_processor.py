import logging
import re

from functional import seq

from shopping_analyzer.receipt_processor.receipt import ReceiptItem, Receipt

receipt_pattern = re.compile(
    r".*www\.lidl\.pl\s*(?P<date>\d{4}-\d{2}-\d{2})(?P<items>.*)PTU A.*RAZEM PLN\s+(?P<total_amount>\d+,\d{2}).*",
    re.DOTALL)
item_pattern = re.compile(r"(?P<name>.+)\s+(?P<quantity>\d+)\s*\*\s+(?P<price>\d+,\d{2})\s+(?P<cost>\d+,\d{2})\s*.*")


def process_ocr_receipts(ocr_receipts):
    return seq(ocr_receipts) \
        .map(lambda ocr_receipt: process_single_text_receipt(ocr_receipt)) \
        .filter(None) \
        .to_list()


def process_single_text_receipt(ocr_receipt):
    # TODO Pass here also receipt metadata to be able to log invalid receipt filename
    receipt_match = re.match(receipt_pattern, ocr_receipt.receipt_text)
    if receipt_match:
        date = receipt_match.group('date')
        total_amount = receipt_match.group('total_amount')
        raw_receipt_items = receipt_match.group('items')
        receipt_items = extract_receipt_items(raw_receipt_items)
        # TODO Perform validation on items sum vs total amount
        # TODO Log as error any issues in the data
        return Receipt(date, receipt_items, total_amount)
    else:
        logging.error(f'Failed to match whole receipt: [{ocr_receipt.source_file_name}]')


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
