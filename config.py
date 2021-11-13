#
# gnucash_file    (GNUCASH2DASH_FILE)
#
# Required. Path to the GnuCash file which should be used to render
# the stats in the dashboard. The path can be absolute or relative
# to the `app.py` file:
gnucash_file = 'Demo.gnucash'

#
# host             (GNUCASH2DASH_HOST)
# Required. Host which should be used to render the dashboard on.
# Defaults to localhost ('127.0.0.1')
host = '127.0.0.1'

#
# port             (GNUCASH2DASH_PORT)
# Required. Host which should be used to render the dashboard on.
# Defaults to '8050'.
port = '8050'

#
# now              (GNUCASH2DASH_NOW)
# Optional. An iso8601 formatted date string which should be used
# as default for date calculations for the dashboard. Set to None
# if you want to use the current system date.
now = '2026-06-26'  # or None

#
# open_browser     (GNUCASH2DASH_OPEN_BROWSER)
# Optional. If the default browser of the current system should be opened
# automatically after the dashboard started. Enabled if the value
# is set to True or '1'.
open_browser = True
