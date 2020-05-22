# TODO Are all below imports needed?
import glob

from shopping_analyzer.receipt_processor.receipt import OcrReceipt

try:
    from PIL import Image
except ImportError:
    import Image
import ntpath

import pytesseract


def ocr_receipts_in_directory(source_directory):
    # TODO Think about more optimal and clean creating this collection and returning it.
    # TODO Is there something like java Stream API in Python?
    # TODO Fix encoding. It is producing windows like?
    img_receipt_paths = glob.glob(f'{source_directory}/image/*.jpg')
    ocr_receipts = []
    for receipt_img_path in img_receipt_paths:
        # TODO Make tesseract read 0 instead of 8 when sometime 0 has a dash inside
        receipt_text = pytesseract.image_to_string(receipt_img_path, lang='pol')
        ocr_receipts.append(OcrReceipt(ntpath.basename(receipt_img_path), receipt_text))
    return ocr_receipts
