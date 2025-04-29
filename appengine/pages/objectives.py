from dash import dcc, html
from styles.styles import container_style, section_style
from components.navbar import navbar

def page():
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