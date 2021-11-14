import os
import config

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
            widgets.net_worth_trend(book, n_months=int(os.environ.get('GNUCASH2DASH_NET_WORTH_TREND_N_MONTHS', config.net_worth_trend_n_months))),
            widgets.net_worth_prediction(book, goal=int(os.environ.get('GNUCASH2DASH_NET_WORTH_PREDICT_GOAL', config.net_worth_predict_goal)))
        ]),
        html.Div(style={ 'flex': 1, 'display': 'flex', 'flex-drection': 'column', 'justify-content': 'space-between' },
        children=[
            widgets.income_vs_expense(book, n_months=int(os.environ.get('GNUCASH2DASH_INCOME_EXPENSE_N_MONTHS', config.income_expense_n_months))),
            widgets.runway(book, n_days=int(os.environ.get('GNUCASH2DASH_RUNWAY_N_DAYS', config.runway_n_days)))
        ])
    ])

    return app
