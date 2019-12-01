from dash.exceptions import PreventUpdate
from readers import *
import plotly.graph_objs as go
from plotly.subplots import make_subplots

color_list = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#7f7f7f',  # middle gray
    '#bcbd22',  # curry yellow-green
    '#17becf'  # blue-teal
]


def plotter_v1(home_name, year, apps, weather):
    df = merger(home_name, year)
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    color_count = 0
    fig.add_trace(
        go.Scatter(x=df["Date"],
                   y=df[weather],
                   name=weather,
                   line=dict(color="black", width=0.5)),
        secondary_y=True
    )
    if apps is None:
        raise PreventUpdate
    else:
        for app in apps:
            fig.add_trace(
                go.Scatter(x=df["Date"],
                           y=df[app],
                           name=app,
                           line=dict(color=color_list[color_count], width=1)),
                secondary_y=False
            )
            color_count += 1
    fig.update_layout(title='Appliance Power Consumption across Weather Conditions ' + home_name + ' ' + year)
    fig.update_xaxes(title_text="Months", nticks=6)
    fig.update_yaxes(title_text=weather, secondary_y=True)
    fig.update_yaxes(title_text="Power Consumption", secondary_y=False)
    return fig
