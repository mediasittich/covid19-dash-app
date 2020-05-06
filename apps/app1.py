import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

from app import app
from src.get_data import df

# print(get_data.df.head())

layout = html.Div([
    html.H3('Map'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    html.Div([
        dash_table.DataTable(
            id='covid-cases-table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=10,  # for pagination with 10 rows per page
            style_cell={'textAlign': 'left'},
            #fixed_rows={'headers': True},
            #style_table={'height': 400},
        )
    ])

])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
