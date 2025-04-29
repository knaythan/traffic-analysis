from dash import dcc, html
from pages import home, objectives, methods, findings
from dash import Dash, callback, Input, Output
from components.navbar import navbar
from styles.styles import footer_style

# Set up app and data
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

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
        return objectives.page()
    elif pathname == '/methods':
        return methods.page()
    elif pathname == '/findings':
        return findings.page()
    else:
        return home.page()

# ====================== RUN APP ===========================
if __name__ == '__main__':
    app.run(debug=True)