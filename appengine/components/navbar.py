from dash import dcc, html
from styles.styles import navbar_style, link_style

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