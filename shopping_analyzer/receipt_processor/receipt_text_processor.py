import logging
import re

from functional import seq

from shopping_analyzer.receipt_processor.receipt import ReceiptItem, Receipt

failed_receipts_count = 0
all_receipt_items_count = 0
failed_receipt_items_count = 0

receipt_pattern = re.compile(
    r".*www\.lidl\.pl\s*(?P<date>\d{4}-\d{2}-\d{2})(?P<items>.*)PTU A.*RAZEM PLN\s+(?P<total_amount>\d+,\d{2}).*",
    re.DOTALL)

regular_item_pattern = re.compile(
    r"(?P<name>.+)\s+(?P<quantity>\d+(,\s*\d{2,3})?)\s*[* ]\s*(?P<price>\d+,\s*\d{2})\s+(?P<cost>\d+,\s*\d{2})\s*.*")

lidl_plus_discount_item_pattern = re.compile(r"Lidl Plus rabat\s+-(?P<discount_amount>\d+,\s*\d{2})")

common_discount_item_pattern = re.compile(r"^(?!Lidl Plus rabat).*\s+-(?P<discount_amount>\d+,\s*\d{2})")


def process_ocr_receipts(ocr_receipts):
    return seq(ocr_receipts) \
        .map(lambda ocr_receipt: process_single_text_receipt(ocr_receipt)) \
        .filter(None) \
        .to_list()


def process_single_text_receipt(ocr_receipt):
    receipt_match = re.match(receipt_pattern, ocr_receipt.receipt_text)
    if receipt_match:
        date = receipt_match.group('date')
        total_amount = receipt_match.group('total_amount')
        raw_receipt_items = receipt_match.group('items')
        receipt_items = extract_receipt_items(raw_receipt_items, ocr_receipt)
        # logging.info(f"Count of all receipt items is: {all_receipt_items_count}")
        return Receipt(ocr_receipt.source_file_name, date, receipt_items, total_amount)
    else:
        global failed_receipts_count
        failed_receipts_count += 1
        # logging.error(f'{failed_receipts_count} Failed to match whole receipt: [{ocr_receipt.source_file_name}]')


def extract_receipt_items(text_receipt, ocr_receipt):
    text_receipt_item_lines = text_receipt.splitlines()
    return seq(text_receipt_item_lines) \
        .filter(None) \
        .map(lambda text_receipt_item: clean_text_receipt_item(text_receipt_item)) \
        .map(lambda text_receipt_item: parse_single_receipt_item(text_receipt_item, ocr_receipt)) \
        .filter(None) \
        .to_list()


def parse_single_receipt_item(text_receipt_item, ocr_receipt):
    # TODO Handle such counts somehow nicer
    global all_receipt_items_count
    all_receipt_items_count += 1

    regular_item_match = re.match(regular_item_pattern, text_receipt_item)
    lidl_plus_discount_item_match = re.match(lidl_plus_discount_item_pattern, text_receipt_item)
    common_discount_item_match = re.match(common_discount_item_pattern, text_receipt_item)
    if regular_item_match:
        return parse_matching_regular_item(regular_item_match)
    elif lidl_plus_discount_item_match:
        return parse_matching_lidl_plus_discount_item(lidl_plus_discount_item_match)
    elif common_discount_item_match:
        return parse_matching_common_discount_item(common_discount_item_match)
    else:
        global failed_receipt_items_count
        failed_receipt_items_count += 1
        logging.error(
            f'{failed_receipt_items_count} Failed to process following receipt item [{ocr_receipt.source_file_name}]: {text_receipt_item}')


def clean_text_receipt_item(text_receipt_item):
    return text_receipt_item \
        .replace('%', '') \
        .replace('\\', '') \
        .replace('/', '')


def parse_matching_regular_item(item_match):
    name = item_match.group('name')
    quantity = item_match.group('quantity').replace(' ', '')
    price = item_match.group('price').replace(' ', '')
    cost = item_match.group('cost').replace(' ', '')
    return ReceiptItem(name, quantity, price, cost)


def parse_matching_lidl_plus_discount_item(item_match):
    cost = item_match.group('discount_amount').replace(' ', '')
    return ReceiptItem('Lidl Plus rabat', None, None, cost)


def parse_matching_common_discount_item(item_match):
    cost = item_match.group('discount_amount').replace(' ', '')
    return ReceiptItem('standardowy rabat', None, None, cost)
