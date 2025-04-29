from dash import html, Input, Output, State, callback
from styles.styles import container_style, section_style
from visuals.analysis import *

def page():
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
        
                # Monthly Accident Trend Analysis Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Monthly Accident Trend Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#EDF2F7',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #63B3ED',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Daily Accident Trends by Month", style={'color': '#3182CE', 'marginTop': '0'}),
                html.P(
                    "This interactive visualization allows you to explore how accident frequencies vary day-by-day across different months. "
                    "Use the dropdown menu to select a specific month or view all months combined for comparison.",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                accidents_by_month(),  # <-- Your new function here
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Analysis reveals noticeable spikes during holidays, weekends, and at month beginnings/endings. "
                        "Understanding these patterns can help inform better traffic management and public safety campaigns.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
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