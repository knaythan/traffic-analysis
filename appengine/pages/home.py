from dash import dcc, html
from styles.styles import container_style, section_style
from components.navbar import navbar

def page():
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