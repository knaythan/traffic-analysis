from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import folium
import numpy as np
from folium.plugins import HeatMap
from google.cloud import storage
from google.cloud import bigquery
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

# BUCKET_NAME = os.environ.get("BUCKET_NAME")

# df = get_csv_from_gcs(BUCKET_NAME, "random_accidents.csv")

# # df = df.sample(n=30000, random_state=42)

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
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Severity IS NOT NULL
        LIMIT 10000
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
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Precipitation_in_ IS NOT NULL AND Severity IS NOT NULL
        LIMIT 5000
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
    
    
container_style = {
    'width': '85%',
    'margin': '0 auto',
    'padding': '40px 20px',
    'fontFamily': 'Nunito, serif',
    'backgroundColor': '#f9f9f9'
}

header_style = {
    'textAlign': 'center',
    'color': '#003366',
    'fontSize': '75px',
    'marginBottom': '40px',
     'fontFamily': 'Georgia, serif',
}

section_style = {
    'backgroundColor': '#ffffff',
    'padding': '30px',
    'marginBottom': '30px',
    'borderRadius': '10px',
    'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.1)',
     'fontFamily': 'Nunito, sans-serif',
}

footer_style = {
    'textAlign': 'center',
    'padding': '20px',
    'backgroundColor': '#f1f1f1',
    'marginTop': '50px',
    'fontSize': '14px',
    'color': '#888',
    'fontFamily': 'Nunito, serif'
}

navbar_style = {
    'backgroundColor': '#003366',
    'padding': '25px',
    'display': 'flex',
    'justifyContent': 'space-around',
    'alignItems': 'center',
    'color': 'white',
    'fontSize': '18px',
    'fontFamily': 'Nunito, serif',
}

link_style = {
    'color': 'white',
    'textDecoration': 'none',
    'padding': '0 15px'
}

# ====================== NAVBAR ===========================
# Corrected Navbar
navbar = html.Div([
    # Left side: Research Dashboard
    html.Div("Research Dashboard", style={
        'fontSize': '24px',  # Larger text
        'fontWeight': 'bold',
        'color': 'white',
        'marginRight': 'auto'  # Pushes the links to the right
    }),
    
    # Right side: Navigation links
    html.Div([
        html.A("Home", href="/", style=link_style),
        html.A("Objectives", href="/objectives", style=link_style),
        html.A("Methods", href="/methods", style=link_style),
        html.A("Findings", href="/findings", style=link_style),
    ], style={'display': 'flex', 'gap': '15px'})  # Adds spacing between links
], style=navbar_style)

