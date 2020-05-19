import glob
import re

from shopping_analyzer.argument_parser import get_source_argument
from shopping_analyzer.csv_export import write_data_to_csv
from shopping_analyzer.receipt import ReceiptItem, Receipt, ReceiptItemSummary
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

    # TODO Make below code more stream like. Join all lists and use reduce?
    receipt_items_summary = {}
    for receipt in receipts:
        for item in receipt.items:
            if item.name in receipt_items_summary.keys():
                receipt_items_summary[item.name] = receipt_items_summary.get(item.name).add_cost(item.cost)
            else:
                receipt_items_summary[item.name] = ReceiptItemSummary(item.name, item.cost)

    # TODO Extract below to some new (statistics) module
    statistic0 = sorted(map(lambda x: [x.name], receipt_items_summary.values()))
    # print(statistic0)
    write_data_to_csv(source_directory, 'statistic0.csv', statistic0)

    statistic1a = sorted(receipt_items_summary.values(), key=lambda x: x.cost, reverse=True)
    # print(statistic1a)
    write_data_to_csv(source_directory, 'statistic1a.csv', map(lambda x: [x.name, x.cost], statistic1a))

    # TODO Analysis:
    #  0) List all distinct items to validate and prepare categories for each (consider using str similarity algorithms)
    #  1a) All distinct items with total cost across all time
    #  1b) All distinct items with total cost grouped by month
    #  2a) [categories are ready] All time cost for all categories
    #  2b) [categories are ready] Per month cost for all categories

    # TODO Add loading config file with items mapped to categories (json? yaml?)
    # TODO Perform statistical operations to get interesting data
    # TODO Output results as files (csv?)
    # TODO Add unit tests. What about e2e?
    # TODO Add exception handling
    # TODO Perform general refactor in each module

    # TODO investigate GitHub build pipeline. How Python project are handled in CI/CD?
    # TODO What is the Python way for "java -jar X"? How do you build such self contained app?
