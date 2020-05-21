import glob

from shopping_analyzer.receipt_processor.receipt_ocr import ocr_receipts
from shopping_analyzer.receipt_processor.receipt_text_processor import process_text_receipts


def process_input_receipts(source_directory):
    # TODO Refactor source folder management and simplify arguments
    # list all input files under source
    img_receipt_paths = glob.glob(f'{source_directory}/image/*.jpg')
    text_receipts = ocr_receipts(source_directory, img_receipt_paths)
    return process_text_receipts(text_receipts)
