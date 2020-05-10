import plotly as py
import plotly.graph_objects as go


def plot_timeseries_line():
    fig = go.Figure()

    pass


def plot_timeseries_bar():
    pass


def plot_multiple_timeseries(x, y):
    # dict_of_fig = dict({
    #     'data': [],
    #     'layout': []
    # })

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines',
        )
    )

    return fig
