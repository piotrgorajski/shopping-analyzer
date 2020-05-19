# TODO Are all below imports needed?
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import ntpath


def ocr_receipts(source_directory, img_receipt_paths):
    # TODO Think about more optimal and clean creating this collection and returning it.
    # TODO Is there something like java Stream API in Python?
    # TODO Fix encoding. It is producing windows like?
    text_receipts = []
    for receipt_img_path in img_receipt_paths:
        # TODO Make tesseract read 0 instead of 8 when sometime 0 has a dash inside
        receipt_text = pytesseract.image_to_string(receipt_img_path, lang='pol')
        text_receipts.append(receipt_text)

        # TODO Remove this fake data files structure. Read source argument. You may create some tmp dir for text files
        # TODO For history reruns maybe read saved text files instead of ocr all again
        with open(f'{source_directory}/text/{ntpath.basename(receipt_img_path)}.txt', 'w') as txt_receipt_file:
            txt_receipt_file.write(receipt_text)

    return text_receipts
