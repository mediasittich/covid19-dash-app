
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table

from app import app
from src.features import covid_data

print(covid_data.head())

map_description = '''
Some useful info
'''

layout = html.Div([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.H3('Map'),
            html.P(map_description),
        ]),
    ]),
    # World-wide Map and Data



    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    html.Br(),

])


@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
