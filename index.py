import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app, server
from apps import index, app1, app2, data

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavLink('About', href='/'),
            dbc.NavLink('World-wide', href='/app1'),
            dbc.NavLink('Countries', href='/app2'),
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
    elif pathname == '/app1':
        return app1.layout
    elif pathname == '/app2':
        return app2.layout
    elif pathname == '/data':
        return data.layout
    else:
        return dbc.Jumbotron([
            html.H1('404: Not found', className='text-danger')
        ])


if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=True)
