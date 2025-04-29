from dash import dcc, html
import pandas as pd
import plotly.express as px
import folium
import numpy as np
from folium.plugins import HeatMap
from google.cloud import storage
from google.cloud import bigquery
from io import StringIO
import os

client = bigquery.Client()
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = os.environ.get("DATASET_ID")
TABLE = os.environ.get("TABLE_ID")

PROJECT_ID = 'cs163-final-project' if PROJECT_ID is None else PROJECT_ID
DATASET = 'us_accident_data' if DATASET is None else DATASET
TABLE = 'us_accidents' if TABLE is None else TABLE

def severity_distribution():
    query = f"""
        SELECT Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    severity_counts = df["Severity"].value_counts().sort_index()
    fig = px.bar(x=severity_counts.index, y=severity_counts.values,
                 labels={'x': 'Severity Level', 'y': 'Number of Accidents'},
                 title='Accident Severity Distribution')
    return dcc.Graph(figure=fig)

 
def feature_correlation():
    query = f"""
        SELECT
            Severity,
            `Temperature_F_`,
            `Wind_Chill_F_`,
            `Humidity_%_`,
            `Pressure_in_`,
            `Visibility_mi_`,
            `Wind_Speed_mph_`,
            `Precipitation_in_`
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Severity IS NOT NULL
    """

    df = client.query(query).to_dataframe()
    corr_matrix = df.corr()
    fig = px.imshow(corr_matrix, text_auto=True,
                    color_continuous_scale='Viridis',
                    title='Feature Correlation Heatmap')
    return dcc.Graph(figure=fig)


def precipitation_vs_severity():
    query = f"""
        SELECT Precipitation_in_ AS Precipitation, Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Precipitation_in_ IS NOT NULL AND Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    fig = px.scatter(df, x="Precipitation", y="Severity", log_x=True,
                     title="Precipitation vs Severity (Log Scale)",
                     labels={"Precipitation": "Precipitation (in)", "Severity": "Severity"})
    return dcc.Graph(figure=fig)


def accidents_by_state():
    query = f"""
        SELECT State
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE State IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    state_counts = df["State"].value_counts().sort_values(ascending=False)
    fig = px.bar(x=state_counts.index, y=state_counts.values,
                 labels={'x': 'State', 'y': 'Number of Accidents'},
                 title='Accident Distribution by State')
    return dcc.Graph(figure=fig)


def accident_heatmap():
    query = f"""
        SELECT Start_Lat, Start_Lng
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Start_Lat IS NOT NULL AND Start_Lng IS NOT NULL
    """
    try:
        df = client.query(query).to_dataframe()
        
        heat_data = df[["Start_Lat", "Start_Lng"]].values.tolist()
        m = folium.Map(location=[37.8, -96], zoom_start=5, tiles="CartoDB Voyager")
    
        HeatMap(heat_data, radius=2, blur=2, max_zoom=10).add_to(m)
        map_html = m.get_root().render()
        return html.Iframe(srcDoc=map_html, width='100%', height='600px')
    except Exception as e:
        return html.Div(f"Error rendering heatmap: {str(e)}")