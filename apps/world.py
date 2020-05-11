
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table

import datetime

from app import app
from src.features import covid_data_countries, covid_data_world, case_types
from src.visualisations import plot_multiple_timeseries

map_description = '''
Some useful info
'''

countries = covid_data_countries['DisplayName'].unique()

latest_date = covid_data_countries['Date'].max()

# Info Cards with Current Numbers
case_type_colors = {'confirmed': 'primary',
                    'death': 'danger', 'recovered': 'secondary'}

cards = []

df = covid_data_world[covid_data_world['Date'] == latest_date]

for case_type, color in case_type_colors.items():
    case_num = df[df['CaseType'] == case_type]['CumulativeReportedCases']

    card_content = dbc.CardBody([
        html.H5('{}'.format(case_type.capitalize()), className='card-title'),
        html.H2(case_num, id='number-world-{}'.format(case_type),
                className='card-text')
    ])
    cards.append(dbc.Col(dbc.Card(card_content, color=color, inverse=True)))


# Checkboxes for CaseType Selection
checklist = dbc.FormGroup([
    dbc.Label('Selected Metrics'),
    dbc.Checklist(
        options=[{'label': case_type.capitalize(), 'value': case_type}
                 for case_type in case_types],
        value=['confirmed', 'death'],
        id='case-type-world-input',
        inline=True
    )
])

# Select Axis Scale
yaxis_cumsum_radioitems = dbc.FormGroup([
    dbc.Label('Select y-Axis Scale'),
    dbc.RadioItems(
        options=[
            {'label': 'linear', 'value': 'linear'},
            {'label': 'logarithmic', 'value': 'log'}
        ],
        value='linear',
        id='yaxis-cumsum-scale-world-radioinput'
    )
])


layout = html.Div([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.P(map_description),
        ]),
    ]),

    # Display Current Numbers
    dbc.Row(cards, className='mb-4'),

    # World-wide Map and Data

    # Display Checkboxes for CaseType Selection
    dbc.Row([
        dbc.Col(checklist),
        dbc.Col(yaxis_cumsum_radioitems)
    ], className='mb-4'),

    # Display Cumulative Cases
    dbc.Row(dbc.Col([
        dcc.Graph(id='plot_cumulative_cases_world',
                  config={'displayModeBar': False}),
    ])),

])
