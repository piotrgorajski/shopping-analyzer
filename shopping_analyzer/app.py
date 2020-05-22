from shopping_analyzer.argument_parser import get_app_arguments
from shopping_analyzer.receipt_processor.receipt_processor import process_input_receipts
from shopping_analyzer.shopping_statistics.shopping_statistics import generate_statistics


def run():
    # read app arguments
    app_args = get_app_arguments()

    # ocr and process source files
    receipts = process_input_receipts(app_args.source, app_args.perform_ocr)

    # generate various statistics as csv files
    generate_statistics(receipts, app_args.source)
