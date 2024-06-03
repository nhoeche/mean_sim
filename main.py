import math
from scipy.stats import norm
import numpy as np
import pandas as pd

from dash import Dash, html, dash_table, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from plotly import graph_objects as go

rng = np.random.default_rng()
data = px.data.medals_long()

stylesheets = [dbc.themes.BOOTSTRAP]
scripts = [{'src': 'https://cdn.tailwindcss.com'}]

app = Dash(__name__, external_scripts=scripts)


## IDS
ID_SLIDER_N = "slider-n"
ID_SLIDER_MU = "slider-mu"
ID_SLIDER_SIGMA = "slider-sigma"
ID_SLIDER_RUNS = "slider-runs"
ID_TABLE = "random-data-table"
ID_GRAPH_DIST = "graph_distribution"
ID_GRAPH_HISTS = "graph_histograms"

## COMPONENTS ##
slider_n = dcc.Slider(0, 100, 1,
                      id=ID_SLIDER_N,
                      marks={i:str(i) for i in range(0, 101, 20)},
                      value=10)
label_n = dbc.Label(children=[html.P("n: ")], id="label-n")

slider_mu = dcc.Slider(-10, 10, value=0,
                       id=ID_SLIDER_MU
)
label_mu = dbc.Label(children=[html.P("µ: ")], id="label-mu")

slider_sigma = dcc.Slider(1, 5, value=1, id=ID_SLIDER_SIGMA)
label_sigma = dbc.Label(children=[html.P("σ: ")], id="label-sigma")

slider_runs = dcc.Slider(1, 5, 1, value=1, id=ID_SLIDER_RUNS)
label_runs = dbc.Label(children=[html.P("N Durchgänge: ")], id="label-runs")

parameter_block = html.Div([
        html.Div([
                html.Div(label_mu,
                         className="w-1/8 p-4"), 
                html.Div(slider_mu,
                         style={"width":"87%"},
                         className="p-4")
            ],
            className="""
                flex items-center
                bg-white
                border border-gray-200
                rounded-md
                m-1
            """
        ),
        html.Div([
                html.Div(label_sigma,
                         className="w-1/8 p-4"), 
                html.Div(slider_sigma,
                         style={"width":"87%"},
                         className="p-4")
            ],
            className="""
                flex items-center
                bg-white
                border border-gray-200
                rounded-md
                m-1
            """
        ),
        html.Div([
                html.Div(label_n,
                         className=" p-4"), 
                html.Div(slider_n,
                         style={"width":"87%"},
                         className=" p-4")
            ],
            className="""
                flex items-center
                bg-white
                border border-gray-200
                rounded-md
                m-1
            """
        ),
        html.Div([
                html.Div(label_runs,
                         className="w-1/8 p-4"), 
                html.Div(slider_runs,
                         style={"width":"87%"},
                         className=" p-4")
            ],
            className="""
                flex items-center
                bg-white
                border border-gray-200
                rounded-md
                m-1
            """
        ),
    ],
    className="flex flex-col bg-gray-100 border border-solid border-gray-400 rounded-md p-2 m-4"                        
)

dist_plot = dcc.Graph(id=ID_GRAPH_DIST)
hist_plots = dcc.Graph(id=ID_GRAPH_HISTS)
sample_table = dash_table.DataTable(id=ID_TABLE, page_size=20)

# Layout
app.layout = dbc.Container([
        html.Div(
            html.H1("Schätzung des Erwartungswertes anhand einer Stichprobe"),
            className="bg-gray-200 font-large"),
        html.Hr(),
        parameter_block,
        dist_plot,
        hist_plots,
        sample_table
    ],
    fluid=True
)

## CALLBACKS ##
@callback(
        Output(ID_TABLE, "data"),
        Input(ID_SLIDER_MU, "value"),
        Input(ID_SLIDER_SIGMA, "value"),
        Input(ID_SLIDER_N, "value"),
        Input(ID_SLIDER_RUNS, "value"),
)
def generate_sample_data(mu, sigma, n, runs):
    """Generate random data"""
    data_dict = {f"x{i}": rng.normal(mu, sigma, n).round(2) for i in range(runs)}
    data = pd.DataFrame(data_dict)
    return data.to_dict('records')


@callback(
        Output(ID_GRAPH_DIST, "figure"),
        Input(ID_SLIDER_MU, "value"),
        Input(ID_SLIDER_SIGMA, "value"),
        Input(ID_TABLE, "data")
)
def generate_normal_distribution_graph(mu, sigma, sample):
    """Generate plot of normal distribution."""
    xn = np.linspace(mu-3.2*sigma, mu+3.2*sigma, 1000)
    yn = norm.pdf(xn, mu, sigma)
    yn2 = norm.cdf(xn, mu, sigma)

    sample = pd.DataFrame(sample)
    data = pd.DataFrame({'x': xn, 'probability_density': yn, 'cumulative_probability': yn2})
    
    fig = px.line(data,
                  x='x',
                  y='probability_density',
                  labels={"probability_density": "P(x)"})
    fig.add_vline(mu, line_color="red", annotation_text="Distribution mean")
    
    for col in sample:
        fig.add_vline(sample[col].mean(), line_dash="dash")

    return fig


@callback(
        Output(ID_GRAPH_HISTS, "figure"),
        Input(ID_SLIDER_N, "value"),
        Input(ID_TABLE, "data")
)
def generate_histograms_graph(n, sample):
    """Generate plots of sample histograms."""
    sample = pd.DataFrame(sample)
    sample = sample.melt(value_name="x", var_name="run")

    fig = px.histogram(sample,
                  x='x',
                  facet_col="run",
                #   nbins=math.ceil(n/10)
                  )
    
    for i, (name, col) in enumerate(sample.groupby("run")):
        fig.add_vline(col.x.mean(),
                      line_dash="dash",
                      col=i+1,
                      row=1,
                      annotation_text=f"mean = {col.x.mean():.2f}")

    return fig 


if __name__ == "__main__":
    app.run(debug=True)
