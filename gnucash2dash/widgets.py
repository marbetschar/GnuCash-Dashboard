from dash import dcc
from dash import html
from dash import dash_table
import dash_daq as daq

import locale
import numpy
import plotly.express as px
import plotly.graph_objects as go

from datetime import date
from gnucash2dash import metrics

def net_worth(book):
    net_worth = metrics.current_net_worth(book)
    currency = book.get_currency(book.assets)

    if currency is None:
        currency = ''

    classification = 'medium'
    if net_worth > 0:
        classification = 'good'
    elif net_worth < 0:
        classification = 'bad'

    return html.Div(className='widget kpi ' + classification, children=[
        html.Caption(className='label', children=['net worth absolute'], style={ 'whiteSpace': 'nowrap' }),
        html.H1(locale.format_string(currency + ' %.0f', net_worth, True))
        ])

def net_worth_trend(book, n_months):
    df = metrics.net_worth_trend(book, n_months=n_months)
    fig = px.line(df, x='date', y='net_worth_diff', labels={
        'date': '',
        'net_worth_diff': ''
    })
    fig.update_layout(title='net worth trend')

    classification_color = '#ffc000'  # medium
    if df.values[0][1] < df.values[len(df.values) - 1][1]:
        classification_color = '#0bd44d'  # good
    elif df.values[0][1] > df.values[len(df.values) - 1][1]:
        classification_color = '#ff1300'  # bad

    fig.update_traces(line_color=classification_color)

    return dcc.Graph(className='widget', figure=fig)

def net_worth_prediction(book, goal):
    predicted_date = metrics.predict_date_for_net_worth(book, net_worth=goal)

    predicted_date_formatted = '∞'
    if not predicted_date is numpy.inf:
        predicted_date_formatted = predicted_date.strftime("%b %Y")

    currency = book.get_currency(book.assets)
    if currency is None:
        currency = ''

    today_date = date.today()
    classification = 'medium'
    if predicted_date is numpy.inf or predicted_date > date(today_date.year + 20, today_date.month, today_date.day):
        classification = 'bad'
    elif predicted_date < date(today_date.year + 10, today_date.month, today_date.day):
        classification = 'good'

    return html.Div(className='widget kpi ' + classification, children=[
        html.Caption(className='label', children=['net worth prediction'], style={ 'whiteSpace': 'nowrap' }),
        html.H1(predicted_date_formatted),
        html.Span(locale.format_string(currency + ' %.0f', goal, True))
        ])

def income_vs_expense(book, n_months):
    df = metrics.income_vs_expense(book, n_months=n_months)
    fig = px.bar(df, x='date', y=['income', 'expenses'], barmode='overlay', opacity=1, labels={
        'date': '',
        'value': '',
        'variable': ''
    })
    fig.update_layout(title='income vs expenses')

    return dcc.Graph(className='widget', figure=fig)

def runway(book, n_days):
    runway_in_days = numpy.floor(metrics.runway(book, n_days=n_days))

    return html.Div(className='widget kpi gauge', children=[
        html.Caption(className='label', children=['runway'], style={ 'whiteSpace': 'nowrap' }),
        daq.Gauge(
        color={"gradient":True,"ranges":{"red":[0,60],"yellow":[60,90],"green":[90,120]}},
        value=runway_in_days,
        min=0,
        max=120,
        scale={ 'start': 0, 'interval': 30, 'labelInterval': 1 }),
        html.Span(locale.format_string('%.0f days', runway_in_days))
    ])