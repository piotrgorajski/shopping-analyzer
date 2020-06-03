import logging

from shopping_analyzer.argument_parser import get_app_arguments
from shopping_analyzer.receipt_processor.receipt_processor import process_input_receipts
from shopping_analyzer.receipt_processor.receipt_validator import validate_receipts
from shopping_analyzer.shopping_statistics.shopping_statistics import generate_statistics


def run():
    # set up logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s %(asctime)s %(message)s')
    logging.info('Application Start')

    # read app arguments
    app_args = get_app_arguments()

    # ocr and process source files
    receipts = process_input_receipts(app_args.source, app_args.perform_ocr)
    logging.info(f'Processing {len(receipts)} receipts')

    # validate receipt items data
    fixed_receipts = validate_receipts(receipts)

    # generate various statistics as csv files
    generate_statistics(fixed_receipts, app_args.source)

    logging.info('Application End')
