import plotly as py
import plotly.graph_objects as go

case_type_colors = {'confirmed': '#2780E3',
                    'death': '#FF0039', 'recovered': '#373a3c'}


def plot_timeseries_line():
    pass


def plot_timeseries_bar():
    pass


def plot_multiple_timeseries(data, metric, case_types, scale_type):
    # dict_of_fig = dict({
    #     'data': [],
    #     'layout': []
    # })

    fig = go.Figure()

    for ct in case_types:
        print(ct)
        df = data[data['CaseType'] == ct]

        fig.add_trace(
            go.Scatter(
                x=df['Date'],
                y=df[metric],
                mode='lines',
                name=ct.capitalize(),
                marker_color=case_type_colors[ct]
            )
        )

    fig.update_yaxes(type=scale_type)
    # fig['layout']['yaxis'].update(type=scale_type)

    return fig
