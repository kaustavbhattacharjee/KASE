import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotters import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app_options = {
    "HomeA": ["FurnaceHRV [kW]", "Refrigerator [kW]", "KitchenDenLights [kW]", "DishwasherDisposalSinkLight [kW]",
              "OfficeLights [kW]", "CellarOutlets [kW]", "Dryer [kW]", "BasementOutdoorOutlets [kW]"],
    "HomeB": ["Grid [kW]", "AC [kW]", "Furnace [kW]", "Utility Rm + Basement Bath [kW]", "Home Office (R) [kW]",
              "Home office [kW]", "Guest Bedroom / Media Room [kW]"],
    "HomeC": ["LivingRoomOutlets [kW]", "House overall [kW]", "Furnace 1 [kW]", "Furnace 2 [kW]", "Home office [kW]",
              "Fridge [kW]", "Wine cellar [kW]", "Living room [kW]"]
}
year_options = {
    "HomeA": ["2014", "2015", "2016"],
    "HomeB": ["2014", "2015", "2016"],
    "HomeC": ["2014", "2015", "2016"]
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
        html.Label("Task1"),

        dcc.Dropdown(
            id="drop-down-year",
            value="2016"
        ),
        dcc.Dropdown(
            id="drop-down-apps",
            multi=True,
        ),
        dcc.Dropdown(
            id="drop-down-homes",
            value='HomeA',
            options=[
                {'label': 'Home A', 'value': 'HomeA'},
                {'label': 'Home B', 'value': 'HomeB'},
                {'label': 'Home C', 'value': 'HomeC'}
            ]
        ),
        dcc.RadioItems(
            id="radio-weather",
            options=[
                {'label': 'Temperature', 'value': 'temperature'},
                {'label': 'Pressure', 'value': 'pressure'},
                {'label': 'WindSpeed', 'value': 'windSpeed'}
            ],
            value="temperature"
        ),
        html.Div([
            dcc.Graph(
                id='Vis-1',
            ),
            dcc.Graph(
                id='Vis-2',
            )
        ])
    ])
])


@app.callback(
    [Output("drop-down-year", "options"),
     Output("drop-down-apps", "options")],
    [Input("drop-down-homes", "value")])
def update_comps(home_name):
    return [{'label': i, 'value': i} for i in year_options[home_name]], [{'label': i, 'value': i} for i in
                                                                         app_options[home_name]]


@app.callback(
    [Output('Vis-1', 'figure'),
     Output("Vis-2", "figure")],
    [Input("drop-down-homes", "value"),
     Input("drop-down-year", "value"),
     Input("drop-down-apps", "value"),
     Input("radio-weather", "value")],
)
def update_graph(home_name, year, apps, weather):
    df = merger(home_name, year)

    df["Temperature range"] = df["temperature"].apply(roundup_v1)
    df["Temperature range"] = [("(" + str(row - 10) + "," + str(row) + ")") for row in df["Temperature range"]]

    df["Pressure range"] = df["pressure"].apply(roundup_v1)
    df["Pressure range"] = [("(" + str(row - 10) + "," + str(row) + ")") for row in df["Pressure range"]]

    df["windSpeed range"] = df["windSpeed"].apply(roundup_v2)
    df["windSpeed range"] = [("(" + str(row - 1) + "," + str(row) + ")") for row in df["windSpeed range"]]

    fig_1 = make_subplots(specs=[[{"secondary_y": True}]])
    fig_2 = make_subplots(rows=1, cols=3, y_title="Power Consumption [kW]")

    color_count = 0
    fig_1.add_trace(
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
            fig_1.add_trace(
                go.Scatter(x=df["Date"],
                           y=df[app],
                           name=app,
                           line=dict(color=color_list[color_count], width=1)),
                secondary_y=False
            )
            fig_2.add_trace(
                go.Scatter(
                    x=df["Temperature range"].sort_values(ascending=True),
                    y=df[app],
                    name=app,
                    mode='markers',
                    marker_color=color_list[color_count],
                    opacity = 0.5
                ), row=1, col=1,
            )
            fig_2.add_trace(
                go.Scatter(
                    x=df["Pressure range"].sort_values(ascending=True),
                    y=df[app],
                    name=app,
                    mode='markers',
                    marker_color=color_list[color_count],
                    opacity=0.5,
                    showlegend = False
                ), row=1, col=2
            )
            fig_2.add_trace(
                go.Scatter(
                    x=df["windSpeed range"].sort_values(ascending=True),
                    y=df[app],
                    name=app,
                    mode='markers',
                    marker_color=color_list[color_count],
                    opacity=0.5,
                    showlegend=False
                ), row=1, col=3
            )
            color_count += 1

    fig_1.update_layout(title='Appliance Power Consumption across Weather Conditions ' + home_name + ' ' + year)
    fig_1.update_xaxes(title_text="Months", nticks=6)
    fig_1.update_yaxes(title_text=weather, secondary_y=True)
    fig_1.update_yaxes(title_text="Power Consumption", secondary_y=False)
    fig_2.update_xaxes(title_text="Temperature (C)", row=1, col=1)
    fig_2.update_xaxes(title_text="Pressure(mBar)", row=1, col=2)
    fig_2.update_xaxes(title_text="WindSpeed(kmph)", row=1, col=3)

    return fig_1, fig_2


if __name__ == "__main__":
    app.run_server(debug=True)
