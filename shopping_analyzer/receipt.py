class Receipt:

    def __init__(self, date, items, total_amount):
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
        self.quantity = quantity
        self.price = price
        self.cost = cost

    def __str__(self):
        return f'ReceiptItem[{self.name}: {self.quantity} * {self.price} = {self.cost}]'

    def __repr__(self):
        return self.__str__()
