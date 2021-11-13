from enum import Enum
from datetime import date, datetime, timedelta
import calendar

from gnucash import (
    Session,
    GncCommodity,
    ACCT_TYPE_ASSET,
    ACCT_TYPE_EXPENSE,
    ACCT_TYPE_INCOME,
    ACCT_TYPE_LIABILITY,
    ACCT_TYPE_EQUITY
)

class Mode(Enum):
    HEAD = 1
    TAIL = 2

class DateInterval(Enum):
    DAY = 1
    MONTH = 30
    YEAR = 365

class Book:

    def __init__(self, path):
        self.session = Session("xml://%s" % path, ignore_lock=True, force_new=False)

        self.assets = None
        self.expenses = None
        self.income = None
        self.liabilities = None
        self.equity = None

        book = self.session.get_book()
        root = book.get_root_account()

        children = root.get_children()
        for child in children:
            account_type = child.GetType()

            if account_type is ACCT_TYPE_ASSET:
                self.assets = child

            elif account_type is ACCT_TYPE_EXPENSE:
                self.expenses = child

            elif account_type is ACCT_TYPE_INCOME:
                self.income = child

            elif account_type is ACCT_TYPE_LIABILITY:
                self.liabilities = child

            elif account_type is ACCT_TYPE_EQUITY:
                self.equity = child

    def get_currency(self, account):
        commodity = account.GetCommodity()

        if not commodity is None and commodity.is_currency():
            return commodity.get_nice_symbol()

        return None

    def get_balance(self, account, begin=None, end=date.today()):
        if account is None:
            return None

        end_datetime = datetime.combine(end, datetime.max.time())

        try:
            balance = account.GetBalanceAsOfDate(end_datetime).to_double()
        except:
            return None

        if not begin is None:
            begin_datetime = datetime.combine(begin, datetime.min.time())
            try:
                balance -= account.GetBalanceAsOfDate(begin_datetime).to_double()
            except:
                pass

        children = account.get_children()
        for child in children:
            try:
                balance += self.get_balance(child, begin=begin, end=end)
            except:
                pass

        return balance

    def get_interval_balances(self, account, interval=DateInterval.DAY, begin=None, end=date.today(), opening_balance=None):
        if account is None:
            return None

        balances = []
        interval_begin = None
        interval_end = None

        if interval is DateInterval.DAY:
            interval_begin = datetime.combine(end, datetime.min.time())
            interval_end = datetime.combine(end, datetime.max.time())

        elif interval is DateInterval.MONTH:
            days_in_month = calendar.monthrange(end.year, end.month)[1]

            interval_begin = datetime.combine(date(end.year, end.month, 1), datetime.min.time())
            interval_end = datetime.combine(date(end.year, end.month, days_in_month), datetime.max.time())

        elif interval is DateInterval.YEAR:
            interval_begin = datetime.combine(date(end.year, 1, 1), datetime.min.time())
            interval_end = datetime.combine(date(end.year, 12, 31), datetime.max.time())

        else:
            raise ValueError('DateInterval provided is unknown')

        interval_balance = self.get_balance(account, begin=interval_begin, end=interval_end)

        begin_datetime = None
        if not begin is None:
            begin_datetime = datetime.combine(begin, datetime.min.time())

        # If we don't have any balance or if the current interval balance
        # is the same as the one calculated before and we don't have a start
        # date, we assume we don't have any more historical data and stop processing:
        if interval_balance is None or begin_datetime is None and interval_balance == opening_balance:
            return balances

        # Prepend current interval balance
        balances.insert(0, (interval_end.date(), interval_balance))

        if begin_datetime is None or interval_begin > begin_datetime:
            # Prepend balances of previous interval
            balances[:0] = self.get_interval_balances(
                account,
                begin=begin,
                end=interval_begin - timedelta(seconds=1),
                interval=interval,
                opening_balance=interval_balance
            )

        return balances

    def get_leafs(self, account, path=[]):
      leafs = []

      if not account is None:
        path.append(account.name)

        if account.n_children() > 0:
          children = account.get_children()
          for child in children:
            leafs.extend(self.get_leafs(child, list(path)))

        else:
          leafs.append((account, list(path)))

      return leafs
