from dash import html, Input, Output, State, callback
from styles.styles import container_style, section_style

# Update import to use analysis module with new specialized findings visualizations
from visuals.analysis import (
    # Basic visualizations
    severity_distribution,
    feature_correlation,
    precipitation_vs_severity,
    accident_heatmap,
    
    # Findings-specific visualizations
    severity_by_weather_conditions,
    accident_time_analysis,
    severity_by_road_feature,
    highway_severity_analysis,
    weather_condition_counts,
    predictive_feature_importance,
    accidents_by_month,
    model_performance_visualization,
    generate_risk_map_visualization
)

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
    html.H2("Key Insights Summary", style={'color': '#2C5282', 'marginTop': '0'}),
    html.P(
        "Our comprehensive analysis of 7.7 million traffic accidents revealed several critical findings:",
        style={'fontSize': '18px', 'marginBottom': '20px'}
    ),
    html.Ul([
        html.Li([
            html.Strong("Environmental impacts on safety: "), 
            "Pressure, temperature, and humidity emerge as the most influential environmental factors, with significant correlations to accident severity."
        ], style={'margin': '10px 0', 'fontSize': '16px'}),
        html.Li([
            html.Strong("Model Performance: "), 
            "Random Forest models demonstrated varying performance between balanced and non-balanced datasets, with accuracy ranging from 62% to 74%."
        ], style={'margin': '10px 0', 'fontSize': '16px'}),
        html.Li([
            html.Strong("Feature Importance: "), 
            "The top three features (Pressure, Temperature, Humidity) account for the majority of the model's predictive capability."
        ], style={'margin': '10px 0', 'fontSize': '16px'}),
        html.Li([
            html.Strong("Severity Distribution: "), 
            "Most accidents fall into the moderate severity range (levels 2-3), with severity level 2 accounting for approximately 70% of recorded incidents."
        ], style={'margin': '10px 0', 'fontSize': '16px'}),
    ], style={'paddingLeft': '20px', 'color': '#2D3748'})
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
                        "Severity level 2 accounts for approximately 70% of all recorded incidents, indicating that most accidents "
                        "cause moderate disruptions to traffic flow rather than severe consequences. This suggests targeted "
                        "interventions could have significant impact on the most common accident types.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
            
            # NEW: Model Confusion Matrix Card
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#EBF8FF',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #3182CE',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Severity Prediction Accuracy", style={'color': '#2B6CB0', 'marginTop': '0'}),
                html.P(
                    "Our machine learning models can effectively predict accident severity level based on environmental and road factors:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                model_performance_visualization(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "The confusion matrix demonstrates our model's strong predictive capabilities, "
                        "correctly identifying severity levels with high accuracy. This predictive power "
                        "enables proactive safety measures and resource allocation based on forecasted risk levels.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
        ]),
        
        # Weather and Environmental Factors Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Weather & Environmental Factor Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # NEW: Weather Condition Counts
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F0F9FF',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #63B3ED',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Most Common Weather Conditions in Accidents", style={'color': '#3182CE', 'marginTop': '0'}),
                html.P(
                    "Analysis of weather conditions present during accidents reveals important patterns:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                weather_condition_counts(),
            ]),
            
            # NEW: Severity by Weather Conditions
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F0FFF4',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #38A169',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Weather Impact on Severity", style={'color': '#2F855A', 'marginTop': '0'}),
                html.P(
                    "Different weather conditions show distinct patterns in accident severity distribution:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                severity_by_weather_conditions(),
                html.Div(style={'marginTop': '15px'}, children=[
                html.P(
                    "While most accidents occur during clear or fair weather, adverse conditions such as light snow, overcast skies, "
                    "and fog show noticeably higher proportions of severe accidents (Severity 3 and 4). These patterns suggest that "
                    "even though rare, poor weather significantly increases accident severity. This underlines the importance of "
                    "weather-responsive safety policies and heightened driver caution during these conditions. ",
                    style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                ),
                html.P(
                    "Interestingly, clear, overcast, and scattered cloud conditions are associated with the most severe accidents overall, "
                    "not necessarily because they are more dangerous, but because they occur more often. In contrast, rain and snow may prompt "
                    "drivers to slow down and drive more cautiously, reducing the severity of accidents despite the riskier road conditions.",
                    style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                )
             ])
            ]),
            
            
        ]),
        
        # Road Infrastructure Analysis
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Road Infrastructure Impact", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # NEW: Highway Severity Analysis
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F0FFF4',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #38A169',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Highway vs Non-Highway Accidents", style={'color': '#2F855A', 'marginTop': '0'}),
                html.P(
                    "Comparative analysis of accident severity on highways versus local roads:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                highway_severity_analysis()
            ]),
        ]),
        
        # Temporal Analysis Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Temporal Pattern Analysis", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # NEW: Time of Day Analysis
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#EBF8FF',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #3182CE',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Time of Day Impact", style={'color': '#2B6CB0', 'marginTop': '0'}),
                html.P(
                    "Analysis of how accident frequency and severity vary throughout the day:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                accident_time_analysis(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Morning and evening rush hours show dramatic spikes in accident frequency, with notable differences "
                        "in severity distribution. Peak commuting times (7-9 AM and 4-6 PM) represent critical periods for "
                        "traffic management and emergency service readiness.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
            
            # Monthly Accident Trend Analysis Section
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
                    "Interactive visualization of daily accident patterns across different months, with holiday markers:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                accidents_by_month(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Our temporal analysis reveals distinct patterns in accident frequency across different months and days. "
                        "Major holidays (Thanksgiving, Christmas, Independence Day) show significant spikes in accidents. "
                        "Many months also display cyclical patterns with weekend peaks and mid-week troughs, suggesting "
                        "day-of-week specific safety strategies could be effective.",
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
                    "Geographical distribution of accidents reveals critical patterns for targeted safety interventions:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                accident_heatmap(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "The heatmap visualization clearly identifies accident hotspots concentrated around major urban centers "
                        "and along key interstate corridors. The patterns reveal that accident density follows population centers "
                        "but also highlights specific high-risk corridors between urban areas. Eastern and Western coastal regions "
                        "show significantly higher accident densities compared to central parts of the country, correlating with "
                        "both population density and transportation network complexity.",
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
                html.H3("US Accident Risk Mapping", style={'color': '#2B6CB0', 'marginTop': '0'}),
                html.P(
                    "Geographical analysis of accident risk reveals critical safety insights:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                generate_risk_map_visualization(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "The risk map provides a nuanced visualization of accident severity across the United States. "
                        "By aggregating and color-coding locations based on the proportion of severe accidents, "
                        "we identify high-risk corridors and urban centers. The analysis reveals that accident risk "
                        "is not uniformly distributed, with certain geographic regions showing significantly higher "
                        "proportions of severe accidents. These hotspots correlate with complex transportation networks, "
                        "urban density, and potentially challenging driving conditions.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
        ]),
        
            
            # Predictive Model Insights
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
                    html.H3("Environmental Impact", style={'color': '#2B6CB0', 'marginTop': '0'}),
                    html.P(
                        "Our Random Forest models revealed that atmospheric conditions significantly influence accident severity, with pressure, temperature, and humidity emerging as key predictors."
                        ,
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Pressure shows the highest feature importance in predicting accident severity", 
                                style={'margin': '8px 0'}),
                        html.Li("Temperature ranks as the second most influential environmental factor", 
                                style={'margin': '8px 0'}),
                        html.Li("Humidity demonstrates a notable correlation with accident characteristics", 
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
                    html.H3("Temporal Analysis", style={'color': '#2F855A', 'marginTop': '0'}),
                    html.P(
                        "Time-based analysis reveals critical patterns in accident occurrence and severity across different periods."
                        ,
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Peak commuting hours (7-9 AM and 4-6 PM) show highest accident frequencies", 
                                style={'margin': '8px 0'}),
                        html.Li("Accident patterns demonstrate cyclical variations across days and months", 
                                style={'margin': '8px 0'}),
                        html.Li("Major holidays correlate with significant accident spikes", 
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
                    html.H3("Model Performance Insights", style={'color': '#6B46C1', 'marginTop': '0'}),
                    html.P(
                        "Our predictive models demonstrate nuanced performance across different dataset configurations."
                        ,
                        style={'lineHeight': '1.6'}
                    ),
                    html.Ul([
                        html.Li("Non-balanced dataset accuracy: 62%", 
                                style={'margin': '8px 0'}),
                        html.Li("Balanced dataset accuracy: 74%", 
                                style={'margin': '8px 0'}),
                        html.Li("Variations highlight the complexity of predicting accident severity", 
                                style={'margin': '8px 0'}),
                    ], style={'paddingLeft': '20px', 'color': '#4A5568'})
                ]),
            ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-between'}),
        

        
        # Conclusions Section
            html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
                html.H2("Research Conclusions", style={
                    'color': '#2D3748', 
                    'borderBottom': '2px solid #E2E8F0', 
                    'paddingBottom': '10px'
                }),
                
                html.Div(style={
                    'padding': '25px',
                    'backgroundColor': '#FFFCEB',
                    'borderRadius': '10px',
                    'marginBottom': '25px',
                    'borderLeft': '5px solid #ECC94B',
                    'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
                }, children=[
                    html.H3("Key Takeaways", style={'color': '#B7791F', 'marginTop': '0'}),
                    html.P(
                        "Our comprehensive analysis of 7.7 million traffic accidents reveals critical insights into road safety:",
                        style={'fontSize': '16px', 'marginBottom': '20px'}
                    ),
                    html.Ol([
                        html.Li([
                            html.Strong("Severity Distribution: "), 
                            html.Span("Most accidents fall in the moderate severity range (Level 2), accounting for approximately 70% of incidents. This suggests that targeted interventions could significantly impact the most common accident types.")
                        ], style={'margin': '12px 0', 'fontSize': '16px'}),
                        html.Li([
                            html.Strong("Environmental Influences: "), 
                            html.Span("Weather conditions play a crucial role in accident dynamics. While clear weather accounts for 46.5% of accidents, adverse conditions like light snow and fog show disproportionately higher severe accident rates.")
                        ], style={'margin': '12px 0', 'fontSize': '16px'}),
                        html.Li([
                            html.Strong("Temporal Patterns: "), 
                            html.Span("Rush hours (7-9 AM and 4-6 PM) demonstrate significant accident spikes, highlighting critical periods for traffic management and emergency preparedness.")
                        ], style={'margin': '12px 0', 'fontSize': '16px'}),
                        html.Li([
                            html.Strong("Geographical Insights: "), 
                            html.Span("Accident density correlates strongly with urban centers and interstate corridors, with Eastern and Western coastal regions showing substantially higher accident concentrations.")
                        ], style={'margin': '12px 0', 'fontSize': '16px'}),
                        html.Li([
                            html.Strong("Predictive Modeling: "), 
                            html.Span("Random Forest models revealed nuanced performance, with accuracies ranging from 62% to 74%. Pressure, temperature, and humidity emerged as the most influential predictive features.")
                        ], style={'margin': '12px 0', 'fontSize': '16px'}),
                    ], style={'paddingLeft': '20px', 'color': '#2D3748'})
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
                        "Dive deeper into the advanced analytical approaches used to extract these valuable insights.",
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
                ])
            ])
    ])