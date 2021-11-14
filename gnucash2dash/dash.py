from dash import Dash
from dash import html
from dash import dcc

import plotly.io as pio

from dash.dependencies import Input, Output
from gnucash2dash import gnucash, widgets

def app(name, gnucash_file):
    # Set default template for plotly:
    pio.templates.default = 'plotly_dark'

    app = Dash(__name__, title='GnuCash Dashboard')
    book = gnucash.Book(gnucash_file)

    app.layout = html.Div(style={ 'display': 'flex', 'height': '100vh', 'flex-direction': 'column', 'justify-content': 'space-between' }, children=[
        html.Div(style={ 'flex': 1, 'display': 'flex', 'flex-drection': 'column', 'justify-content': 'space-between' },
        children=[
            widgets.net_worth(book),
            widgets.net_worth_trend(book),
            widgets.net_worth_prediction(book)
        ]),
        html.Div(style={ 'flex': 1, 'display': 'flex', 'flex-drection': 'column', 'justify-content': 'space-between' },
        children=[
            widgets.income_vs_expense(book),
            widgets.runway(book)
        ])
    ])

    return app
