import os
import unittest
from datetime import date, timedelta

from gnucash2dash import gnucash

class TestBook(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Tests.gnucash')

    def test_open(self):
        book = gnucash.Book(self.path)

    def test_assets(self):
        book = gnucash.Book(self.path)
        self.assertIsNotNone(book.assets)

    def test_assets_balance_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(book.assets, end=date(2022, 12, 31))

        self.assertEqual(1105.46, balance)

    def test_assets_balance_begin_till_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(
            book.assets,
            begin=date(2023, 1, 1),
            end=date(2023, 12, 31))

        self.assertEqual(994.04, balance)

    def test_expenses(self):
        book = gnucash.Book(self.path)
        self.assertIsNotNone(book.expenses)

    def test_expenses_balance_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(book.expenses, end=date(2022, 12, 31))

        self.assertEqual(11996.54, balance)

    def test_expenses_balance_begin_till_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(
            book.expenses,
            begin=date(2023, 1, 1),
            end=date(2023, 12, 31))

        self.assertEqual(8427.96, balance)

    def test_liabilities(self):
        book = gnucash.Book(self.path)
        self.assertIsNotNone(book.liabilities)

    def test_liabilities_balance_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(book.liabilities, end=date(2022, 12, 31))

        self.assertEqual(-82.0, balance)

    def test_liabilities_balance_begin_till_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(
            book.liabilities,
            begin=date(2023, 1, 1),
            end=date(2023, 12, 31))

        self.assertEqual(-102.0, balance)

    def test_income(self):
        book = gnucash.Book(self.path)
        self.assertIsNotNone(book.income)

    def test_income_balance_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(book.income, end=date(2022, 12, 31))

        self.assertEqual(-13020.0, balance)

    def test_income_balance_begin_till_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(
            book.income,
            begin=date(2023, 1, 1),
            end=date(2023, 12, 31))

        self.assertEqual(-9320.0, balance)

    def test_equity(self):
        book = gnucash.Book(self.path)
        self.assertIsNotNone(book.equity)

    def test_equity_balance_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(book.equity, end=date(2022, 12, 31))

        self.assertEqual(0.0, balance)

    def test_equity_balance_begin_till_end(self):
        book = gnucash.Book(self.path)
        balance = book.get_balance(
            book.equity,
            begin=date(2023, 1, 1),
            end=date(2023, 12, 31))

        self.assertEqual(0.0, balance)

    def test_asset_interval_balance_one_day(self):
        book = gnucash.Book(self.path)
        interval_balances = book.get_interval_balances(
            book.assets,
            interval=gnucash.DateInterval.DAY,
            begin=date(2024, 5, 2),
            end=date(2024, 5, 2))

        self.assertEqual(1, len(interval_balances))

        end_date, balance = interval_balances[0]
        self.assertEqual(date(2024, 5, 2), end_date)
        self.assertEqual(-50.0, balance)

    def test_expenses_interval_balance_two_months(self):
        book = gnucash.Book(self.path)
        interval_balances = book.get_interval_balances(
            book.expenses,
            interval=gnucash.DateInterval.MONTH,
            begin=date(2024, 1, 1),
            end=date(2024, 2, 28))

        self.assertEqual(2, len(interval_balances))

        month_one_end_date, month_one_balance = interval_balances[0]
        self.assertEqual(date(2024, 1, 31), month_one_end_date)
        self.assertEqual(956.0, month_one_balance)

        month_two_end_date, month_two_balance = interval_balances[1]
        self.assertEqual(date(2024, 2, 29), month_two_end_date)
        self.assertEqual(576.0, month_two_balance)

    def test_income_interval_balance_five_years(self):
        book = gnucash.Book(self.path)
        interval_balances = book.get_interval_balances(
            book.income,
            interval=gnucash.DateInterval.YEAR,
            begin=date(2025, 1, 1),
            end=date(2029, 12, 31))

        self.assertEqual(5, len(interval_balances))

        year_one_end_date, year_one_balance = interval_balances[0]
        self.assertEqual(date(2025, 12, 31), year_one_end_date)
        self.assertEqual(-9320.0, year_one_balance)

        year_three_end_date, year_three_balance = interval_balances[2]
        self.assertEqual(date(2027, 12, 31), year_three_end_date)
        self.assertEqual(-9430.0, year_three_balance)

        year_five_end_date, year_five_balance = interval_balances[4]
        self.assertEqual(date(2029, 12, 31), year_five_end_date)
        self.assertEqual(-9320.0, year_five_balance)

if __name__ == '__main__':
    unittest.main()