import argparse


def get_app_arguments():
    parser = argparse.ArgumentParser(description='Welcome in Shopping Analyzer application')
    parser.add_argument("-s", "--source", help='provide source directory with receipts')
    parser.add_argument("-o", "--perform_ocr", help='provide source directory with receipts', action='store_true',
                        default=False)
    args = parser.parse_args()
    print(f'Provided app arguments: {args}')
    return args
