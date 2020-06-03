from decimal import Decimal


class Receipt:

    def __init__(self, source_file_name, date, items, total_amount):
        self.source_file_name = source_file_name
        self.date = date
        self.items = items
        self.total_amount = convert_string_to_decimal(total_amount)

    def replace_receipt_items(self, new_receipt_items):
        return Receipt(self.source_file_name, self.date, new_receipt_items, str(self.total_amount))

    def __str__(self):
        return f'Receipt[Date: {self.date}, Total Amount: {self.total_amount}, Items: {self.items}]'

    def __repr__(self):
        return self.__str__()


class ReceiptItem:
    def __init__(self, name, quantity, price, cost, valid=True):
        self.name = name
        self.quantity = convert_string_to_decimal(quantity, 3)
        self.price = convert_string_to_decimal(price)
        self.cost = convert_string_to_decimal(cost)
        self.valid = valid

    def mark_as_invalid(self):
        return ReceiptItem(self.name, str(self.quantity), str(self.price), str(self.cost), False)

    def __str__(self):
        return f'ReceiptItem[{self.name}: {self.quantity} * {self.price} = {self.cost}]'

    def __repr__(self):
        return self.__str__()


class OcrReceipt:
    def __init__(self, source_file_name, receipt_text):
        self.source_file_name = source_file_name
        self.receipt_text = receipt_text

    def __str__(self):
        return f'ReceiptOcr[{self.source_file_name}]'

    def __repr__(self):
        return self.__str__()


def convert_string_to_decimal(text, precision=2):
    if text:
        return round(Decimal(text.replace(',', '.')), precision)
