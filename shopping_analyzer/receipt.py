class Receipt:

    def __init__(self, amount):
        self.amount = amount

    def __str__(self):
        return f'Receipt[{self.amount}]'
