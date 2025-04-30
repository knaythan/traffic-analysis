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
                'fontSize': '60px',
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
                html.Div("7.0M+", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#2B6CB0'}),
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
                html.Div("25+", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#2F855A'}),
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
                html.Div("7 Years", style={'fontSize': '36px', 'fontWeight': '700', 'color': '#6B46C1'}),
                html.Div("Historical Data (February 2016 - March 2023)", style={'fontSize': '18px', 'color': '#4A5568', 'marginTop': '5px'}),
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
            html.H2("Project Significance", style={'color': '#2C5282', 'marginTop': '0', 'borderBottom': '2px solid #E2E8F0', 'paddingBottom': '10px'}),
            html.P(
            "Traffic accidents are a leading cause of injuries, fatalities, and economic losses in the United States, with millions of incidents occurring annually. "
            "This study provides critical insights to address these challenges by leveraging data-driven approaches to improve road safety, optimize emergency response, and inform urban planning.",
            style={'fontSize': '18px', 'lineHeight': '1.6', 'marginBottom': '20px'}
            ),
            html.Ul([
            html.Li("Enhancing Road Safety: Identifying environmental, temporal, and road-related factors that contribute to accidents enables targeted interventions, such as improved lighting, signage, and road design.", 
                style={'marginBottom': '10px'}),
            html.Li("Optimizing Emergency Response: Predictive models help emergency services allocate resources effectively, reducing response times and saving lives.", 
                style={'marginBottom': '10px'}),
            html.Li("Informing Urban Planning: Geospatial analysis highlights accident hotspots, guiding infrastructure improvements like safer intersections and traffic calming measures.", 
                style={'marginBottom': '10px'}),
            html.Li("Supporting Autonomous Vehicles: Insights into accident risk factors enhance navigation algorithms, improving the safety of autonomous systems.", 
                style={'marginBottom': '10px'}),
            html.Li("Promoting Data-Driven Policy: Policymakers can implement targeted regulations and infrastructure upgrades based on the study’s findings.", 
                style={'marginBottom': '10px'}),
            ], style={'paddingLeft': '20px', 'fontSize': '18px', 'lineHeight': '1.6'}),
            html.P(
            "By addressing these areas, this research lays the foundation for reducing accidents, saving lives, and creating safer, more efficient transportation systems.",
            style={'fontSize': '18px', 'lineHeight': '1.6'}
            ),
        ]),

        # Analysis Approach Section with cards
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
    # Card 1 - Statistical Analysis
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
            html.H3("Statistical Testing", style={
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
                "We applied rigorous statistical methods to validate relationships between variables and verify the significance of observed patterns in accident data.",
                style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("T-tests to compare means across groups", style={'margin': '8px 0'}),
                html.Li("Chi-square tests for categorical associations", style={'margin': '8px 0'}),
                html.Li("Correlation analysis between key features", style={'margin': '8px 0'}),
            ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
        ]),
    ]),
    
    # Card 2 - Predictive Modeling
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
            html.H3("Predictive Modeling", style={
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
                "Our machine learning approach focuses on predicting accident severity using multiple techniques, with feature importance analysis to identify key risk factors.",
                style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Random Forest classifier with feature importance", style={'margin': '8px 0'}),
                html.Li("NLP-based label modeling (experimental)", style={'margin': '8px 0'}),
                html.Li("Accident severity distribution analysis", style={'margin': '8px 0'}),
            ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
        ]),
    ]),
    
    # Card 3 - Spatiotemporal Analysis
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
            html.H3("Spatiotemporal Analysis", style={
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
                "By combining geospatial and temporal analyses, we identified how accident patterns vary across both location and time, revealing high-risk areas during specific time periods.",
                style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Interactive Folium heatmaps", style={'margin': '8px 0'}),
                html.Li("Hourly accident trend visualization", style={'margin': '8px 0'}),
                html.Li("Time of day and location correlation", style={'margin': '8px 0'}),
                html.Li("Geographic accident hotspot identification", style={'margin': '8px 0'}),
            ], style={'paddingLeft': '20px', 'color': '#4A5568', 'marginTop': '15px'})
        ]),
    ]),
    
    # Card 4 - Feature Analysis
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
            html.H3("Feature Analysis", style={
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
                "We identified the most influential factors in accident occurrence and severity through comprehensive feature analysis and correlation studies.",
                style={'lineHeight': '1.7', 'color': '#4A5568', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Feature importance from Random Forest", style={'margin': '8px 0'}),
                html.Li("Correlation heatmap visualization", style={'margin': '8px 0'}),
                html.Li("Multi-factor interaction analysis", style={'margin': '8px 0'}),
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