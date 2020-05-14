import argparse


def get_source_argument():
    parser = argparse.ArgumentParser(description='Dummy description')
    parser.add_argument("-s", "--source", help='provide source directory with receipts')
    args = parser.parse_args()
    print(f'Following source directory has been provided: {args.source}')
    return args.source
