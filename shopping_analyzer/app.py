from shopping_analyzer.argument_parser import get_source_argument
from shopping_analyzer.receipt_processor.receipt_processor import process_input_receipts
from shopping_analyzer.shopping_statistics.shopping_statistics import generate_statistics


def run():
    # get source parameter
    source_directory = get_source_argument()

    # ocr and process source files
    receipts = process_input_receipts(source_directory)

    # generate various statistics as csv files
    generate_statistics(receipts, source_directory)
