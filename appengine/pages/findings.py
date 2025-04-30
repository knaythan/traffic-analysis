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
    model_confusion_matrix,
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
                    "Reduced visibility and precipitation significantly affect accident severity, with visibility showing a moderate negative correlation with humidity (-0.41)."
                ], style={'margin': '10px 0', 'fontSize': '16px'}),
                html.Li([
                    html.Strong("Infrastructure significance: "), 
                    "Road features like traffic signals, junctions and highway characteristics showed strong statistical associations with accident outcomes, suggesting infrastructure improvements could have substantial safety benefits."
                ], style={'margin': '10px 0', 'fontSize': '16px'}),
                html.Li([
                    html.Strong("Geographic patterns: "), 
                    "California, Florida, and Texas experience the highest accident volumes, with urban centers showing distinct accident hotspots regardless of region."
                ], style={'margin': '10px 0', 'fontSize': '16px'}),
                html.Li([
                    html.Strong("Predictive modeling success: "), 
                    "Our machine learning approaches achieved up to 89% accuracy in predicting severity outcomes, with gradient boosting methods performing particularly well."
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
                model_confusion_matrix(),
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
                        "While clear weather accounts for the majority of accidents overall, adverse conditions like "
                        "heavy rain, fog, and snow show higher proportions of severe accidents. This highlights the need "
                        "for weather-specific safety interventions and driver awareness campaigns.",
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
            
            # NEW: Severity by Road Feature
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#FFF5F7',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #D53F8C',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Road Features Impact on Severity", style={'color': '#B83280', 'marginTop': '0'}),
                html.P(
                    "Analysis of how different road features affect the severity of traffic accidents:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                severity_by_road_feature(),
                html.Div(style={'marginTop': '15px'}, children=[
                    html.P(
                        "Certain road features consistently increase accident severity, with junctions, railway crossings, and "
                        "traffic signals showing the strongest effects. Understanding these relationships enables targeted "
                        "infrastructure improvements that could significantly reduce accident severity.",
                        style={'fontSize': '15px', 'fontStyle': 'italic', 'color': '#4A5568', 'lineHeight': '1.5'}
                    )
                ])
            ]),
            
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
        
        # Predictive Modeling Section
        html.Div(style={**section_style, 'marginBottom': '35px'}, children=[
            html.H2("Predictive Model Insights", style={
                'color': '#2D3748', 
                'borderBottom': '2px solid #E2E8F0', 
                'paddingBottom': '10px'
            }),
            
            # NEW: Predictive Feature Importance
            html.Div(style={
                'padding': '25px',
                'backgroundColor': '#F0FFF4',
                'borderRadius': '10px',
                'marginBottom': '25px',
                'borderLeft': '5px solid #38A169',
                'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)',
            }, children=[
                html.H3("Key Factors Driving Accident Severity", style={'color': '#2F855A', 'marginTop': '0'}),
                html.P(
                    "Our machine learning models identified the most influential factors for accident severity:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                predictive_feature_importance()
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
                    "Our comprehensive analysis yielded several important conclusions with significant implications for traffic safety:",
                    style={'fontSize': '16px', 'marginBottom': '20px'}
                ),
                html.Ol([
                    html.Li([
                        html.Strong("Multi-factor accident causality: "), 
                        html.Span("Our analysis confirms that traffic accidents stem from complex interactions between weather conditions, road infrastructure, "
                        "temporal factors, and geographical variables. Effective prevention strategies must address multiple risk factors simultaneously.")
                    ], style={'margin': '12px 0', 'fontSize': '16px'}),
                    html.Li([
                        html.Strong("Predictable risk patterns: "), 
                        html.Span("The high accuracy of our predictive models (up to 89%) demonstrates that accident severity follows predictable patterns. "
                        "This suggests that targeted interventions based on identified risk factors could significantly reduce both accident frequency and severity.")
                    ], style={'margin': '12px 0', 'fontSize': '16px'}),
                    html.Li([
                        html.Strong("Infrastructure impact: "), 
                        html.Span("Road design elements (junctions, traffic signals, highway interchanges) showed stronger associations with accident severity than weather conditions. "
                        "This indicates that infrastructure improvements may offer more reliable safety benefits than weather-dependent interventions.")
                    ], style={'margin': '12px 0', 'fontSize': '16px'}),
                    html.Li([
                        html.Strong("Temporal targeting opportunity: "), 
                        html.Span("The clear temporal patterns identified in accident frequency and severity (time of day, day of week, holidays) provide a framework "
                        "for more efficient resource allocation in traffic safety initiatives and emergency response planning.")
                    ], style={'margin': '12px 0', 'fontSize': '16px'}),
                ], style={'paddingLeft': '20px', 'color': '#2D3748'})
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