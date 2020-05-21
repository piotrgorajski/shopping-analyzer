from shopping_analyzer.shopping_statistics.csv_export import write_data_to_csv
from shopping_analyzer.shopping_statistics.receipt_item_summary import ReceiptItemSummary


# TODO Analysis:
#  0) [DONE] All distinct items to validate and prepare categories for each (consider using str similarity algorithms)
#  1a) [DONE] All distinct items with total cost across all time
#  1b) All distinct items with total cost grouped by month
#  2a) [categories are ready] All time cost for all categories
#  2b) [categories are ready] Per month cost for all categories


class StatisticsGenerator:

    def __init__(self, receipts, source_directory):
        self.receipts = receipts
        self.source_directory = source_directory

    def generate_statistic_0(self, receipt_items_summary):
        """List all distinct items to validate and prepare categories for each. Sorted by name (asc)"""
        statistic0 = sorted(map(lambda x: [x.name], receipt_items_summary.values()))
        write_data_to_csv(self.source_directory, 'statistic0.csv', statistic0)

    def generate_statistic_1a(self, receipt_items_summary):
        """List all distinct items with total cost across all time. Sorted by cost (desc)"""
        statistic1a = sorted(receipt_items_summary.values(), key=lambda x: x.cost, reverse=True)
        # TODO Convert cost to use comma instead of dot?
        write_data_to_csv(self.source_directory, 'statistic1a.csv', map(lambda x: [x.name, x.cost], statistic1a))

    def convert_to_receipt_summary(self):
        # TODO Make below code more stream like. Join all lists and use reduce?
        receipt_items_summary = {}
        for receipt in self.receipts:
            for item in receipt.items:
                if item.name in receipt_items_summary.keys():
                    receipt_items_summary[item.name] = receipt_items_summary.get(item.name).add_cost(item.cost)
                else:
                    receipt_items_summary[item.name] = ReceiptItemSummary(item.name, item.cost)
        return receipt_items_summary


def generate_statistics(receipts, source_directory):
    statistics_generator = StatisticsGenerator(receipts, source_directory)
    receipt_items_summary = statistics_generator.convert_to_receipt_summary()
    statistics_generator.generate_statistic_0(receipt_items_summary)
    statistics_generator.generate_statistic_1a(receipt_items_summary)
