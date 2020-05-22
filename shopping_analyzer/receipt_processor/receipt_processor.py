from shopping_analyzer.receipt_processor.ocr_result_handler import save_ocr_text_in_files, read_ocr_text_receipts
from shopping_analyzer.receipt_processor.receipt_ocr import ocr_receipts_in_directory
from shopping_analyzer.receipt_processor.receipt_text_processor import process_text_receipts


def process_input_receipts(source_directory, perform_ocr):
    if perform_ocr:
        ocr_receipts = ocr_receipts_in_directory(source_directory)
        save_ocr_text_in_files(ocr_receipts, source_directory)
    text_receipts = read_ocr_text_receipts(source_directory)
    return process_text_receipts(text_receipts)
