class Receipt:

    def __init__(self, source_file_name, date, items, total_amount):
        self.source_file_name = source_file_name
        self.date = date
        self.items = items
        self.total_amount = total_amount

    def __str__(self):
        return f'Receipt[Date: {self.date}, Total Amount: {self.total_amount}, Items: {self.items}]'

    def __repr__(self):
        return self.__str__()


class ReceiptItem:
    def __init__(self, name, quantity, price, cost):
        self.name = name
        if quantity:
            self.quantity = float(ReceiptItem.replace_comma_with_dot(quantity))
        if price:
            self.price = float(ReceiptItem.replace_comma_with_dot(price))
        self.cost = float(ReceiptItem.replace_comma_with_dot(cost))

    @staticmethod
    def replace_comma_with_dot(text):
        return text.replace(',', '.')

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