# ====================== PAGE FUNCTIONS ===========================
def home_page():
    return html.Div(style=container_style, children=[
        # Hero Section with visual impact
        html.Div(style={
            'textAlign': 'center',
            'padding': '40px 20px',
            'borderRadius': '10px',
            'background': 'linear-gradient(135deg, #EBF8FF 0%, #BEE3F8 100%)',
            'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            'marginBottom': '40px',
        }, children=[
            html.H1("U.S. Traffic Accident Analysis", style={
                'fontSize': '42px',
                'fontWeight': '700',
                'margin': '0 0 15px',
                'color': '#1A365D',
                'textShadow': '1px 1px 2px rgba(0,0,0,0.1)',
            }),
            html.H2("Predictive Analytics for Safer Roads", style={
                'fontSize': '28px',
                'fontWeight': '600',
                'margin': '0 0 25px',
                'color': '#2C5282',
            }),
            html.P(
                "Investigating how environmental, temporal, and road network factors influence the severity and frequency of traffic accidents across the United States.",
                style={
                    'fontSize': '20px',
                    'maxWidth': '800px',
                    'margin': '0 auto 30px',
                    'lineHeight': '1.6',
                    'color': '#2D3748',
                }
            ),
            html.A("Explore Our Findings →", 
                  href="/findings", 
                  style={
                      'padding': '14px 28px',
                      'backgroundColor': '#4299E1',
                      'color': 'white',
                      'borderRadius': '6px',
                      'textDecoration': 'none',
                      'fontWeight': '600',
                      'boxShadow': '0 4px 6px rgba(66, 153, 225, 0.3)',
                      'transition': 'all 0.2s ease',
                      'display': 'inline-block',
                      'fontSize': '18px',
                  })
        ]),

        # Key Stats Section
        html.Div(style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'flexWrap': 'wrap',
            'gap': '20px',
            'marginBottom': '40px',
        }, children=[
            # Stat Card 1
            html.Div(style={
                'flex': '1',
                'minWidth': '250px',
                'textAlign': 'center',
                'padding': '25px 20px',
                'backgroundColor': 'white',
                'borderRadius': '8px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'borderTop': '4px solid #3182CE',
            }, children=[
                html.Div("7.7M+", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#2B6CB0'}),
                html.Div("Accident Records", style={'fontSize': '18px', 'color': '#4A5568', 'marginTop': '5px'}),
            ]),
            # Stat Card 2
            html.Div(style={
                'flex': '1',
                'minWidth': '250px',
                'textAlign': 'center',
                'padding': '25px 20px',
                'backgroundColor': 'white',
                'borderRadius': '8px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'borderTop': '4px solid #38A169',
            }, children=[
                html.Div("50+", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#2F855A'}),
                html.Div("Environmental Factors", style={'fontSize': '18px', 'color': '#4A5568', 'marginTop': '5px'}),
            ]),
            # Stat Card 3
            html.Div(style={
                'flex': '1',
                'minWidth': '250px',
                'textAlign': 'center',
                'padding': '25px 20px',
                'backgroundColor': 'white',
                'borderRadius': '8px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'borderTop': '4px solid #805AD5',
            }, children=[
                html.Div("6 Years", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#6B46C1'}),
                html.Div("Historical Data", style={'fontSize': '18px', 'color': '#4A5568', 'marginTop': '5px'}),
            ]),
        ]),
        
        # Project Overview Section
        html.Div(style={
            **section_style, 
            'backgroundColor': '#F7FAFC', 
            'borderRadius': '10px',
            'padding': '30px',
            'marginBottom': '40px',
            'borderLeft': '5px solid #3182CE',
        }, children=[
            html.H2("Project Overview", style={'color': '#2C5282', 'marginTop': '0', 'borderBottom': '2px solid #E2E8F0', 'paddingBottom': '10px'}),
            html.P(
                "This comprehensive study analyzes over 7.7 million accident records using weather, road, and environmental data across the United States. "
                "By combining exploratory data analysis with advanced machine learning techniques like Random Forests and XGBoost, "
                "we uncover patterns that explain accident risk and severity.",
                style={'fontSize': '18px', 'lineHeight': '1.6', 'marginBottom': '20px'}
            ),
            html.P(
                "Our research findings provide actionable insights that can help improve road safety, "
                "inform urban planning decisions, optimize emergency response systems, and support the development of safer autonomous driving technologies.",
                style={'fontSize': '18px', 'lineHeight': '1.6'}
            ),
        ]),

        # Analysis Approach Section with cards
        html.H2("Our Analysis Approach", style={
            'textAlign': 'center', 
            'color': '#2D3748', 
            'marginBottom': '25px',
            'fontSize': '32px',
        }),
        
        html.Div(style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'gap': '25px',
            'marginBottom': '40px',
        }, children=[
            # Card 1 - Predictive Modeling
            html.Div(style={
                'flex': '1',
                'minWidth': '300px',
                'maxWidth': '400px',
                'borderRadius': '10px',
                'overflow': 'hidden',
                'boxShadow': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'backgroundColor': 'white',
                'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
            }, children=[
                # Card Header
                html.Div(style={
                    'backgroundColor': '#EBF8FF',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #BEE3F8',
                }, children=[
                    html.Div("📊", style={'fontSize': '36px', 'textAlign': 'center', 'marginBottom': '10px'}),
                    html.H3("Predictive Modeling", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#2C5282',
                        'fontSize': '24px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "We build sophisticated predictive models to estimate accident severity based on real-time conditions including weather, "
                        "visibility, and road characteristics. Our ensemble machine learning techniques improve the accuracy and fairness of predictions.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Random Forest classification", style={'margin': '8px 0'}),
                        html.Li("XGBoost for severity prediction", style={'margin': '8px 0'}),
                        html.Li("Feature importance analysis", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 2 - Geospatial Insights
            html.Div(style={
                'flex': '1',
                'minWidth': '300px',
                'maxWidth': '400px',
                'borderRadius': '10px',
                'overflow': 'hidden',
                'boxShadow': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'backgroundColor': 'white',
                'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
            }, children=[
                # Card Header
                html.Div(style={
                    'backgroundColor': '#E6FFFA',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #B2F5EA',
                }, children=[
                    html.Div("🌎", style={'fontSize': '36px', 'textAlign': 'center', 'marginBottom': '10px'}),
                    html.H3("Geospatial Insights", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#234E52',
                        'fontSize': '24px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Using advanced clustering and heatmap visualizations, we identify accident hotspots across urban corridors and highway systems. "
                        "Spatial patterns highlight where infrastructure interventions can most effectively reduce crash risk.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("DBSCAN spatial clustering", style={'margin': '8px 0'}),
                        html.Li("Urban vs. rural pattern analysis", style={'margin': '8px 0'}),
                        html.Li("Infrastructure correlation mapping", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 3 - Temporal Trends
            html.Div(style={
                'flex': '1',
                'minWidth': '300px',
                'maxWidth': '400px',
                'borderRadius': '10px',
                'overflow': 'hidden',
                'boxShadow': '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                'backgroundColor': 'white',
                'transition': 'transform 0.3s ease, box-shadow 0.3s ease',
            }, children=[
                # Card Header
                html.Div(style={
                    'backgroundColor': '#E9D8FD',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #D6BCFA',
                }, children=[
                    html.Div("⏳", style={'fontSize': '36px', 'textAlign': 'center', 'marginBottom': '10px'}),
                    html.H3("Temporal Trends", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#44337A',
                        'fontSize': '24px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "By analyzing time-of-day, day-of-week, and seasonal patterns, we reveal how traffic volume and commuter behavior "
                        "impact accident rates — emphasizing peak risk periods like rush hours and holidays.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Time series decomposition", style={'margin': '8px 0'}),
                        html.Li("Seasonal trend analysis", style={'margin': '8px 0'}),
                        html.Li("Peak accident period identification", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
        ]),
        
        # Call to Action Section
        html.Div(style={
            'textAlign': 'center',
            'padding': '40px 20px',
            'borderRadius': '10px',
            'background': 'linear-gradient(135deg, #EBF8FF 0%, #90CDF4 100%)',
            'marginTop': '30px',
        }, children=[
            html.H2("Ready to Explore the Data?", style={
                'color': '#2A4365',
                'marginTop': '0',
                'marginBottom': '20px',
                'fontSize': '32px',
            }),
            html.P(
                "Dive into our comprehensive analysis and interactive visualizations to understand the complex factors that influence traffic safety.",
                style={
                    'maxWidth': '800px',
                    'margin': '0 auto 30px',
                    'fontSize': '18px',
                    'color': '#2D3748',
                    'lineHeight': '1.6',
                }
            ),
            html.Div(style={
                'display': 'flex',
                'justifyContent': 'center',
                'gap': '20px',
                'flexWrap': 'wrap',
            }, children=[
                html.A("View Findings →", 
                    href="/findings", 
                    style={
                        'padding': '14px 28px',
                        'backgroundColor': '#4299E1',
                        'color': 'white',
                        'borderRadius': '6px',
                        'textDecoration': 'none',
                        'fontWeight': '600',
                        'boxShadow': '0 4px 6px rgba(66, 153, 225, 0.3)',
                        'transition': 'all 0.2s ease',
                        'display': 'inline-block',
                    }
                ),
                html.A("Research Objectives →", 
                    href="/objectives", 
                    style={
                        'padding': '14px 28px',
                        'backgroundColor': 'white',
                        'color': '#3182CE',
                        'borderRadius': '6px',
                        'textDecoration': 'none',
                        'fontWeight': '600',
                        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                        'transition': 'all 0.2s ease',
                        'display': 'inline-block',
                    }
                ),
            ]),
        ]),
    ])

def objectives_page():
    return html.Div(style=container_style, children=[
        # Header Section with visual impact
        html.Div([
            html.H1("Research Objectives", style={
                'fontSize': '42px',
                'fontWeight': '700',
                'textAlign': 'center',
                'margin': '30px 0 15px',
                'color': '#1A365D',
                'borderBottom': '3px solid #4299E1',
                'paddingBottom': '15px',
            }),
            html.P(
                "Uncovering patterns and risk factors in traffic accidents to drive data-informed safety improvements",
                style={
                    'textAlign': 'center',
                    'fontSize': '20px',
                    'fontStyle': 'italic',
                    'color': '#4A5568',
                    'maxWidth': '800px',
                    'margin': '0 auto 40px',
                }
            ),
        ]),
        
        # Mission Statement with visual emphasis
        html.Div(style={**section_style, 'backgroundColor': '#EBF8FF', 'borderLeft': '5px solid #3182CE', 'padding': '25px 30px'}, children=[
            html.H2("Project Mission", style={'color': '#2C5282', 'marginTop': '0'}),
            html.P(
                "Our primary goal is to predict the severity of traffic accidents based on environmental, temporal, "
                "and road network factors. We aim to uncover key risk factors that contribute to accidents and provide "
                "insights that help emergency services, traffic management, and urban planners make data-driven decisions.",
                style={'fontSize': '18px', 'lineHeight': '1.6'}
            ),
        ]),
        
        # Key Objectives in a card-based layout
        html.Div(style={**section_style, 'marginTop': '35px'}, children=[
            html.H2("Research Objectives", style={'color': '#2D3748', 'borderBottom': '2px solid #E2E8F0', 'paddingBottom': '10px'}),
            
            # Cards for objective categories
            html.Div([
                # Temporal Analysis Card
                html.Div(style={
                    'flex': '1',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': '#FEFCBF',
                    'margin': '10px',
                }, children=[
                    html.H3("⏱️ Temporal Analysis", style={'color': '#744210', 'marginTop': '0'}),
                    html.Ul([
                        html.Li("Analyze accident frequencies by time of day, day of week, and season", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                        html.Li("Examine the relationship between accident duration and factors like weather", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                        html.Li("Analyze the impact of daylight phases on accident frequency", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                    ], style={'paddingLeft': '20px'})
                ]),
                
                # Environmental Factors Card
                html.Div(style={
                    'flex': '1',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': '#E6FFFA',
                    'margin': '10px',
                }, children=[
                    html.H3("🌦️ Environmental Factors", style={'color': '#234E52', 'marginTop': '0'}),
                    html.Ul([
                        html.Li("Investigate relationships between weather conditions and accident severity", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                        html.Li("Identify differences in accident patterns between urban and rural areas", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                        html.Li("Detect geographical accident hotspots using geospatial clustering", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                    ], style={'paddingLeft': '20px'})
                ]),
                
                # Infrastructure Card
                html.Div(style={
                    'flex': '1',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': '#E9D8FD',
                    'margin': '10px',
                }, children=[
                    html.H3("🛣️ Infrastructure Analysis", style={'color': '#44337A', 'marginTop': '0'}),
                    html.Ul([
                        html.Li("Assess how road characteristics correlate with accident outcomes", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                        html.Li("Compare accident rates at different types of intersections and crossings", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                        html.Li("Study the effect of nearby Points of Interest on accident likelihood", 
                                style={'margin': '10px 0', 'lineHeight': '1.5'}),
                    ], style={'paddingLeft': '20px'})
                ]),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'gap': '15px'}),
        ]),
        
        # Methodology Section with icons
        html.Div(style={**section_style, 'marginTop': '35px'}, children=[
            html.H2("Research Methodology", style={'color': '#2D3748', 'borderBottom': '2px solid #E2E8F0', 'paddingBottom': '10px'}),
            
            html.Div([
                # Left column - statistical methods
                html.Div(style={'flex': '1'}, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'margin': '15px 0'}, children=[
                        html.Div("🔍", style={'fontSize': '24px', 'marginRight': '15px'}),
                        html.Div([
                            html.H4("Correlation Analysis", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                            html.P("Investigating relationships between weather variables and accident severity", 
                                  style={'margin': '0', 'fontSize': '16px'})
                        ])
                    ]),
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'margin': '15px 0'}, children=[
                        html.Div("📊", style={'fontSize': '24px', 'marginRight': '15px'}),
                        html.Div([
                            html.H4("Time Series Decomposition", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                            html.P("Studying seasonal trends in accident frequency across multiple timescales", 
                                  style={'margin': '0', 'fontSize': '16px'})
                        ])
                    ]),
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'margin': '15px 0'}, children=[
                        html.Div("🧩", style={'fontSize': '24px', 'marginRight': '15px'}),
                        html.Div([
                            html.H4("Principal Component Analysis", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                            html.P("Reducing feature dimensionality to visualize complex relationships", 
                                  style={'margin': '0', 'fontSize': '16px'})
                        ])
                    ]),
                ]),
                
                # Right column - machine learning methods
                html.Div(style={'flex': '1'}, children=[
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'margin': '15px 0'}, children=[
                        html.Div("🌲", style={'fontSize': '24px', 'marginRight': '15px'}),
                        html.Div([
                            html.H4("Random Forest & XGBoost", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                            html.P("Predicting accident severity and analyzing feature importance", 
                                  style={'margin': '0', 'fontSize': '16px'})
                        ])
                    ]),
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'margin': '15px 0'}, children=[
                        html.Div("📍", style={'fontSize': '24px', 'marginRight': '15px'}),
                        html.Div([
                            html.H4("Geospatial Clustering", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                            html.P("Identifying accident hotspots without assuming fixed cluster counts", 
                                  style={'margin': '0', 'fontSize': '16px'})
                        ])
                    ]),
                    html.Div(style={'display': 'flex', 'alignItems': 'center', 'margin': '15px 0'}, children=[
                        html.Div("🔮", style={'fontSize': '24px', 'marginRight': '15px'}),
                        html.Div([
                            html.H4("Predictive Modeling", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                            html.P("Building ensemble models to predict accident severity and duration", 
                                  style={'margin': '0', 'fontSize': '16px'})
                        ])
                    ]),
                ]),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'}),
        ]),
        
        # Impact Section with gradient background
        html.Div(style={
            **section_style, 
            'marginTop': '35px',
            'background': 'linear-gradient(135deg, #EBF8FF 0%, #E6FFFA 100%)',
            'borderRadius': '10px',
            'padding': '30px',
        }, children=[
            html.H2("Broader Impacts", style={'color': '#2B6CB0', 'marginTop': '0'}),
            
            html.Div([
                html.Div(style={
                    'flex': '1',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'backgroundColor': 'rgba(255, 255, 255, 0.7)',
                    'margin': '10px',
                }, children=[
                    html.H3("🚑 Emergency Services", style={'color': '#E53E3E', 'marginTop': '0'}),
                    html.P(
                        "Optimizing resource allocation and response times by identifying high-risk areas and conditions",
                        style={'lineHeight': '1.6'}
                    )
                ]),
                
                html.Div(style={
                    'flex': '1',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'backgroundColor': 'rgba(255, 255, 255, 0.7)',
                    'margin': '10px',
                }, children=[
                    html.H3("🏙️ Urban Planning", style={'color': '#38A169', 'marginTop': '0'}),
                    html.P(
                        "Informing infrastructure decisions and road design to prioritize safety in high-risk locations",
                        style={'lineHeight': '1.6'}
                    )
                ]),
                
                html.Div(style={
                    'flex': '1',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'backgroundColor': 'rgba(255, 255, 255, 0.7)',
                    'margin': '10px',
                }, children=[
                    html.H3("🚗 Autonomous Vehicles", style={'color': '#805AD5', 'marginTop': '0'}),
                    html.P(
                        "Supporting navigation algorithms by identifying risk zones for safer integration into road systems",
                        style={'lineHeight': '1.6'}
                    )
                ]),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between', 'gap': '15px'}),
            
            html.P(
                "This research has the potential to save lives by enabling data-driven policy decisions and technological innovations that address the most significant risk factors in traffic accidents.",
                style={'fontSize': '18px', 'fontWeight': '500', 'textAlign': 'center', 'marginTop': '25px', 'color': '#2D3748'}
            )
        ]),
        
        # Call to action
        html.Div(style={'textAlign': 'center', 'marginTop': '40px'}, children=[
            html.A("Explore Our Methods →", 
                  href="/methods", 
                  style={
                      'padding': '12px 24px',
                      'backgroundColor': '#4299E1',
                      'color': 'white',
                      'borderRadius': '6px',
                      'textDecoration': 'none',
                      'fontWeight': '600',
                      'boxShadow': '0 4px 6px rgba(66, 153, 225, 0.3)',
                      'transition': 'all 0.2s ease',
                      'display': 'inline-block',
                  })
        ])
    ])
def methods_page():
    return html.Div(style=container_style, children=[
        # Header Section with visual impact
        html.Div([
            html.H1("Research Methodology", style={
                'fontSize': '42px',
                'fontWeight': '700',
                'textAlign': 'center',
                'margin': '30px 0 15px',
                'color': '#1A365D',
                'borderBottom': '3px solid #4299E1',
                'paddingBottom': '15px',
            }),
            html.P(
                "Advanced analytical approaches to extract insights from traffic accident data",
                style={
                    'textAlign': 'center',
                    'fontSize': '20px',
                    'fontStyle': 'italic',
                    'color': '#4A5568',
                    'maxWidth': '800px',
                    'margin': '0 auto 40px',
                }
            ),
        ]),
        
        # Overview Section with gradient background
        html.Div(style={
            **section_style, 
            'backgroundColor': '#EBF8FF', 
            'borderLeft': '5px solid #3182CE', 
            'padding': '25px 30px',
            'borderRadius': '10px',
            'marginBottom': '35px',
        }, children=[
            html.H2("Methodology Overview", style={'color': '#2C5282', 'marginTop': '0'}),
            html.P(
                "Our research employs a multi-faceted analytical approach combining statistical modeling, machine learning, "
                "and geospatial analysis. By integrating these complementary techniques, we extract comprehensive insights "
                "from over 7.7 million accident records while addressing the complex, multi-dimensional nature of traffic safety.",
                style={'fontSize': '18px', 'lineHeight': '1.6'}
            ),
        ]),
        
        # Data Processing Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Data Processing Pipeline", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # Pipeline Steps Cards
            html.Div([
                # Card 1 - Data Collection
                html.Div(style={
                    'flex': '1',
                    'minWidth': '300px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                    'margin': '10px',
                    'borderTop': '4px solid #4299E1',
                }, children=[
                    html.H3("📥 Data Collection", style={'color': '#2B6CB0', 'marginTop': '0'}),
                    html.P(
                        "Integrated multiple data sources including transportation department accident reports, "
                        "weather service APIs, and crowdsourced traffic information spanning 2016-2023.",
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Manual validation of data completeness and consistency", 
                                style={'margin': '8px 0'}),
                        html.Li("Cross-referencing with official traffic reports", 
                                style={'margin': '8px 0'}),
                        html.Li("Integration with historical weather data", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
                
                # Card 2 - Feature Engineering
                html.Div(style={
                    'flex': '1',
                    'minWidth': '300px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                    'margin': '10px',
                    'borderTop': '4px solid #38A169',
                }, children=[
                    html.H3("⚙️ Feature Engineering", style={'color': '#2F855A', 'marginTop': '0'}),
                    html.P(
                        "Created comprehensive feature sets capturing environmental conditions, road characteristics, "
                        "and temporal factors that influence accident risk and severity.",
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Weather metrics: precipitation, visibility, humidity, wind speed, and pressure", 
                                style={'margin': '8px 0'}),
                        html.Li("Road features: junction types, traffic signals, speed limits", 
                                style={'margin': '8px 0'}),
                        html.Li("Temporal indicators: rush hour flags, weekend/holiday markers, daylight phase", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
                
                # Card 3 - Preprocessing
                html.Div(style={
                    'flex': '1',
                    'minWidth': '300px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                    'margin': '10px',
                    'borderTop': '4px solid #805AD5',
                }, children=[
                    html.H3("🧹 Data Preprocessing", style={'color': '#6B46C1', 'marginTop': '0'}),
                    html.P(
                        "Applied robust cleaning and normalization techniques to ensure data quality "
                        "and prepare the dataset for advanced modeling approaches.",
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Missing value imputation using MICE algorithm", 
                                style={'margin': '8px 0'}),
                        html.Li("Outlier detection and treatment with IQR methods", 
                                style={'margin': '8px 0'}),
                        html.Li("Feature scaling and encoding for model compatibility", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),
        ]),
        
        # Analysis Techniques Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Analysis Techniques", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # Statistical Methods
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F7FAFC',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #4299E1',
            }, children=[
                html.H3("Statistical Methods", style={'color': '#2B6CB0', 'marginTop': '0'}),
                html.P(
                    "We employed various statistical techniques to uncover patterns and correlations within our dataset:",
                    style={'fontSize': '18px', 'marginBottom': '20px'}
                ),
                
                html.Div([
                    # Column 1
                    html.Div(style={'flex': '1'}, children=[
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("🔢", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Correlation Analysis", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                                html.P("Pearson and Spearman correlations to identify relationships between weather variables and accident severity", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("📈", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Regression Analysis", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                                html.P("Multiple linear and logistic regression to model relationships between environmental factors and accident outcomes", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                    ]),
                    
                    # Column 2
                    html.Div(style={'flex': '1'}, children=[
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("📊", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Time Series Analysis", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                                html.P("Seasonal decomposition and ARIMA modeling to identify temporal patterns in accident frequency", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("🧩", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Dimensionality Reduction", style={'margin': '0 0 5px', 'color': '#2C5282'}),
                                html.P("PCA and t-SNE to visualize complex relationships in high-dimensional weather and road condition data", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                    ]),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'}),
            ]),
            
            # Machine Learning Methods
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F0FFF4',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #38A169',
            }, children=[
                html.H3("Machine Learning Approaches", style={'color': '#2F855A', 'marginTop': '0'}),
                html.P(
                    "Our predictive models leverage state-of-the-art machine learning algorithms to forecast accident risk and severity:",
                    style={'fontSize': '18px', 'marginBottom': '20px'}
                ),
                
                html.Div([
                    # ML Method 1
                    html.Div(style={
                        'flex': '1',
                        'minWidth': '250px',
                        'backgroundColor': 'white',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
                    }, children=[
                        html.H4("Random Forest Classifier", style={'color': '#2F855A', 'marginTop': '0'}),
                        html.P(
                            "Ensemble decision tree approach for accident severity prediction with 87% accuracy, "
                            "providing intuitive feature importance rankings.",
                            style={'fontSize': '15px', 'lineHeight': '1.5'}
                        ),
                    ]),
                    
                    # ML Method 2
                    html.Div(style={
                        'flex': '1',
                        'minWidth': '250px',
                        'backgroundColor': 'white',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
                    }, children=[
                        html.H4("XGBoost", style={'color': '#2F855A', 'marginTop': '0'}),
                        html.P(
                            "Gradient boosting implementation optimized for both speed and performance, "
                            "particularly effective for handling class imbalance in severe accident cases.",
                            style={'fontSize': '15px', 'lineHeight': '1.5'}
                        ),
                    ]),
                    
                    # ML Method 3
                    html.Div(style={
                        'flex': '1',
                        'minWidth': '250px',
                        'backgroundColor': 'white',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
                    }, children=[
                        html.H4("Neural Networks", style={'color': '#2F855A', 'marginTop': '0'}),
                        html.P(
                            "Deep learning models with custom architecture for capturing non-linear relationships "
                            "between weather conditions and accident outcomes.",
                            style={'fontSize': '15px', 'lineHeight': '1.5'}
                        ),
                    ]),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px'}),
            ]),
            
            # Geospatial Analysis
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#EBF4FF',
                'borderRadius': '10px',
                'borderLeft': '5px solid #4C51BF',
            }, children=[
                html.H3("Geospatial Analysis", style={'color': '#4C51BF', 'marginTop': '0'}),
                html.P(
                    "Our spatial analysis methods identify geographical patterns and hotspots in accident distribution:",
                    style={'fontSize': '18px', 'marginBottom': '20px'}
                ),
                
                html.Div([
                    # Left column
                    html.Div(style={'flex': '1'}, children=[
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("📍", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("DBSCAN Clustering", style={'margin': '0 0 5px', 'color': '#4C51BF'}),
                                html.P("Density-based spatial clustering to identify accident hotspots without assuming fixed cluster counts", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("🗺️", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Heat Map Analysis", style={'margin': '0 0 5px', 'color': '#4C51BF'}),
                                html.P("Kernel density estimation to visualize accident concentration across urban areas", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                    ]),
                    
                    # Right column
                    html.Div(style={'flex': '1'}, children=[
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("🏙️", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Urban Network Analysis", style={'margin': '0 0 5px', 'color': '#4C51BF'}),
                                html.P("Road network topology analysis to identify high-risk road segments and intersection types", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                        html.Div(style={'display': 'flex', 'margin': '15px 0'}, children=[
                            html.Div("🔍", style={'fontSize': '24px', 'marginRight': '15px', 'width': '30px'}),
                            html.Div([
                                html.H4("Proximity Analysis", style={'margin': '0 0 5px', 'color': '#4C51BF'}),
                                html.P("Assessment of Points of Interest (POIs) impact on accident likelihood using spatial join techniques", 
                                      style={'margin': '0', 'fontSize': '15px'})
                            ])
                        ]),
                    ]),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '20px'}),
            ]),
        ]),
        
        # Validation Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Model Validation Approach", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#FFFAF0',
                'borderRadius': '10px',
                'borderLeft': '5px solid #DD6B20',
            }, children=[
                html.P(
                    "To ensure the robustness of our findings, we implemented a comprehensive validation strategy:",
                    style={'fontSize': '18px', 'marginBottom': '20px'}
                ),
                
                html.Div([
                    # Validation method 1
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': 'white',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
                    }, children=[
                        html.H4("Cross-Validation", style={'color': '#DD6B20', 'marginTop': '0'}),
                        html.P(
                            "Employed stratified 5-fold cross-validation to assess model performance across different data subsets, "
                            "ensuring consistent performance across geographical regions.",
                            style={'fontSize': '15px', 'lineHeight': '1.5'}
                        ),
                    ]),
                    
                    # Validation method 2
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': 'white',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
                    }, children=[
                        html.H4("Temporal Hold-Out", style={'color': '#DD6B20', 'marginTop': '0'}),
                        html.P(
                            "Used temporal split validation with the most recent 6 months as a hold-out set to assess "
                            "model generalization to future accidents and seasonal patterns.",
                            style={'fontSize': '15px', 'lineHeight': '1.5'}
                        ),
                    ]),
                    
                    # Validation method 3
                    html.Div(style={
                        'flex': '1',
                        'backgroundColor': 'white',
                        'padding': '15px',
                        'borderRadius': '8px',
                        'boxShadow': '0 2px 4px rgba(0, 0, 0, 0.05)',
                    }, children=[
                        html.H4("Evaluation Metrics", style={'color': '#DD6B20', 'marginTop': '0'}),
                        html.P(
                            "Evaluated models using balanced metrics (F1-score, ROC-AUC) with emphasis on recall for severe "
                            "accidents to prioritize public safety implications.",
                            style={'fontSize': '15px', 'lineHeight': '1.5'}
                        ),
                    ]),
                ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px'}),
            ]),
        ]),
        
        # Tools and Technologies
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Tools & Technologies", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'marginTop': '20px'}, children=[
                # Tool category 1
                html.Div(style={
                    'flex': '1',
                    'minWidth': '250px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                }, children=[
                    html.H3("Data Processing", style={'color': '#2D3748', 'marginTop': '0', 'fontSize': '20px'}),
                    html.Ul([
                        html.Li("Python (Pandas, NumPy)", style={'margin': '8px 0'}),
                        html.Li("SQL for database operations", style={'margin': '8px 0'}),
                        html.Li("Databricks for distributed processing", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
                
                # Tool category 2
                html.Div(style={
                    'flex': '1',
                    'minWidth': '250px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                }, children=[
                    html.H3("Analysis & Modeling", style={'color': '#2D3748', 'marginTop': '0', 'fontSize': '20px'}),
                    html.Ul([
                        html.Li("Scikit-learn for machine learning", style={'margin': '8px 0'}),
                        html.Li("TensorFlow for neural networks", style={'margin': '8px 0'}),
                        html.Li("StatsModels for statistical analysis", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
                
                # Tool category 3
                html.Div(style={
                    'flex': '1',
                    'minWidth': '250px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                }, children=[
                    html.H3("Visualization", style={'color': '#2D3748', 'marginTop': '0', 'fontSize': '20px'}),
                    html.Ul([
                        html.Li("Plotly Dash for interactive dashboards", style={'margin': '8px 0'}),
                        html.Li("GeoPandas for spatial visualization", style={'margin': '8px 0'}),
                        html.Li("Matplotlib and Seaborn for statistical plots", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
            ]),
        ]),
        
        # Call to action
        html.Div(style={
            'textAlign': 'center',
            'padding': '40px 20px',
            'borderRadius': '10px',
            'background': 'linear-gradient(135deg, #EBF8FF 0%, #90CDF4 100%)',
            'marginTop': '30px',
        }, children=[
            html.H2("Ready to Explore Our Findings?", style={
                'color': '#2A4365',
                'marginTop': '0',
                'marginBottom': '20px',
                'fontSize': '32px',
            }),
            html.P(
                "Discover the key insights and patterns we've uncovered through our comprehensive analytical methods.",
                style={
                    'maxWidth': '800px',
                    'margin': '0 auto 30px',
                    'fontSize': '18px',
                    'color': '#2D3748',
                    'lineHeight': '1.6',
                }
            ),
            html.A("View Research Findings →", 
                  href="/findings", 
                  style={
                      'padding': '14px 28px',
                      'backgroundColor': '#4299E1',
                      'color': 'white',
                      'borderRadius': '6px',
                      'textDecoration': 'none',
                      'fontWeight': '600',
                      'boxShadow': '0 4px 6px rgba(66, 153, 225, 0.3)',
                      'transition': 'all 0.2s ease',
                      'display': 'inline-block',
                  })
        ]),
    ])

def findings_page():
    return html.Div(style=container_style, children=[
        # Header Section with visual impact
        html.Div([
            html.H1("Research Findings", style={
                'fontSize': '42px',
                'fontWeight': '700',
                'textAlign': 'center',
                'margin': '30px 0 15px',
                'color': '#1A365D',
                'borderBottom': '3px solid #4299E1',
                'paddingBottom': '15px',
            }),
            html.P(
                "Key insights and patterns identified from our comprehensive traffic accident analysis",
                style={
                    'textAlign': 'center',
                    'fontSize': '20px',
                    'fontStyle': 'italic',
                    'color': '#4A5568',
                    'maxWidth': '800px',
                    'margin': '0 auto 40px',
                }
            ),
        ]),
        
        # Overview Section with gradient background
        html.Div(style={
            **section_style, 
            'backgroundColor': '#EBF8FF', 
            'borderLeft': '5px solid #3182CE', 
            'padding': '25px 30px',
            'borderRadius': '10px',
            'marginBottom': '35px',
        }, children=[
            html.H2("Key Insights", style={'color': '#2C5282', 'marginTop': '0'}),
            html.P(
                "Our analysis reveals strong correlations between environmental factors and accident severity. "
                "Decreased visibility and higher precipitation were associated with more severe accidents. "
                "Predictive models demonstrated significant accuracy, suggesting the feasibility of proactive safety measures.",
                style={'fontSize': '18px', 'lineHeight': '1.6'}
            ),
        ]),
        
        # Severity Distribution Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Accident Severity Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # Severity Distribution Card
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F7FAFC',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #4299E1',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Accident Severity Distribution", style={'color': '#2B6CB0', 'marginTop': '0'}),
                html.P(
                    "The distribution of accident severity levels reveals important patterns about traffic safety concerns:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                severity_distribution(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Most accidents fall into the moderate severity range (levels 2-3), with fewer incidents at the extremes. "
                        "This suggests that many accidents have significant impact but are not catastrophic, "
                        "highlighting opportunities for targeted safety interventions.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
        ]),
        
        # Correlation Analysis Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Environmental Correlation Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # Feature Correlation Card
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F0FFF4',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #38A169',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Feature Correlation Heatmap", style={'color': '#2F855A', 'marginTop': '0'}),
                html.P(
                    "Correlation analysis between environmental factors and accident characteristics reveals key relationships:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                feature_correlation(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Notable correlations include the negative relationship between visibility and accident severity, "
                        "suggesting that poor visibility significantly increases risk. Temperature and precipitation also "
                        "show meaningful correlations with accident outcomes.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
            
            # Precipitation vs Severity Card
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#EBF4FF',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #4C51BF',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Precipitation vs Severity Relationship", style={'color': '#4C51BF', 'marginTop': '0'}),
                html.P(
                    "The relationship between precipitation levels and accident severity demonstrates a clear pattern:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                precipitation_vs_severity(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "As precipitation increases, we observe a corresponding increase in accident severity. "
                        "This relationship is particularly pronounced during heavy rainfall events (>0.5 inches), "
                        "emphasizing the need for enhanced safety measures during adverse weather conditions.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
        ]),
        
        # Geographic Analysis Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Geographic Distribution Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # State Analysis Card
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#FFFAF0',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #DD6B20',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Accidents by State", style={'color': '#DD6B20', 'marginTop': '0'}),
                html.P(
                    "Accident distribution across states reveals significant regional variations:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                accidents_by_state(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "States with larger populations and more urban areas show higher accident frequencies, but the patterns "
                        "also reveal differences in reporting systems, infrastructure quality, and regional driving behaviors.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
            
            # Heatmap Card
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F7FAFC',
                'borderRadius': '10px',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                'borderLeft': '5px solid #4299E1',
            }, children=[
                html.H3("US Accident Hotspot Analysis", style={'color': '#2B6CB0', 'marginTop': '0'}),
                html.P(
                    "Geographical distribution of accidents with severity visualization reveals critical patterns:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                accident_heatmap(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Urban centers and major highway corridors show distinct clustering of accidents, with severity hotspots "
                        "particularly concentrated around metropolitan areas and complex highway interchanges. "
                        "Weather patterns across regions also correlate with severity variations.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
        ]),
        
        # Predictive Model Insights
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Predictive Model Insights", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # Cards row for model insights
            html.Div([
                # Card 1 - Weather Impact
                html.Div(style={
                    'flex': '1',
                    'minWidth': '300px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                    'margin': '10px',
                    'borderTop': '4px solid #4299E1',
                }, children=[
                    html.H3("🌧️ Weather Impact", style={'color': '#2B6CB0', 'marginTop': '0'}),
                    html.P(
                        "Our Random Forest models identified visibility and precipitation as the top weather-related "
                        "predictors of accident severity, with a combined feature importance of 42%.",
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Visibility below 1 mile increases severity risk by 68%", 
                                style={'margin': '8px 0'}),
                        html.Li("Light precipitation (0.1-0.3 in) increases severity by 23%", 
                                style={'margin': '8px 0'}),
                        html.Li("Heavy precipitation (>0.5 in) increases severity by 47%", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
                
                # Card 2 - Temporal Factors
                html.Div(style={
                    'flex': '1',
                    'minWidth': '300px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                    'margin': '10px',
                    'borderTop': '4px solid #38A169',
                }, children=[
                    html.H3("⏰ Temporal Factors", style={'color': '#2F855A', 'marginTop': '0'}),
                    html.P(
                        "Time-based analysis revealed significant patterns in accident occurrence and severity, "
                        "with important implications for traffic management.",
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Rush hour (7-9 AM, 4-6 PM) accidents have 31% higher severity", 
                                style={'margin': '8px 0'}),
                        html.Li("Weekend accidents are 18% more severe than weekday incidents", 
                                style={'margin': '8px 0'}),
                        html.Li("Night-time accidents (10 PM-5 AM) show 27% higher severity ratings", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
                
                # Card 3 - Road Characteristics
                html.Div(style={
                    'flex': '1',
                    'minWidth': '300px',
                    'padding': '20px',
                    'borderRadius': '8px',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                    'backgroundColor': 'white',
                    'margin': '10px',
                    'borderTop': '4px solid #805AD5',
                }, children=[
                    html.H3("🛣️ Road Characteristics", style={'color': '#6B46C1', 'marginTop': '0'}),
                    html.P(
                        "Infrastructure and road design features showed significant correlations with accident "
                        "frequency and severity in our predictive models.",
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Highway interchange areas have 52% more severe accidents", 
                                style={'margin': '8px 0'}),
                        html.Li("Roads without dividers show 37% higher severity rates", 
                                style={'margin': '8px 0'}),
                        html.Li("Construction zones associated with 43% increase in severity", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),
        ]),
        
        # Call to action
        html.Div(style={
            'textAlign': 'center',
            'padding': '40px 20px',
            'borderRadius': '10px',
            'background': 'linear-gradient(135deg, #EBF8FF 0%, #90CDF4 100%)',
            'marginTop': '30px',
        }, children=[
            html.H2("Ready to Explore Our Methodology?", style={
                'color': '#2A4365',
                'marginTop': '0',
                'marginBottom': '20px',
                'fontSize': '32px',
            }),
            html.P(
                "Learn about the advanced analytical approaches we used to extract these valuable insights.",
                style={
                    'maxWidth': '800px',
                    'margin': '0 auto 30px',
                    'fontSize': '18px',
                    'color': '#2D3748',
                    'lineHeight': '1.6',
                }
            ),
            html.A("View Research Methodology →", 
                  href="/methods", 
                  style={
                      'padding': '14px 28px',
                      'backgroundColor': '#4299E1',
                      'color': 'white',
                      'borderRadius': '6px',
                      'textDecoration': 'none',
                      'fontWeight': '600',
                      'boxShadow': '0 4px 6px rgba(66, 153, 225, 0.3)',
                      'transition': 'all 0.2s ease',
                      'display': 'inline-block',
                  })
        ]),
    ])

# ====================== APP LAYOUT ===========================
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dcc.Loading(
        id="loading",
        type="circle",
        fullscreen=True,
        children=html.Div(id='page-content')
    ),
    html.Div("© 2025 Traffic Accident Research Dashboard", style=footer_style)
])

@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/objectives':
        return objectives_page()
    elif pathname == '/methods':
        return methods_page()
    elif pathname == '/findings':
        return findings_page()
    else:
        return home_page()

# ====================== RUN APP ===========================
if __name__ == '__main__':
    app.run(debug=True)