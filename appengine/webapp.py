from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import folium
import numpy as np
from folium.plugins import HeatMap
from google.cloud import storage
from io import StringIO
import os

# Fetch CSV from Google Cloud Storage
def get_csv_from_gcs(bucket_name, source_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    data = blob.download_as_text()
    return pd.read_csv(StringIO(data))

# Set up app and data
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

BUCKET_NAME = os.environ.get("BUCKET_NAME")

df = get_csv_from_gcs(BUCKET_NAME, "us_accidents_01.csv")

# # df = df.sample(n=30000, random_state=42)

def severity_distribution():
    return dcc.Iframe(src="/assets/severity.html", width="100%", height="600")

def feature_correlation():
    return dcc.Iframe(src="/assets/correlation.html", width="100%", height="600")

def precipitation_vs_severity():
    return dcc.Iframe(src="/assets/precipitation.html", width="100%", height="600")

def accidents_by_state():
    return dcc.Iframe(src="/assets/states.html", width="100%", height="600")

def accident_heatmap():
    return dcc.Iframe(src="/assets/heatmap.html", width="100%", height="600")

# Styled container
container_style = {
    'width': '85%',
    'margin': '0 auto',
    'padding': '40px 20px',
    'fontFamily': 'Segoe UI, sans-serif',
    'backgroundColor': '#f9f9f9'
}

header_style = {
    'textAlign': 'center',
    'color': '#003366',
    'marginBottom': '40px'
}

section_style = {
    'backgroundColor': '#ffffff',
    'padding': '30px',
    'marginBottom': '30px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)'
}

# Home layout
def home_page():
    return html.Div(style=container_style, children=[
        html.H1("US Accidents Analysis Dashboard", style=header_style),

        html.Div(style=section_style, children=[
            html.H2(html.A("Accident Severity Distribution", href="/severity")),
            severity_distribution()
        ]),

        html.Div(style=section_style, children=[
            html.H2(html.A("Feature Correlation Heatmap", href="/correlation")),
            feature_correlation()
        ]),

        html.Div(style=section_style, children=[
            html.H2(html.A("Precipitation vs Severity", href="/precipitation")),
            precipitation_vs_severity()
        ]),

        html.Div(style=section_style, children=[
            html.H2(html.A("Accidents by State", href="/states")),
            accidents_by_state()
        ]),

        html.Div(style=section_style, children=[
            html.H2(html.A("US Accident Heatmap", href="/heatmap")),
            accident_heatmap()
        ])
    ])

# App routing
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/severity':
        return html.Div(style=container_style, children=[html.H1("Severity Distribution Summary", style=header_style), severity_distribution()])
    elif pathname == '/correlation':
        return html.Div(style=container_style, children=[html.H1("Correlation Heatmap Summary", style=header_style), feature_correlation()])
    elif pathname == '/precipitation':
        return html.Div(style=container_style, children=[html.H1("Precipitation vs Severity Summary", style=header_style), precipitation_vs_severity()])
    elif pathname == '/states':
        return html.Div(style=container_style, children=[html.H1("State Distribution Summary", style=header_style), accidents_by_state()])
    elif pathname == '/heatmap':
        return html.Div(style=container_style, children=[html.H1("Heatmap Summary", style=header_style), accident_heatmap()])
    else:
        return home_page()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
