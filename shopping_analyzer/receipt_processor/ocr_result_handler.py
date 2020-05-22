import glob


def save_ocr_text_in_files(ocr_receipts, source_directory):
    for ocr_receipt in ocr_receipts:
        # TODO Remove this fake data files structure. Read source argument. You may create some tmp dir for text files
        # TODO For history reruns maybe read saved text files instead of ocr all again
        with open(f'{source_directory}/text/{ocr_receipt.source_file_name}.txt', 'w') as text_receipt_file:
            text_receipt_file.write(ocr_receipt.receipt_text)


def read_ocr_text_receipts(source_directory):
    text_receipts = []
    text_receipt_paths = glob.glob(f'{source_directory}/text/*.txt')
    for text_receipt_path in text_receipt_paths:
        with open(text_receipt_path, 'r') as text_receipt_file:
            text_receipt_lines = text_receipt_file.readlines()
            text_receipts.append('\n'.join(text_receipt_lines))
    return text_receipts
