
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_table

from app import app
from src.features import covid_data_countries, covid_data_world, case_types

data_description = '''
Some useful info
'''

# table_style = dict(
#     overflowX='auto',
#     margin=dict(
#         l=35,
#     )
# )
# table_header_style = dict(
#     fontWeight='bold',
# )

layout = html.Div([
    # Page Header
    dbc.Row([
        dbc.Col([
            html.H3('Data'),
            html.P(data_description),
        ]),
    ]),
    # World-wide Map and Data

    html.Br(),

    dbc.Row(dbc.Col([
        dash_table.DataTable(
            id='covid-cases-table',
            columns=[{'name': i, 'id': i}
                     for i in covid_data_world.columns],
            data=covid_data_countries.head().to_dict('records'),
            page_size=10,  # for pagination with 10 rows per page
            #style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            # fixed_rows={'headers': True},
            # style_table={'height': 400},
            # style_table=table_style,
            # style_header=table_header_style
        )
    ]))

])
