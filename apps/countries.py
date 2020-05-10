import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import datetime

from app import app
from src.features import covid_data_countries, case_types
from src.visualisations import plot_multiple_timeseries

app_description = '''
Here you can select a country and get infos for it.
'''
countries = covid_data_countries['DisplayName'].unique()

latest_date = covid_data_countries['Date'].max()

# Dropdown Country Selector
dropdown = dbc.Select(
    id='country-dropdown',
    options=[{'label': country, 'value': country} for country in countries],
    value='Italy',
    className='mb-4'
)

# Info Cards with Current Numbers
case_type_colors = {'confirmed': 'primary',
                    'death': 'danger', 'recovered': 'secondary'}

cards = []

for case_type, color in case_type_colors.items():
    print(case_type, color)
    card_content = dbc.CardBody([
        html.H5('{}'.format(case_type.capitalize()), className='card-title'),
        html.H2('Some Number', id='number-{}'.format(case_type),
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
        id='case-type-input',
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
        id='yaxis-cumsum-scale-radioinput'
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

    dbc.Row(dbc.Col([
        html.H1(id='display-selection', className='mb-4'),
    ])),

    # Dipslay Current Numbers
    dbc.Row(cards, className='mb-4'),

    # Display Checkboxes for CaseType Selection
    dbc.Row([
        dbc.Col(checklist),
        dbc.Col(yaxis_cumsum_radioitems)
    ], className='mb-4'),


    # Display Cumulative Cases
    dbc.Row(dbc.Col([
        dcc.Graph(id='plot_cumulative_cases',
                  config={'displayModeBar': False}),
    ])),

])


@app.callback(
    Output('display-selection', 'children'),
    [Input('country-dropdown', 'value')])
def update_country(country):
    return '{}'.format(country)


@app.callback(
    [Output('number-confirmed', 'children'), Output('number-death',
                                                    'children'), Output('number-recovered', 'children')],
    [Input('country-dropdown', 'value')])
def update_numbers(country):
    df = covid_data_countries[(covid_data_countries['Date'] == latest_date) & (
        covid_data_countries['DisplayName'] == country)]
    num_confirmed = df[df['CaseType'] ==
                       'confirmed']['CumulativeReportedCases']
    num_death = df[df['CaseType'] == 'death']['CumulativeReportedCases']
    num_recovered = df[df['CaseType'] ==
                       'recovered']['CumulativeReportedCases']

    return num_confirmed, num_death, num_recovered


@app.callback(
    Output('plot_cumulative_cases', 'figure'),
    # Output('plot_cumulative_cases', 'figure'),
    [Input('country-dropdown', 'value'), Input('case-type-input', 'value'),
     Input('yaxis-cumsum-scale-radioinput', 'value')])
def update_cumsum_graph(country, case_types, scale_type):
    df = covid_data_countries[
        covid_data_countries['DisplayName'] == country]
    return plot_multiple_timeseries(df, 'CumulativeReportedCases', case_types, scale_type)
