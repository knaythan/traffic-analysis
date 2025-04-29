from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import folium
from folium.plugins import HeatMap
from google.cloud import bigquery
import os
import holidays
import datetime

client = bigquery.Client()
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = os.environ.get("DATASET_ID")
TABLE = os.environ.get("TABLE_ID")

PROJECT_ID = 'cs163-final-project' if PROJECT_ID is None else PROJECT_ID
DATASET = 'us_accident_data' if DATASET is None else DATASET
TABLE = 'us_accidents' if TABLE is None else TABLE

def severity_distribution():
    query = f"""
        SELECT Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    severity_counts = df["Severity"].value_counts().sort_index()
    fig = px.bar(x=severity_counts.index, y=severity_counts.values,
                 labels={'x': 'Severity Level', 'y': 'Number of Accidents'},
                 title='Accident Severity Distribution')
    return dcc.Graph(figure=fig)

 
def feature_correlation():
    query = f"""
        SELECT
            Severity,
            `Temperature_F_`,
            `Wind_Chill_F_`,
            `Humidity_%_`,
            `Pressure_in_`,
            `Visibility_mi_`,
            `Wind_Speed_mph_`,
            `Precipitation_in_`
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Severity IS NOT NULL
    """

    df = client.query(query).to_dataframe()
    corr_matrix = df.corr()
    fig = px.imshow(corr_matrix, text_auto=True,
                    color_continuous_scale='Viridis',
                    title='Feature Correlation Heatmap')
    return dcc.Graph(figure=fig)


def precipitation_vs_severity():
    query = f"""
        SELECT Precipitation_in_ AS Precipitation, Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Precipitation_in_ IS NOT NULL AND Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    fig = px.scatter(df, x="Precipitation", y="Severity", log_x=True,
                     title="Precipitation vs Severity (Log Scale)",
                     labels={"Precipitation": "Precipitation (in)", "Severity": "Severity"})
    return dcc.Graph(figure=fig)


def accidents_by_state():
    query = f"""
        SELECT State
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE State IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    state_counts = df["State"].value_counts().sort_values(ascending=False)
    fig = px.bar(x=state_counts.index, y=state_counts.values,
                 labels={'x': 'State', 'y': 'Number of Accidents'},
                 title='Accident Distribution by State')
    return dcc.Graph(figure=fig)


def accident_heatmap():
    query = f"""
        SELECT Start_Lat, Start_Lng
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Start_Lat IS NOT NULL AND Start_Lng IS NOT NULL
    """
    try:
        df = client.query(query).to_dataframe()
        
        heat_data = df[["Start_Lat", "Start_Lng"]].values.tolist()

        # 🔧 Add min_zoom and max_zoom here
        m = folium.Map(
            location=[37.8, -96],
            zoom_start=5,
            tiles="CartoDB Voyager",
            min_zoom=4,
            max_zoom=8  # prevents zooming too far in
        )

        HeatMap(heat_data, radius=2, blur=2, max_zoom=10).add_to(m)
        map_html = m.get_root().render()
        return html.Iframe(srcDoc=map_html, width='100%', height='600px')

    except Exception as e:
        return html.Div(f"Error rendering heatmap: {str(e)}")

    
def accidents_by_month():
    # Get day and month data
    query = f"""
        SELECT
            EXTRACT(YEAR FROM Start_Time) AS Year,
            EXTRACT(MONTH FROM Start_Time) AS Month,
            EXTRACT(DAY FROM Start_Time) AS Day
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Start_Time IS NOT NULL
    """
    df = client.query(query).to_dataframe().dropna()

    # Choose a representative year (most frequent)
    base_year = int(df['Year'].mode()[0])
    us_hols = holidays.UnitedStates(years=[base_year])

    # Organize holidays by month
    holiday_days_by_month = {}
    for date, name in us_hols.items():
        if date.year == base_year:
            holiday_days_by_month.setdefault(date.month, []).append((date.day, name))

    # Aggregate "All Months"
    all_data = df.groupby('Day').size().reset_index(name='Accidents')
    all_data['Rolling'] = all_data['Accidents'].rolling(3, center=True).mean()

    # Aggregate per month
    monthly_data = {}
    for m in range(1, 13):
        mdf = df[df['Month'] == m]
        mgroup = mdf.groupby('Day').size().reset_index(name='Accidents')
        mgroup['Rolling'] = mgroup['Accidents'].rolling(3, center=True).mean()
        monthly_data[m] = mgroup

    # Build Plotly figure
    fig = go.Figure()

    # Default view: All months
    fig.add_trace(go.Scatter(
        x=all_data['Day'], y=all_data['Accidents'],
        mode='lines+markers', name='Number of Accidents',
        line=dict(color='blue')
    ))
    fig.add_trace(go.Scatter(
        x=all_data['Day'], y=all_data['Rolling'],
        mode='lines', name='Rolling Average',
        line=dict(color='red')
    ))

    # Add hidden month traces
    for m in range(1, 13):
        d = monthly_data[m]
        fig.add_trace(go.Scatter(
            x=d['Day'], y=d['Accidents'],
            mode='lines+markers',
            name='Number of Accidents',
            visible=False,
            line=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=d['Day'], y=d['Rolling'],
            mode='lines',
            name='Rolling Average',
            visible=False,
            line=dict(color='red')
        ))

    # Dropdown buttons
    buttons = []
    month_names = ['All Months', 'January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']

    # Button for All Months (no holidays)
    buttons.append(dict(
        label='All Months',
        method='update',
        args=[
            {'visible': [True, True] + [False]*24},
            {'title': 'Accidents by Day - All Months', 'shapes': [], 'annotations': []}
        ]
    ))

    # Buttons for each individual month
    for i in range(1, 13):
        vis = [False]*2 + [False]*24
        vis[2*i] = True
        vis[2*i + 1] = True

        shapes = []
        annotations = []

        # If the month has holidays
        if i in holiday_days_by_month:
            y_base = 1.05
            y_gap = 0.07  # vertical spacing between stacked labels

            for idx, (day, label) in enumerate(sorted(holiday_days_by_month[i])):
                shapes.append(dict(
                    type='line',
                    x0=day, x1=day,
                    y0=0, y1=1, yref='paper',
                    line=dict(color='red', dash='dot')
                ))
                annotations.append(dict(
                    x=day,
                    y=y_base + idx * y_gap,
                    xref='x',
                    yref='paper',
                    text=label,
                    showarrow=False,
                    font=dict(size=11, color='red')
                ))

        buttons.append(dict(
            label=month_names[i],
            method='update',
            args=[
                {'visible': vis},
                {
                    'title': f'Accidents by Day - {month_names[i]} ({base_year})',
                    'shapes': shapes,
                    'annotations': annotations
                }
            ]
        ))

    # Final layout
    fig.update_layout(
        xaxis_title='Day of the Month',
        yaxis_title='Number of Accidents',
        height=650,
        margin=dict(t=100, r=40, b=40, l=40),
        updatemenus=[{
            'buttons': buttons,
            'direction': 'down',
            'showactive': True,
            'x': 0,
            'y': 1.25,
            'xanchor': 'left',   # <<< was 'right', now 'left'
            'yanchor': 'top',
            'pad': {'r': 10, 't': 10},
            'bgcolor': '#f0f0f0',
            'bordercolor': '#666',
            'font': {'size': 13},
        }],

        legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.25)
    )

    return dcc.Graph(figure=fig)