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
        self.quantity = float(ReceiptItem.replace_comma_with_dot(quantity))
        self.price = float(ReceiptItem.replace_comma_with_dot(price))
        self.cost = float(ReceiptItem.replace_comma_with_dot(cost))

    @staticmethod
    def replace_comma_with_dot(text):
        return text.replace(',', '.')

    def __str__(self):
        return f'ReceiptItem[{self.name}: {self.quantity} * {self.price} = {self.cost}]'

    def __repr__(self):
        return self.__str__()


# Figure out better name na place for that class (statistics module?)
class ReceiptItemSummary:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost

    def add_cost(self, new_cost):
        return ReceiptItemSummary(self.name, self.cost + new_cost)

    def __str__(self):
        return f'ReceiptItemSummary[{self.name}: {self.cost}]'

    def __repr__(self):
        return self.__str__()
