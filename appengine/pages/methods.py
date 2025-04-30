from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

# Import styles and components
from styles.styles import container_style, section_style
from components.navbar import navbar

# Import visualization functions
from visuals.analysis import (
    severity_distribution,
    feature_correlation,
    precipitation_vs_severity,
    accidents_by_state,
    accident_heatmap,
    weather_impact_analysis,
    highway_feature_importance,
    road_feature_chi_square,
    model_performance_comparison
)

def page():
    """
    Renders the methodology page with sections describing the research approach,
    data processing, analysis techniques, and model validation.
    """
    return html.Div(style=container_style, children=[
        # Header Section
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
        
        # Overview Section
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
                        html.Li("Missing value imputation using KNN algorithm", 
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
                
                # Statistical methods visualization
                html.Div([
                    feature_correlation(),
                    html.Div(style={'height': '30px'}),  # Spacer
                    weather_impact_analysis()
                ])
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
                
                # ML methods visualization
                html.Div([
                    highway_feature_importance(),
                    html.Div(style={'height': '30px'}),  # Spacer
                    model_performance_comparison()
                ])
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
                
                # Geospatial visualization
                html.Div([
                    accident_heatmap()
                ])
            ]),
        ]),
        
        # Exploratory Data Analysis Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Exploratory Data Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#FFF5F7',
                'borderRadius': '10px',
                'borderLeft': '5px solid #D53F8C',
            }, children=[
                html.P(
                    "Our exploratory analysis revealed key patterns and distributions in the traffic accident data:",
                    style={'fontSize': '18px', 'marginBottom': '20px'}
                ),
                
                # EDA visualizations
                html.Div([
                    severity_distribution(),
                    html.Div(style={'height': '30px'}),  # Spacer
                    precipitation_vs_severity(),
                    html.Div(style={'height': '30px'}),  # Spacer
                    accidents_by_state()
                ])
            ]),
        ]),
        
        # Categorical Features Analysis Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Categorical Features Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#FFF8F0',
                'borderRadius': '10px',
                'borderLeft': '5px solid #DD6B20',
            }, children=[
                html.P(
                    "We analyzed how categorical road features affect accident severity using Chi-Square analysis:",
                    style={'fontSize': '18px', 'marginBottom': '20px'}
                ),
                
                # Categorical features visualization
                html.Div([
                    road_feature_chi_square()
                ])
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
                        html.Li("Google BigQuery for data storage", style={'margin': '8px 0'}),
                        html.Li("Scikit-learn for preprocessing", style={'margin': '8px 0'}),
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
                        html.Li("SciPy for statistical analysis", style={'margin': '8px 0'}),
                        html.Li("XGBoost for gradient boosting", style={'margin': '8px 0'}),
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
                        html.Li("Folium for geospatial visualization", style={'margin': '8px 0'}),
                        html.Li("Matplotlib and Seaborn for statistical plots", style={'margin': '8px 0'}),
                        html.Li("Plotly Express for interactive charts", style={'margin': '8px 0'}),
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