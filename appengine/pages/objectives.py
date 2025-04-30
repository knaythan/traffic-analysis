from dash import dcc, html
from styles.styles import container_style, section_style
from components.navbar import navbar

def page():
    return html.Div(style=container_style, children=[
        # Header Section
        html.Div([
            html.H1("Research Objectives", style={
                'fontSize': '38px',
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
        
        # Research Objectives in card format - similar to Analysis Approach
        html.H2("Research Objectives", style={
            'textAlign': 'center', 
            'color': '#2D3748', 
            'marginBottom': '25px',
            'marginTop': '35px',
            'fontSize': '32px',
        }),
        
        html.Div(style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'gap': '25px',
            'marginBottom': '40px',
        }, children=[
            # Card 1 - Temporal Analysis
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
                    'backgroundColor': '#FEFCBF',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #F6E05E',
                }, children=[
                    html.H3("Temporal Analysis", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#744210',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Examining how accident patterns vary across different time periods to identify high-risk hours, days, and seasons.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Analyze accident frequencies by time of day and day of week", style={'margin': '8px 0'}),
                        html.Li("Examine relationship between accident duration and external factors", style={'margin': '8px 0'}),
                        html.Li("Study seasonal variations in accident severity", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 2 - Environmental Factors
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
                    html.H3("Environmental Factors", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#234E52',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Investigating how weather conditions and geographical context influence accident occurrence and severity.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Assess relationships between weather conditions and accident outcomes", style={'margin': '8px 0'}),
                        html.Li("Compare accident patterns between urban and rural areas", style={'margin': '8px 0'}),
                        html.Li("Identify geographical accident hotspots using spatial analysis", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 3 - Infrastructure Analysis
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
                    html.H3("Infrastructure Analysis", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#44337A',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Evaluating how road design, traffic control systems, and surrounding infrastructure affect accident risk.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Analyze impact of road characteristics on accident outcomes", style={'margin': '8px 0'}),
                        html.Li("Compare accident rates at different intersection types", style={'margin': '8px 0'}),
                        html.Li("Study effects of nearby Points of Interest on accident likelihood", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
        ]),
        
        # Research Methodology Section
        html.H2("Research Methodology", style={
            'textAlign': 'center', 
            'color': '#2D3748', 
            'marginBottom': '25px',
            'marginTop': '35px',
            'fontSize': '32px',
        }),
        
        html.Div(style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'gap': '25px',
            'marginBottom': '40px',
        }, children=[
            # Card 1 - Statistical Methods
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
                    'backgroundColor': '#FEF5E7',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #FDEBD0',
                }, children=[
                    html.H3("Statistical Methods", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#7D6608',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Applying rigorous statistical techniques to uncover significant relationships and validate observed patterns in the data.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Correlation Analysis for environmental variables", style={'margin': '8px 0'}),
                        html.Li("Time Series Decomposition for seasonal trends", style={'margin': '8px 0'}),
                        html.Li("Principal Component Analysis for dimension reduction", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 2 - Machine Learning Approaches
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
                    html.H3("Machine Learning", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#2C5282',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Leveraging advanced predictive models to forecast accident severity and identify the most influential risk factors.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Random Forest and XGBoost classifiers", style={'margin': '8px 0'}),
                        html.Li("Feature importance analysis for key factors", style={'margin': '8px 0'}),
                        html.Li("Ensemble methods for improved prediction accuracy", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 3 - Geospatial Analysis
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
                    'backgroundColor': '#FEEBC8',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #FBD38D',
                }, children=[
                    html.H3("Geospatial Analysis", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#7B341E',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Mapping and analyzing the spatial distribution of accidents to identify high-risk locations and underlying geographic patterns.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Geospatial clustering to identify hotspots", style={'margin': '8px 0'}),
                        html.Li("Interactive heatmap visualizations", style={'margin': '8px 0'}),
                        html.Li("Analysis of proximity to infrastructure elements", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
        ]),
        
        # Broader Impacts Section
        html.H2("Broader Impacts", style={
            'textAlign': 'center', 
            'color': '#2D3748', 
            'marginBottom': '25px',
            'marginTop': '35px',
            'fontSize': '32px',
        }),
        
        html.Div(style={
            'display': 'flex',
            'flexWrap': 'wrap',
            'justifyContent': 'center',
            'gap': '25px',
            'marginBottom': '40px',
        }, children=[
            # Card 1 - Emergency Services
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
                    'backgroundColor': '#FED7D7',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #FEB2B2',
                }, children=[
                    html.H3("Emergency Services", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#822727',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Supporting first responders with data-driven insights to optimize resource allocation and reduce response times in high-risk areas.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Predictive deployment of emergency vehicles", style={'margin': '8px 0'}),
                        html.Li("Risk-based resource allocation strategies", style={'margin': '8px 0'}),
                        html.Li("Temporal planning for high-risk periods", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 2 - Urban Planning
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
                    'backgroundColor': '#C6F6D5',
                    'padding': '25px 20px',
                    'borderBottom': '1px solid #9AE6B4',
                }, children=[
                    html.H3("Urban Planning", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#22543D',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Informing infrastructure development and road design to create safer transportation networks and reduce accident frequency.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Data-driven road safety improvements", style={'margin': '8px 0'}),
                        html.Li("Targeted infrastructure modifications", style={'margin': '8px 0'}),
                        html.Li("Risk-aware urban development planning", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
            
            # Card 3 - Autonomous Vehicles
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
                    html.H3("Autonomous Vehicles", style={
                        'margin': '0',
                        'textAlign': 'center',
                        'color': '#44337A',
                        'fontSize': '30px',
                    }),
                ]),
                # Card Body
                html.Div(style={
                    'padding': '25px 20px',
                }, children=[
                    html.P(
                        "Enhancing autonomous vehicle safety systems by providing data on high-risk scenarios and environmental conditions.",
                        style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
                    ),
                    html.Ul([
                        html.Li("Risk-aware navigation algorithms", style={'margin': '8px 0'}),
                        html.Li("Environmental hazard prediction", style={'margin': '8px 0'}),
                        html.Li("Temporal and spatial risk modeling", style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
                ]),
            ]),
        ]),
        
        # Summary statement
        html.Div(style={**section_style, 'backgroundColor': '#EBF8FF', 'borderLeft': '5px solid #3182CE', 'padding': '25px 30px', 'marginTop': '35px'}, children=[
            html.P(
                "This research has the potential to save lives by enabling data-driven policy decisions and technological innovations that address the most significant risk factors in traffic accidents.",
                style={'fontSize': '18px', 'lineHeight': '1.6', 'textAlign': 'center', 'fontWeight': '500', 'color': '#2C5282', 'margin': '0'}
            ),
        ]),
        
        # Call to action
        html.Div(style={'textAlign': 'center', 'marginTop': '40px', 'marginBottom': '30px'}, children=[
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