import glob
import re

from shopping_analyzer.argument_parser import get_source_argument
from shopping_analyzer.receipt import ReceiptItem, Receipt
from shopping_analyzer.receipt_ocr import ocr_receipts
from shopping_analyzer.receipt_processor import process_text_receipts


def run():
    # get source parameter
    source_directory = get_source_argument()

    # list all input files under source
    img_receipt_paths = glob.glob(f'{source_directory}/image/*.jpg')

    # ocr source files
    text_receipts = ocr_receipts(source_directory, img_receipt_paths)

    # process raw ocr source files text
    receipts = process_text_receipts(text_receipts)
    print(receipts)

    # TODO Perform statistical operations to get interesting data
    # TODO Output results as files (csv?)
    # TODO Add unit tests. What about e2e?
    # TODO Add exception handling
    # TODO Perform general refactor in each module

    # TODO investigate GitHub build pipeline. How Python project are handled in CI/CD?
    # TODO What is the Python way for "java -jar X"? How do you build such self contained app?

    # print('Hello World! Lets analyze some receipts!')
    # dummy_receipt = Receipt(704)
    # print(f'First dummy receipt is: {dummy_receipt}')
