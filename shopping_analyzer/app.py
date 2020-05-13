import argparse
import glob
from shopping_analyzer.Receipt import Receipt

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import ntpath


def get_source_arg():
    parser = argparse.ArgumentParser(description='Dummy description')
    parser.add_argument("-s", "--source", help='provide source directory with receipts')
    args = parser.parse_args()
    print(f'Following source directory has been provided: {args.source}')
    return args.source


def run():
    source_directory = get_source_arg()

    img_receipt_paths = glob.glob(f'{source_directory}/image/*.jpg')
    print(img_receipt_paths)

    for receipt_img_path in img_receipt_paths:
        receipt_text = pytesseract.image_to_string(receipt_img_path, lang='pol')

        # Get bounding box estimates
        # print('### Get bounding box estimates ###')
        # print(pytesseract.image_to_boxes(receipt_img_path))
        # print()

        # Get verbose data including boxes, confidences, line and page numbers
        # print('### Get verbose data including boxes, confidences, line and page numbers ###')
        # print(pytesseract.image_to_data(receipt_img_path))
        # print()

        # Get information about orientation and script detection
        # print('### Get information about orientation and script detection ###')
        # print(pytesseract.image_to_osd(receipt_img_path))

        with open(f'{source_directory}/text/{ntpath.basename(receipt_img_path)}.txt', 'w') as txt_receipt_file:
            txt_receipt_file.write(receipt_text)

    # print('Hello World! Lets analyze some receipts!')
    # dummy_receipt = Receipt(704)
    # print(f'First dummy receipt is: {dummy_receipt}')
