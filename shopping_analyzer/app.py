import glob
import re

from shopping_analyzer.argument_parser import get_source_argument
from shopping_analyzer.receipt_ocr import ocr_receipts

# TODO Resolve issue with GitHub auth and commit/push current state!
def run():
    source_directory = get_source_argument()

    img_receipt_paths = glob.glob(f'{source_directory}/image/*.jpg')
    print(img_receipt_paths)

    text_receipts = ocr_receipts(source_directory, img_receipt_paths)

    date = re.findall(r".*www\.lidl\.pl\s*(\d{4}-\d{2}-\d{2}).*", text_receipts[0])
    items = re.findall(r".*www\.lidl\.pl\s*\d{4}-\d{2}-\d{2}(.*)PTU A.*", text_receipts[0], re.DOTALL)
    total = re.findall(r".*RAZEM PLN\s+(\d+,\d{2}).*", text_receipts[0])
    print(date)
    print(items)
    print(items[0].splitlines())
    # TODO Add filtering items (blank lines, lidl discounts, etc., use pattern and throw out non matching items)
    # TODO Perform validation on items like if the a * b = c
    # TODO Perform validation on items sum vs total amount
    # TODO Log as error any issues in the data
    # TODO Make tesseract read 0 instead of 8 when sometime 0 has a dash inside
    # TODO Save all valid items in a class oriented structure ready to perform statistical operations
    # TODO Create nested structure in Receipt for Item (name, quantity, price, item total)
    # TODO Move all above as separate module (receipt_processor?)

    # TODO Perform statistical operations to get interesting data
    # TODO Output results as files (csv?)
    # TODO Add unit tests. What about e2e?
    # TODO Add exception handling
    # TODO Perform general refactor in each module

    # TODO investigate GitHub build pipeline. How Python project are handled in CI/CD?
    # TODO What is the Python way for "java -jar X"? How do you build such self contained app?
    print(total)

    # print('Hello World! Lets analyze some receipts!')
    # dummy_receipt = Receipt(704)
    # print(f'First dummy receipt is: {dummy_receipt}')


def process_text_receipts(text_receipts):
    pass
