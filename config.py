#
# gnucash_file     (env = GNUCASH2DASH_FILE)
#
# Required. Path to the GnuCash file which should be used to render
# the stats in the dashboard. The path can be absolute or relative
# to the `app.py` file:
gnucash_file = 'Demo.gnucash'

#
# host             (env = GNUCASH2DASH_HOST)
# Required. Host which should be used to render the dashboard on.
# Defaults to localhost ('127.0.0.1')
host = '127.0.0.1'

#
# port             (GNUCASH2DASH_PORT)
# Required. Host which should be used to render the dashboard on.
# Defaults to '8050'.
port = '8050'

#
# now              (env = GNUCASH2DASH_NOW)
# Optional. An iso8601 formatted date string which should be used
# as default for date calculations for the dashboard. Set to None
# if you want to use the current system date.
now = None  # or '2026-06-26'

#
# open_browser     (env = GNUCASH2DASH_OPEN_BROWSER)
# Optional. If the default browser of the current system should be opened
# automatically after the dashboard started. Enabled if the value
# is set to True or '1'.
open_browser = True

#
# net_worth_trend_n_months    (env = GNUCASH2DASH_NET_WORTH_TREND_N_MONTHS)
# Required. How many of the last couple of months should be used
# to calculate the linear regression for the change in net worth?
net_worth_trend_n_months = 6

#
# net_worth_predict_goal      (env = GNUCASH2DASH_NET_WORTH_PREDICT_GOAL)
# Required. The net worth goal which is used to predict the date at which
# this goal will be achieved using the current net worth trend.
net_worth_predict_goal = 100_000

#
# income_expense_n_months     (env = GNUCASH2DASH_INCOME_EXPENSE_N_MONTHS)
# Required. How many of the last couple of months should be used
# to render the income vs expense bar charts?
income_expense_n_months = 6

#
# runway_n_days               (env = GNUCASH2DASH_RUNWAY_N_DAYS)
# Required. How many days backwards should be measured for the
# average daily expense which in turn is used to calculate the
# expected runway?
runway_n_days = 180