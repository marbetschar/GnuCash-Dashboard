from datetime import datetime
from dateutil.relativedelta import relativedelta

import calendar
import pandas
import numpy

from gnucash2dash import gnucash, utils

def predict_date_for_net_worth(book, net_worth):
    historical = historical_net_worth(book, n_months=6)
    diff_sign = utils.sign(net_worth - current_net_worth(book))

    a, b, x = utils.linear_regression_coefficients([hist[1] for hist in historical])

    if a == 0 or a > 0 and diff_sign < 0 or a < 0 and diff_sign > 0:
        return numpy.inf

    else:
        y = numpy.ceil((net_worth - b) / a)

        return (utils.now() + relativedelta(months=y)).date()

def current_net_worth(book):
    """
    net_worth = assets + liabilities
        absolute: red below 0, yellow below 50'000, green otherwise
    """
    net_worth = 0

    if not book.assets is None:
        net_worth += book.get_balance(book.assets)

    if not book.liabilities is None:
        net_worth += book.get_balance(book.liabilities)

    return net_worth

def historical_net_worth(book, n_months=6):
  end = utils.now()
  begin = end - relativedelta(months=n_months)

  assets = book.get_interval_balances(book.assets, interval=gnucash.DateInterval.MONTH, begin=begin, end=end)
  liabilities = book.get_interval_balances(book.liabilities, interval=gnucash.DateInterval.MONTH, begin=begin, end=end)

  hist_net_worth = []
  for i in range(0, n_months):
    hist_net_worth.append((assets[i][0], assets[i][1] + liabilities[i][1]))

  return hist_net_worth

def net_worth_trend(book, n_months=6):
    """
    net_worth_trend = monthly_assets + monthly_liabilities
        absolute: line chart, grouped per month, show the last n_months
    """
    hist_net_worth = historical_net_worth(book, n_months=n_months)

    a, b, x = utils.linear_regression_coefficients([hist[1] for hist in hist_net_worth])
    for i in range(0, n_months):
        hist_net_worth[i] = (hist_net_worth[i][0], a*x[i] + b)

    return pandas.DataFrame(hist_net_worth, columns=['date', 'net_worth_diff'])

def runway(book, n_days=180):
  """
  If my income stopped right now, how long would I be able to survive?

      runway = assets / average_daily_expense

  in days: red below 60, yellow below 90, and green otherwise
  """
  end = utils.now()
  begin = end - relativedelta(days=n_days)

  average_daily_expense = numpy.mean([balance[1] for balance in book.get_interval_balances(book.expenses, interval=gnucash.DateInterval.DAY, begin=begin, end=end)])
  assets = book.get_balance(book.assets)

  return assets / average_daily_expense

def income_vs_expense(book, n_months=6):
    """
    income vs expense
       absolute: bar charts, grouped per month, show the last n_months
    """
    end = utils.now()
    begin = end - relativedelta(months=n_months)

    income = book.get_interval_balances(book.income, interval=gnucash.DateInterval.MONTH, begin=begin, end=end)
    expenses = book.get_interval_balances(book.expenses, interval=gnucash.DateInterval.MONTH, begin=begin, end=end)

    data = []
    for i in range(0, n_months):
        data.append((income[i][0], abs(income[i][1]), abs(expenses[i][1])))

    return pandas.DataFrame(data, columns=['date', 'income', 'expenses'])

# - net_worth_goal_date = extrapolate_linear(net_worth_trend_since_start, until_net_worth=goal)
#   - as date, small line chart below, huge end-date above
#   - Trend seit Start der Erfassung
#   - Forecasting: Datum Zielbetrag basierend auf Extrapolation des Trends
# - payback_rate = (cur_month_net_income - cur_month_expenses) / (prev_month_liabilities - cur_month_liabilities)
#   - as percentage: red below 50, yellow below 75, green otherwise
#   - Wieviel des verfügbaren Gelds habe ich tatsächlich pro Monat in Rückzahlung investiert?
# - runway = assets / average_daily_expense
#   - in days: red below 60, yellow below 90, and green otherwise
#   - if my income stopped right now, how long would I be able to survive?