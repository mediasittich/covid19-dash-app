import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app, server
from apps import index, world, countries, data

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavLink('About', href='/'),
            dbc.NavLink('World-wide', href='/world'),
            dbc.NavLink('Countries', href='/countries'),
            dbc.NavLink('Data', href='/data'),
        ],
        brand='COVID-19 Project',
        brand_href='/',
        color='light',
        dark=False
    ),
    dbc.Container(id='page-content', className='pt-4')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def render_page_content(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/world':
        return world.layout
    elif pathname == '/countries':
        return countries.layout
    elif pathname == '/data':
        return data.layout
    else:
        return dbc.Jumbotron([
            html.H1('404: Not found', className='text-danger')
        ])


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
