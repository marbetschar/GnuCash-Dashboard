import calendar
import pandas
import numpy
import plotly.graph_objects as go

from dash import dcc
from dash import html
from dash import dash_table
from dash.dash_table.Format import Format, Symbol, Scheme
from datetime import datetime
from gnucash2dash import gnucash, utils

def snowball(book, account, monthly_budget=1000):
    """
    Calculate monthly payments for the provided account in the book using the debt snowball algorithm.
    """
    today = utils.now().date()

    debt_leafs = book.get_leafs(account)
    debt_sign = utils.sign(book.get_balance(account, end=today))

    index = [today]
    data = {}

    for leaf_account, leaf_path in debt_leafs:
        leaf_path.pop(0)
        leaf_balance = book.get_balance(leaf_account, end=today)
        leaf_sign = utils.sign(leaf_balance)

        # Ignore if leaf is already payed:
        if leaf_balance == 0 or leaf_sign != debt_sign:
            continue

        data[str.join(':', leaf_path)] = [-1 * abs(leaf_balance)]

    df = pandas.DataFrame(data=data, index=index)

    # Sort columns by value ascending, so we get the lowest amount in the upper left corner:
    df_sorted = pandas.DataFrame(data=df.values[0], index=df.columns, columns=df.index)
    df_sorted = df_sorted.sort_values(by=df_sorted.columns[0], ascending=False)

    # Reformat table, so we get dates as index:
    df = pandas.DataFrame(data=df_sorted.values.T, columns=df_sorted.index, index=df_sorted.columns)

    # loop through the columns and calculate monthly payments:
    debt_month_datetime = pandas.to_datetime(df.index[-1])
    debt_month_days = calendar.monthrange(debt_month_datetime.year, debt_month_datetime.month)[1]

    current_month_index = debt_month_datetime + pandas.Timedelta(debt_month_days, unit='days')
    current_month_budget = monthly_budget
    for column in df.columns:
        while df[column].sum() < 0:
            if current_month_budget > 0:
                transaction_budget = numpy.abs(df[column].sum())
                if transaction_budget > current_month_budget:
                    transaction_budget = current_month_budget

                df.at[current_month_index, column] = transaction_budget
                current_month_budget -= transaction_budget

            else:
                previous_month_datetime = pandas.to_datetime(df.index[-1])
                previous_month_days = calendar.monthrange(previous_month_datetime.year, previous_month_datetime.month)[1]

                current_month_index = previous_month_datetime + pandas.Timedelta(previous_month_days, unit='days')
                current_month_budget = monthly_budget

    return df.fillna(0)

def snowball_widget(book, account, monthly_budget=10):
    df = snowball(book, account, monthly_budget=monthly_budget)

    fig = go.Figure()
    for column in df.columns:
        fig.add_trace(go.Scatter(name=column, x=df.index, y=df[column].cumsum(), fill='tonexty', mode='none'))
    fig.update_layout(title='debt snowball')

    money_format = Format(precision=2, scheme=Scheme.fixed)

    # Move index into a new, regular column, format the date and copy the same column
    # to the end of the DataFrame - then display the whole DataFrame in the DataTable below:
    df = df.reset_index()
    df['index'] = df['index'].dt.strftime('%d.%m.%Y')
    df = df.rename(columns={ 'index': '' })

    table = dash_table.DataTable(
        columns=[{
            'name': i,
            'id': i,
            'type': 'numeric',
            'format': money_format
        } for i in df.columns],
        data=df.to_dict('records'))

    return html.Div(className='widget', children=[
        dcc.Graph(figure=fig),
        table
    ])