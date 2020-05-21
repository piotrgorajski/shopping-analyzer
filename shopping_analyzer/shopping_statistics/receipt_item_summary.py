# TODO Figure out better name for that class
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
