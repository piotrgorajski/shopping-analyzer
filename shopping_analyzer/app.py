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

    # TODO Add loading config file with items mapped to categories (json? yaml?)
    # TODO Add unit tests. What about e2e?
    # TODO Add exception handling
    # TODO Perform general refactor in each module

    # TODO investigate GitHub build pipeline. How Python project are handled in CI/CD?
    # TODO What is the Python way for "java -jar X"? How do you build such self contained app?
