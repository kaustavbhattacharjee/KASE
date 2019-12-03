import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from readers import *
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import csv,os
from pathlib import Path
import plotly.express as px
import pandas as pd
import math
from abs_path import return_abs_path,return_abs_path2


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app_options = {
    "A":["Temperature [F]", "Humidity [g/m3]"]
}
year_options = {
    "A":["2014", "2015", "2016"]
}

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

app.layout = html.Div([
    html.Div([
        html.Label("Task2"),

        dcc.Dropdown(
            id="drop-down-year",
            options=[
            {'label': '2014', 'value': '2014'},
            {'label': '2015', 'value': '2015'},
            {'label': '2016', 'value': '2016'}
        ],
            value="2014"
        ),

        dcc.RadioItems(
            id="radio-weather",
            options=[
                {'label': 'Temperature', 'value': 'temperature'},
                {'label': 'Humidity', 'value': 'humidity'}
            ],
            value="temperature"
        ),
        html.H3("Primary Visualization"),
        html.Div([
            dcc.Graph(
                id='Vis-1',
            )
        ]),
        html.H3("Alternative Visualization"),
        html.Div([
            dcc.Graph(
                id='Vis-2',
            )
        ])
    ])
])



@app.callback(
    [Output('Vis-1', 'figure'),
     Output("Vis-2", "figure")],
    [Input("drop-down-year", "value"),
     Input("radio-weather", "value")],
)
def update_graph(year,weather):
    filename = "visualizations/task2_"+str(weather)+"_"+str(year)+"_line.csv"
    title = "Mean Power Consumption across different "+str(weather)+"("+str(year)+")"
    xaxis_title_dict = {"temperature":"Temperature(in F)","humidity":"Humidity(g/m3)"}
    df = pd.read_csv(filename, names=[str(weather), 'power'])
    fig1 = px.line(df, x=str(weather), y='power', title=title)
    fig1.update_xaxes(ticks="inside", title_font=dict(family='Georgia', color='black'),tickfont=dict(family='Georgia', color='black'))
    fig1.update_yaxes(title_font=dict(family='Georgia', color='black'), tickfont=dict(family='Georgia', color='black'))
    fig1.update_layout(font=dict(family="Georgia", color="black"), xaxis_title=xaxis_title_dict[str(weather)],yaxis_title="Power(kW)")
    return [fig1,fig1]








if __name__ == "__main__":
    app.run_server(debug=True)
