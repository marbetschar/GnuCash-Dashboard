import os
import config
import webbrowser

from gnucash2dash import dash

app = dash.app(__name__, os.environ.get('GNUCASH2DASH_FILE', config.gnucash_file))

if __name__ == '__main__':
    host = os.environ.get('GNUCASH2DASH_HOST', config.host)
    port = os.environ.get('GNUCASH2DASH_PORT', config.port)
    open_browser = os.environ.get('GNUCASH2DASH_OPEN_BROWSER', config.open_browser)

    if open_browser == '1' or open_browser is True:
        webbrowser.open_new("http://{}:{}".format(host, port))

    app.run_server(debug=False, host=host, port=port)