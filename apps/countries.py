import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from app import app
from src.features import covid_data_countries, case_types

app_description = '''
Here you can select a country and get infos for it.
'''
countries = covid_data_countries['DisplayName'].unique()

# Dropdown Country Selector
dropdown = dbc.Select(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in countries],
    value='Italy',
    className='mb-4'
)

# Info Cards with Current Numbers
card_content = dbc.CardBody([
    html.H5('Card title', className='card-title'),
    html.H2('Some Number', className='card-text')
])

cards = [
    dbc.Col(dbc.Card(card_content, color='primary', inverse=True)),
    dbc.Col(dbc.Card(card_content, color='danger', inverse=True)),
    dbc.Col(dbc.Card(card_content, color='secondary', inverse=True)),
]

# Checkboxes for CaseType Selection
checklist = dbc.FormGroup([
    dbc.Label('Selected Metrics'),
    dbc.Checklist(
        options=[{'label': case_type.capitalize(), 'value': case_type}
                 for case_type in case_types],
        value=['confirmed', 'death'],
        id='case-type-input',
        inline=True
    )
])

layout = html.Div([
    # Display App Description
    dbc.Row(dbc.Col(html.P(app_description))),

    # Country Selector
    dbc.Row([
        dbc.Col([
            # html.H4('Country'),
            dropdown,
        ]),
    ]),

    # Dipslay Current Numbers
    dbc.Row(cards, className='mb-4'),

    # Display Checkboxes for CaseType Selection
    dbc.Row(dbc.Col(checklist), className='mb-4'),

    # Display Cumulative Cases
    dbc.Row(dbc.Col([
        dcc.Graph(id='plot_cumulative_cases',
                  config={'displayModeBar': False}),
    ])),


    html.Div(id='app-2-display-value'),

])


# @app.callback(
#     Output('app-2-display-value', 'children'),
#     [Input('app-2-dropdown', 'value')])
# def display_value(value):
#     return 'You have selected "{}"'.format(value)
