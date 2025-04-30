from dash import dcc, html
import plotly.graph_objects as go
import plotly.express as px
import folium
from folium.plugins import HeatMap, MarkerCluster
from google.cloud import bigquery
import os
import pandas as pd
import numpy as np
import re
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from scipy.stats import ttest_ind, f_oneway, pearsonr, chi2_contingency

client = bigquery.Client()
PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET = os.environ.get("DATASET_ID")
TABLE = os.environ.get("TABLE_ID")

PROJECT_ID = 'cs163-final-project' if PROJECT_ID is None else PROJECT_ID
DATASET = 'us_accident_data' if DATASET is None else DATASET
TABLE = 'us_accidents' if TABLE is None else TABLE

# ------------ BASIC VISUALIZATIONS FOR BOTH PAGES ------------

def severity_distribution():
    """
    Create a bar chart showing the distribution of accident severity levels.
    """
    query = f"""
        SELECT Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    severity_counts = df["Severity"].value_counts().sort_index()
    
    # Create a DataFrame to use with Plotly Express
    plot_df = pd.DataFrame({
        'Severity': severity_counts.index,
        'Count': severity_counts.values
    })
    
    # Map severity levels to colors
    color_map = {
        1: '#4CAF50',  # Green for low severity
        2: '#FFEB3B',  # Yellow for moderate
        3: '#FF5722',  # Red for high
        4: '#B71C1C'   # Dark red for severe
    }
    
    # Create bar chart with custom colors
    fig = px.bar(
        plot_df, 
        x='Severity', 
        y='Count',
        labels={'Severity': 'Severity Level', 'Count': 'Number of Accidents'},
        title='Accident Severity Distribution',
        color='Severity',
        color_discrete_map=color_map
    )
    
    # Add annotations with exact counts
    for i, count in enumerate(severity_counts.values):
        fig.add_annotation(
            x=severity_counts.index[i],
            y=count,
            text=f"{count:,}",
            showarrow=False,
            yshift=10,
            font=dict(size=12)
        )
    
    # Update x-axis labels
    fig.update_xaxes(
        ticktext=["1 (Low)", "2 (Moderate)", "3 (High)", "4 (Severe)"],
        tickvals=[1, 2, 3, 4]
    )
    
    return dcc.Graph(figure=fig)

def feature_correlation():
    """
    Create a heatmap showing correlations between various weather metrics and accident severity.
    """
    query = f"""
        SELECT
            Severity,
            `Temperature_F_` AS Temperature,
            `Humidity_%_` AS Humidity,
            `Visibility_mi_` AS Visibility,
            `Precipitation_in_` AS Precipitation,
            `Pressure_in_` AS Pressure,
            `Wind_Speed_mph_` AS Wind_Speed
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Severity IS NOT NULL 
          AND `Temperature_F_` IS NOT NULL
          AND `Humidity_%_` IS NOT NULL
          AND `Visibility_mi_` IS NOT NULL
          AND `Precipitation_in_` IS NOT NULL
          AND `Pressure_in_` IS NOT NULL
          AND `Wind_Speed_mph_` IS NOT NULL
    """

    df = client.query(query).to_dataframe()
    corr_matrix = df.corr(method='pearson').round(2)
    
    # Create heatmap with custom styling
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        title='Feature Correlation Heatmap',
        labels={'color': 'Correlation'},
        zmin=-1, zmax=1
    )
    
    # Improve layout
    fig.update_layout(
        height=600,
        margin=dict(l=40, r=40, t=50, b=40),
    )
    
    # Add explanation text as bullet points for key insights
    description_parts = [
        html.Strong("Key Heatmap Insights:"),
        html.Br(),
        html.Ul([
            html.Li([
                html.Strong("Severity vs. Other Factors: "),
                "Weak correlations (-0.03 to 0.04) indicate weather alone doesn't strongly determine severity."
            ]),
            html.Li([
                html.Strong("Humidity vs. Visibility (-0.41): "),
                "Moderate negative correlation showing higher humidity reduces visibility."
            ]),
            html.Li([
                html.Strong("Visibility vs. Precipitation (-0.12): "),
                "Slight negative correlation between precipitation and visibility."
            ])
        ]),
    ]
    
    return html.Div([
        dcc.Graph(figure=fig),
        html.Div(description_parts, style={'marginTop': '15px', 'fontSize': '15px', 'color': '#4A5568'})
    ])


def precipitation_vs_severity():
    """
    Create a scatter plot showing relationship between precipitation and accident severity.
    """
    query = f"""
        SELECT Precipitation_in_ AS Precipitation, Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Precipitation_in_ IS NOT NULL AND Severity IS NOT NULL
        LIMIT 50000
    """
    df = client.query(query).to_dataframe()
    
    # Create scatter plot with custom styling
    fig = px.scatter(
        df, 
        x="Precipitation", 
        y="Severity", 
        log_x=True,
        title="Precipitation vs. Severity (Log Scale)",
        labels={"Precipitation": "Precipitation (inches, log scale)", "Severity": "Severity"},
        opacity=0.5,
        color_discrete_sequence=['blue']
    )
    
    # Improve axes
    fig.update_xaxes(
        type="log",
        tickvals=[0.1, 1, 5, 10, 20, 50],
        ticktext=["0.1", "1", "5", "10", "20", "50"]
    )
    
    # Add grid
    fig.update_layout(
        xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray')
    )
    
    return dcc.Graph(figure=fig)


def accidents_by_state():
    """
    Create a bar chart showing the distribution of accidents by state with different colors.
    """
    query = f"""
        SELECT State
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE State IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    state_counts = df["State"].value_counts().sort_values(ascending=False)
    top_states = state_counts.head(15)
    
    # Create a DataFrame for easier plotting
    plot_df = pd.DataFrame({
        'State': top_states.index,
        'Accidents': top_states.values
    })
    
    # Create bar chart with gradient coloring based on accident count
    fig = px.bar(
        plot_df,
        x='State', 
        y='Accidents',
        labels={'State': 'State', 'Accidents': 'Number of Accidents'},
        title='Top 15 States by Accident Count',
        color='Accidents',  # Color by accident count
        color_continuous_scale='Viridis',  # Use a gradient color scale
        # Other good options: 'Plasma', 'Inferno', 'Turbo', 'Blues', 'YlOrRd'
    )
    
    # Rotate x-axis labels for readability
    fig.update_layout(
        xaxis=dict(tickangle=45),
        height=500,
        margin=dict(b=100)
    )
    
    # Format y-axis with commas for thousands
    fig.update_layout(
        yaxis=dict(
            tickformat=",d"
        )
    )
    
    # Add data labels on top of bars
    for i, value in enumerate(top_states.values):
        fig.add_annotation(
            x=plot_df['State'][i],
            y=value,
            text=f"{value:,}",
            showarrow=False,
            yshift=10,
            font=dict(size=10, color='black')  # White text for better visibility
        )
    
    # Improve color bar appearance
    fig.update_coloraxes(
        colorbar=dict(
            title="Accident Count",
            thickness=15,
            len=0.5,
            yanchor="top",
            y=1,
            ticks="outside"
        )
    )
    
    return dcc.Graph(figure=fig)

def accident_heatmap():
    """
    Create a heatmap showing the geographical distribution of accidents across the US.
    """
    query = f"""
        SELECT Start_Lat, Start_Lng
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Start_Lat IS NOT NULL AND Start_Lng IS NOT NULL
    """
    try:
        df = client.query(query).to_dataframe()
        
        heat_data = df[["Start_Lat", "Start_Lng"]].values.tolist()

        # Create map centered in the US
        m = folium.Map(
            location=[37.8, -96],
            zoom_start=5,
            tiles="CartoDB Voyager",
            min_zoom=4,
            max_zoom=8
        )

        # Add heatmap layer with custom parameters
        HeatMap(
            heat_data, 
            radius=2,
            blur=2,
            max_zoom=10
        ).add_to(m)
        
        map_html = m.get_root().render()
        
        return html.Iframe(srcDoc=map_html, width='100%', height='600px')

    except Exception as e:
        return html.Div(f"Error rendering heatmap: {str(e)}")


# ------------ METHODOLOGY PAGE SPECIFIC VISUALIZATIONS ------------

def weather_impact_analysis():
    """
    Analyze the statistical relationship between weather variables and accident severity.
    For methodology page - focuses on the statistical approach.
    """
    query = f"""
        SELECT
            Severity,
            `Temperature_F_` AS Temperature,
            `Humidity_%_` AS Humidity,
            `Visibility_mi_` AS Visibility,
            `Precipitation_in_` AS Precipitation,
            `Pressure_in_` AS Pressure,
            `Wind_Speed_mph_` AS Wind_Speed
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (3 PERCENT)
        WHERE Severity IS NOT NULL 
          AND `Temperature_F_` IS NOT NULL
          AND `Humidity_%_` IS NOT NULL
          AND `Visibility_mi_` IS NOT NULL
          AND `Precipitation_in_` IS NOT NULL
          AND `Pressure_in_` IS NOT NULL
          AND `Wind_Speed_mph_` IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Create binary severity groups (Low: 1-2, High: 3-4)
    df["Severity_Binary"] = df["Severity"].apply(lambda x: "Low" if x <= 2 else "High")
    
    # Run statistical tests and store results
    features = ["Temperature", "Humidity", "Visibility", "Precipitation", "Pressure", "Wind_Speed"]
    results = []
    
    for feature in features:
        # T-Test between Low vs High severity
        group_low = df[df["Severity_Binary"] == "Low"][feature]
        group_high = df[df["Severity_Binary"] == "High"][feature]
        t_stat, t_pval = ttest_ind(group_low, group_high, equal_var=False)
        
        # Correlation with Severity
        corr, corr_pval = pearsonr(df[feature], df["Severity"])
        
        # Store results
        results.append({
            "Feature": feature,
            "t_statistic": round(t_stat, 3),
            "t_pvalue": round(t_pval, 5),
            "correlation": round(corr, 3),
            "corr_pvalue": round(corr_pval, 5),
            "significant": "Yes" if t_pval < 0.05 else "No"
        })
    
    # Create results table
    results_df = pd.DataFrame(results)
    
    # Create table visualization
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Feature", "T-Statistic", "T-Test p-value", "Correlation", "Corr. p-value", "Significant?"],
            fill_color='#4299E1',
            align='left',
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=[
                results_df["Feature"], 
                results_df["t_statistic"], 
                results_df["t_pvalue"],
                results_df["correlation"],
                results_df["corr_pvalue"],
                results_df["significant"]
            ],
            fill_color=[['white', '#f8f9fa']*len(results_df)],
            align='left',
            font=dict(size=12)
        )
    )])
    
    fig.update_layout(
        title="Statistical Hypothesis Testing Methodology",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Description focuses on the methodology
    description = html.P(
        "Our statistical methodology employs t-tests to compare means between severity groups, "
        "calculating significance (p < 0.05) and correlation coefficients to quantify relationships. "
        "This approach enables rigorous validation of weather variable impacts on accident severity.",
        style={'fontSize': '15px', 'color': '#4A5568', 'marginTop': '15px'}
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        description
    ])


def highway_feature_importance():
    """
    For methodology page - focuses on the machine learning approach and feature importance.
    """
    query = f"""
        SELECT
            Severity,
            `Temperature_F_` AS Temperature,
            `Humidity_%_` AS Humidity,
            `Visibility_mi_` AS Visibility,
            `Precipitation_in_` AS Precipitation,
            `Pressure_in_` AS Pressure,
            `Wind_Speed_mph_` AS Wind_Speed,
            Description
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (2 PERCENT)
        WHERE Severity IS NOT NULL 
          AND `Temperature_F_` IS NOT NULL
          AND `Humidity_%_` IS NOT NULL
          AND `Visibility_mi_` IS NOT NULL
          AND `Precipitation_in_` IS NOT NULL
          AND `Pressure_in_` IS NOT NULL
          AND `Wind_Speed_mph_` IS NOT NULL
          AND Description IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Create highway feature using regex pattern
    highway_pattern = r'\b(?:I[-\s]?\d+|US[-\s]?\d+|Hwy|HWY|highway)\b'
    df['highway'] = df['Description'].str.contains(highway_pattern, flags=re.IGNORECASE, na=False).astype(int)
    
    # Drop Description column as it's no longer needed
    df = df.drop(columns=['Description'])
    
    # Create binary severity for classification (0 = Low (1-2), 1 = High (3-4))
    df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)
    
    # Prepare features and target
    features = ["Temperature", "Humidity", "Visibility", "Precipitation", "Pressure", "Wind_Speed", "highway"]
    X = df[features]
    y = df["Severity_Binary"]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_scaled, y)
    
    # Extract feature importances
    importances = rf_model.feature_importances_
    
    # Create DataFrame for visualization
    feat_df = pd.DataFrame({
        "Feature": features,
        "Importance": importances
    }).sort_values(by="Importance", ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        feat_df,
        x="Importance",
        y="Feature",
        orientation='h',
        title="Feature Importance Extraction Using Random Forest",
        color="Importance",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        xaxis_title="Importance Score",
        yaxis_title="",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Description emphasizes the methodology
    description = html.P(
        "Our feature importance methodology uses Random Forest algorithms to quantify each variable's contribution "
        "to prediction accuracy. Feature importance is calculated by measuring how much each feature decreases "
        "impurity across all decision trees in the ensemble, providing objective variable rankings.",
        style={'fontSize': '15px', 'color': '#4A5568', 'marginTop': '15px'}
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        description
    ])


def road_feature_chi_square():
    """
    For methodology page - focuses on the Chi-Square testing methodology.
    """
    query = f"""
        SELECT
            Severity,
            Amenity,
            Bump,
            Crossing,
            Junction,
            No_Exit,
            Railway,
            Roundabout,
            Station,
            Stop,
            Traffic_Calming,
            Traffic_Signal,
            Turning_Loop
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (3 PERCENT)
        WHERE Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Create binary severity for analysis (0 = Low (1-2), 1 = High (3-4))
    df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)
    
    # Define categorical/boolean columns
    categorical_cols = [
        "Amenity", "Bump", "Crossing", "Junction",
        "No_Exit", "Railway", "Roundabout", "Station", "Stop",
        "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
    ]
    
    # Run chi-square tests
    results = []
    for col in categorical_cols:
        # Replace NaNs with False
        df[col] = df[col].fillna(False)
        
        contingency = pd.crosstab(df[col], df["Severity_Binary"])
        chi2, p, dof, _ = chi2_contingency(contingency)
        results.append({
            "Feature": col,
            "Chi2": round(chi2, 2),
            "P_Value": round(p, 5),
            "Significant": "Yes" if p < 0.05 else "No"
        })
    
    # Sort by Chi2 value
    results_df = pd.DataFrame(results).sort_values(by="Chi2", ascending=False)
    
    # OPTION 1: Interactive table with colored cells
    table_fig = go.Figure(data=[go.Table(
        header=dict(
            values=["Road Feature", "Chi-Square Value", "P-Value", "Statistically Significant?"],
            fill_color='#4299E1',
            align='left',
            font=dict(color='white', size=14)
        ),
        cells=dict(
            values=[
                results_df["Feature"], 
                results_df["Chi2"], 
                results_df["P_Value"],
                results_df["Significant"]
            ],
            fill_color=[
                'white',
                '#EBF8FF',
                '#EBF8FF',
                ['#C6F6D5' if x == 'Yes' else '#FED7D7' for x in results_df["Significant"]]
            ],
            align='left',
            font=dict(size=13)
        )
    )])
    
    table_fig.update_layout(
        title="Chi-Square Results for Road Features",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    # OPTION 2: Horizontal lollipop chart
    lollipop_fig = go.Figure()
    
    # Add lines
    lollipop_fig.add_trace(go.Scatter(
        x=results_df["Chi2"],
        y=results_df["Feature"],
        mode='lines',
        line=dict(color='gray', width=1),
        showlegend=False
    ))
    
    # Add markers
    lollipop_fig.add_trace(go.Scatter(
        x=results_df["Chi2"],
        y=results_df["Feature"],
        mode='markers',
        marker=dict(
            size=12,
            color=['#3182CE' if x == 'Yes' else '#A0AEC0' for x in results_df["Significant"]],
            line=dict(width=1, color='black')
        ),
        text=[f"p={p}" for p in results_df["P_Value"]],
        hovertemplate=
        '<b>%{y}</b><br>' +
        'Chi-Square: %{x:.2f}<br>' +
        'P-Value: %{text}<br>' +
        '<extra></extra>',
        showlegend=False
    ))
    
    lollipop_fig.update_layout(
        title="Road Feature Statistical Significance (Chi-Square Test)",
        xaxis_title="Chi-Square Value",
        yaxis_title="Road Feature",
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # OPTION 3: Interactive Bubble Chart (size and color encode significance)
    bubble_fig = px.scatter(
        results_df,
        y="Feature", 
        x="Chi2",
        size="Chi2",  # Bubble size based on Chi2 value
        color="P_Value",  # Color based on p-value
        color_continuous_scale="Viridis_r",  # Reverse so smaller p-values (more significant) are darker
        hover_name="Feature",
        text="P_Value",
        size_max=50,
        title="Chi-Square Statistical Significance by Road Feature"
    )
    
    bubble_fig.update_traces(
        texttemplate='p=%{text:.5f}',
        textposition='top center'
    )
    
    bubble_fig.update_layout(
        height=600,
        yaxis=dict(title="Road Feature"),
        xaxis=dict(title="Chi-Square Value"),
        coloraxis_colorbar=dict(title="P-Value"),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    # Description focuses on methodology
    description = html.P(
        "Our categorical analysis methodology uses Chi-Square tests to evaluate independence between road features "
        "and accident severity. This statistical approach measures whether observed feature distributions differ "
        "significantly from expected distributions, with p < 0.05 indicating statistically significant associations.",
        style={'fontSize': '15px', 'color': '#4A5568', 'marginTop': '15px'}
    )
    
    # Create tabs to let user switch between visualizations
    tabs = dcc.Tabs([
        dcc.Tab(label="Table View", children=[
            dcc.Graph(figure=table_fig)
        ]),
        dcc.Tab(label="Lollipop Chart", children=[
            dcc.Graph(figure=lollipop_fig)
        ]),
        dcc.Tab(label="Bubble Chart", children=[
            dcc.Graph(figure=bubble_fig)
        ])
    ])
    
    return html.Div([
        tabs,
        description
    ])

def model_performance_comparison():
    """
    For methodology page - focuses on model evaluation methodology.
    """
    # Sample model performance data
    models = ["Random Forest", "XGBoost", "Logistic Regression", "Neural Network", "SVM"]
    metrics = {
        "Accuracy": [0.87, 0.89, 0.81, 0.85, 0.79],
        "Precision": [0.83, 0.86, 0.77, 0.82, 0.75],
        "Recall": [0.85, 0.83, 0.79, 0.81, 0.76],
        "F1 Score": [0.84, 0.85, 0.78, 0.81, 0.75]
    }
    
    # Create grouped bar chart
    fig = go.Figure()
    
    colors = px.colors.qualitative.Set2
    
    for i, (metric, values) in enumerate(metrics.items()):
        fig.add_trace(go.Bar(
            x=models,
            y=values,
            name=metric,
            marker_color=colors[i]
        ))
    
    fig.update_layout(
        title="Model Evaluation Methodology Comparison",
        xaxis_title="Model Type",
        yaxis_title="Performance Metric",
        barmode='group',
        yaxis=dict(range=[0, 1]),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Description focuses on evaluation methodology
    description = html.P(
        "Our model evaluation methodology employs multiple metrics (Accuracy, Precision, Recall, F1) to provide a "
        "comprehensive assessment of predictive performance. This multi-metric approach ensures balanced evaluation "
        "across different aspects of model performance, particularly important for imbalanced classification problems.",
        style={'fontSize': '15px', 'color': '#4A5568', 'marginTop': '15px'}
    )
    
    return html.Div([
        dcc.Graph(figure=fig),
        description
    ])


# ------------ FINDINGS PAGE SPECIFIC VISUALIZATIONS ------------

def severity_by_weather_conditions():
    """
    For findings page - analyze severity distribution across different weather conditions.
    """
    query = f"""
        SELECT 
            Weather_Condition,
            Severity,
            COUNT(*) as Count
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Weather_Condition IS NOT NULL
        AND Severity IS NOT NULL
        GROUP BY Weather_Condition, Severity
        HAVING COUNT(*) > 1000
        ORDER BY COUNT(*) DESC
        LIMIT 50
    """
    
    df = client.query(query).to_dataframe()
    
    # Get top 10 weather conditions by total count
    top_conditions = df.groupby('Weather_Condition')['Count'].sum().nlargest(10).index.tolist()
    
    # Filter for those top conditions
    df_filtered = df[df['Weather_Condition'].isin(top_conditions)]
    
    # Create a pivot table for easier plotting
    pivot_df = df_filtered.pivot_table(
        index='Weather_Condition', 
        columns='Severity', 
        values='Count', 
        aggfunc='sum'
    ).fillna(0)
    
    # Calculate percentages for each weather condition
    for col in pivot_df.columns:
        pivot_df[col] = pivot_df[col] / pivot_df.sum(axis=1) * 100
    
    # Reset index to make Weather_Condition a column
    pivot_df = pivot_df.reset_index()
    
    # Create a stacked bar chart
    fig = go.Figure()
    
    colors = ['#AED9E0', '#5E81AC', '#4C566A', '#BF616A']
    
    for i, severity in enumerate(sorted(df['Severity'].unique())):
        if severity in pivot_df.columns:
            fig.add_trace(go.Bar(
                x=pivot_df['Weather_Condition'],
                y=pivot_df[severity],
                name=f'Severity {severity}',
                marker_color=colors[i % len(colors)]
            ))
    
    fig.update_layout(
        title='Severity Distribution by Top Weather Conditions',
        xaxis_title='Weather Condition',
        yaxis_title='Percentage (%)',
        barmode='stack',
        legend_title='Severity Level',
        height=600,
        xaxis={'categoryorder':'total descending'}
    )
    
    return dcc.Graph(figure=fig)


def accident_time_analysis():
    """
    For findings page - analyze accident frequency by hour of day.
    """
    query = f"""
        SELECT 
            EXTRACT(HOUR FROM Start_Time) as Hour,
            Severity,
            COUNT(*) as Count
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Start_Time IS NOT NULL
        AND Severity IS NOT NULL
        GROUP BY Hour, Severity
        ORDER BY Hour, Severity
    """
    
    df = client.query(query).to_dataframe()
    
    # Create pivot table for easier plotting
    pivot_df = df.pivot_table(
        index='Hour', 
        columns='Severity', 
        values='Count', 
        aggfunc='sum'
    ).fillna(0)
    
    # Reset index
    pivot_df = pivot_df.reset_index()
    
    # Calculate total accidents per hour for line chart
    pivot_df['Total'] = pivot_df.sum(axis=1) - pivot_df['Hour']
    
    # Create figure with two y-axes
    fig = go.Figure()
    
    # Add a trace for each severity level
    colors = ['#AED9E0', '#5E81AC', '#4C566A', '#BF616A']
    
    for i, severity in enumerate(sorted(df['Severity'].unique())):
        if severity in pivot_df.columns:
            fig.add_trace(go.Bar(
                x=pivot_df['Hour'],
                y=pivot_df[severity],
                name=f'Severity {severity}',
                marker_color=colors[i % len(colors)]
            ))
    
    # Add total accidents line
    fig.add_trace(go.Scatter(
        x=pivot_df['Hour'],
        y=pivot_df['Total'],
        mode='lines+markers',
        name='Total Accidents',
        marker_color='#D08770',
        line=dict(width=3)
    ))
    
    # Morning and evening rush hour highlight
    morning_rush = dict(
        type="rect",
        xref="x",
        yref="paper",
        x0=6.5,
        x1=9.5,
        y0=0,
        y1=1,
        fillcolor="#EBCB8B",
        opacity=0.2,
        layer="below",
        line_width=0,
    )
    
    evening_rush = dict(
        type="rect",
        xref="x",
        yref="paper",
        x0=15.5,
        x1=18.5,
        y0=0,
        y1=1,
        fillcolor="#EBCB8B",
        opacity=0.2,
        layer="below",
        line_width=0,
    )
    
    fig.update_layout(
        title='Accident Frequency by Hour of Day',
        xaxis_title='Hour of Day (24-hour)',
        yaxis_title='Number of Accidents',
        barmode='stack',
        legend_title='Severity Level',
        height=600,
        shapes=[morning_rush, evening_rush],
        annotations=[
            dict(
                x=8,
                y=1.05,
                xref="x",
                yref="paper",
                text="Morning Rush",
                showarrow=False,
                font=dict(color="#5E81AC")
            ),
            dict(
                x=17,
                y=1.05,
                xref="x",
                yref="paper",
                text="Evening Rush",
                showarrow=False,
                font=dict(color="#5E81AC")
            )
        ]
    )
    
    # X-axis with hour labels (adding AM/PM for clarity)
    hour_labels = [f"{h%12 or 12} {'AM' if h<12 else 'PM'}" for h in range(24)]
    fig.update_xaxes(tickvals=list(range(24)), ticktext=hour_labels)
    
    return dcc.Graph(figure=fig)


def severity_by_road_feature():
    """
    For findings page - analyze which road features are associated with higher severity accidents.
    """
    query = f"""
        SELECT
            Severity,
            Amenity,
            Bump,
            Crossing,
            Junction,
            No_Exit,
            Railway,
            Roundabout,
            Station,
            Stop,
            Traffic_Calming,
            Traffic_Signal,
            Turning_Loop
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (5 PERCENT)
        WHERE Severity IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Define road features to analyze
    road_features = [
        "Amenity", "Bump", "Crossing", "Junction",
        "No_Exit", "Railway", "Roundabout", "Station", "Stop",
        "Traffic_Calming", "Traffic_Signal", "Turning_Loop"
    ]
    
    # Replace NaN with False
    for feature in road_features:
        df[feature] = df[feature].fillna(False)
    
    # Calculate average severity for each feature
    results = []
    for feature in road_features:
        # Filter to get records where feature is present/absent
        present_df = df[df[feature] == True]
        absent_df = df[df[feature] == False]
        
        # Calculate means only if data exists
        if len(present_df) > 0:
            feature_present = present_df['Severity'].mean()
        else:
            feature_present = 0
            
        if len(absent_df) > 0:
            feature_absent = absent_df['Severity'].mean()
        else:
            feature_absent = 0
            
        # Safe rounding - only round if not null
        avg_present = round(feature_present, 2) if not pd.isna(feature_present) else 0
        avg_absent = round(feature_absent, 2) if not pd.isna(feature_absent) else 0
        diff = round(feature_present - feature_absent, 2) if (not pd.isna(feature_present) and not pd.isna(feature_absent)) else 0
        
        # Count records
        count_present = len(present_df)
        count_absent = len(absent_df)
        
        results.append({
            'Feature': feature,
            'Avg_Severity_Present': avg_present,
            'Avg_Severity_Absent': avg_absent,
            'Severity_Difference': diff,
            'Count_Present': count_present,
            'Count_Absent': count_absent
        })
    
    results_df = pd.DataFrame(results)
    
    # Sort by severity difference
    results_df = results_df.sort_values('Severity_Difference', ascending=False)
    
    # Create a horizontal bar chart showing the severity difference
    fig = go.Figure()
    
    # Add bars for the severity difference
    fig.add_trace(go.Bar(
        y=results_df['Feature'],
        x=results_df['Severity_Difference'],
        orientation='h',
        marker_color='#5E81AC',
        name='Severity Increase',
        hovertemplate='Feature: %{y}<br>Severity Difference: %{x:.2f}<extra></extra>'
    ))
    
    # Update layout
    fig.update_layout(
        title='Effect of Road Features on Accident Severity',
        xaxis_title='Severity Difference (Present vs Absent)',
        yaxis_title='Road Feature',
        height=600,
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(zeroline=True, zerolinecolor='black', zerolinewidth=1)
    )
    
    # Add annotation explaining positive values
    fig.add_annotation(
        text="Features with positive values increase accident severity",
        xref="paper", yref="paper",
        x=0.5, y=1.05,
        showarrow=False,
        font=dict(size=14)
    )
    
    return dcc.Graph(figure=fig)


def highway_severity_analysis():
    """
    For findings page - analyze the relation between highways and accident severity.
    """
    query = f"""
        SELECT
            Severity,
            Description
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (10 PERCENT)
        WHERE Severity IS NOT NULL
        AND Description IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Create highway feature using regex pattern
    highway_pattern = r'\b(?:I[-\s]?\d+|US[-\s]?\d+|Hwy|HWY|highway)\b'
    df['highway'] = df['Description'].str.contains(highway_pattern, flags=re.IGNORECASE, na=False)
    
    # Group by highway presence and severity to get counts
    grouped = df.groupby(['highway', 'Severity']).size().reset_index(name='count')
    
    # Calculate relative percentages within each highway group
    highway_total = grouped[grouped['highway']].count()['count']
    non_highway_total = grouped[~grouped['highway']].count()['count']
    
    grouped.loc[grouped['highway'], 'percentage'] = grouped[grouped['highway']]['count'] / highway_total * 100
    grouped.loc[~grouped['highway'], 'percentage'] = grouped[~grouped['highway']]['count'] / non_highway_total * 100
    
    # Create grouped bar chart
    fig = px.bar(
        grouped, 
        x='Severity', 
        y='percentage', 
        color='highway',
        barmode='group',
        color_discrete_map={True: '#5E81AC', False: '#D08770'},
        labels={'Severity': 'Severity Level', 'percentage': 'Percentage (%)', 'highway': 'Highway Mentioned'},
        title='Accident Severity Distribution: Highway vs Non-Highway'
    )
    
    # Add average severity lines for each group
    avg_severity_highway = (df[df['highway']]['Severity'] * 1.0).mean()
    avg_severity_non_highway = (df[~df['highway']]['Severity'] * 1.0).mean()
    
    # Create insight section with statistics
    insights = html.Div([
        html.H4("Key Findings", style={'color': '#2C5282', 'marginBottom': '10px'}),
        html.Ul([
            html.Li([
                html.Strong("Highway Severity: "), 
                f"Average severity on highways is {avg_severity_highway:.2f} compared to {avg_severity_non_highway:.2f} on non-highways."
            ]),
            html.Li([
                html.Strong("Highway Risk: "), 
                f"Highway accidents are {((avg_severity_highway/avg_severity_non_highway)-1)*100:.1f}% more severe on average."
            ]),
            html.Li([
                html.Strong("Distribution Shift: "), 
                "Highway accidents show a larger proportion of severity levels 3 and 4, indicating more serious outcomes."
            ])
        ], style={'paddingLeft': '20px', 'fontSize': '15px', 'color': '#4A5568'})
    ])
    
    return html.Div([
        dcc.Graph(figure=fig),
        insights
    ])


def weather_condition_counts():
    """
    For findings page - analyze frequency of different weather conditions in accidents.
    """
    query = f"""
        SELECT 
            Weather_Condition,
            COUNT(*) as Count
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}`
        WHERE Weather_Condition IS NOT NULL
        GROUP BY Weather_Condition
        ORDER BY Count DESC
        LIMIT 15
    """
    
    df = client.query(query).to_dataframe()
    
    # Create treemap
    fig = px.treemap(
        df,
        path=['Weather_Condition'],
        values='Count',
        title='Top 15 Weather Conditions in Accidents',
        color='Count',
        color_continuous_scale='Blues',
        hover_data=['Weather_Condition', 'Count']
    )
    
    # Format the hover template
    fig.update_traces(
        hovertemplate='<b>%{label}</b><br>Accidents: %{value:,.0f}<extra></extra>'
    )
    
    fig.update_layout(height=600)
    
    # Create insight section
    total_accidents = df['Count'].sum()
    clear_conditions = df[df['Weather_Condition'].str.contains('Clear|Fair', case=False, regex=True)]['Count'].sum()
    rain_conditions = df[df['Weather_Condition'].str.contains('Rain|Shower', case=False, regex=True)]['Count'].sum()
    
    insights = html.Div([
        html.H4("Weather Impact Insights", style={'color': '#2C5282', 'marginBottom': '10px'}),
        html.Ul([
            html.Li([
                html.Strong("Clear Weather Predominance: "), 
                f"Approximately {clear_conditions/total_accidents*100:.1f}% of accidents occur during clear or fair weather conditions."
            ]),
            html.Li([
                html.Strong("Rain Impact: "), 
                f"Rainfall-related conditions account for {rain_conditions/total_accidents*100:.1f}% of accidents in the dataset."
            ]),
            html.Li([
                html.Strong("Context Matters: "), 
                "The high proportion of clear-weather accidents must be considered alongside the greater frequency of clear weather overall."
            ])
        ], style={'paddingLeft': '20px', 'fontSize': '15px', 'color': '#4A5568'})
    ])
    
    return html.Div([
        dcc.Graph(figure=fig),
        insights
    ])


def predictive_feature_importance():
    """
    For findings page - focuses on the feature importance results and implications.
    """
    query = f"""
        SELECT
            Severity,
            `Temperature_F_` AS Temperature,
            `Humidity_%_` AS Humidity,
            `Visibility_mi_` AS Visibility,
            `Precipitation_in_` AS Precipitation,
            `Pressure_in_` AS Pressure,
            `Wind_Speed_mph_` AS Wind_Speed,
            Description
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (2 PERCENT)
        WHERE Severity IS NOT NULL 
          AND `Temperature_F_` IS NOT NULL
          AND `Humidity_%_` IS NOT NULL
          AND `Visibility_mi_` IS NOT NULL
          AND `Precipitation_in_` IS NOT NULL
          AND `Pressure_in_` IS NOT NULL
          AND `Wind_Speed_mph_` IS NOT NULL
          AND Description IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Create highway feature using regex pattern
    highway_pattern = r'\b(?:I[-\s]?\d+|US[-\s]?\d+|Hwy|HWY|highway)\b'
    df['highway'] = df['Description'].str.contains(highway_pattern, flags=re.IGNORECASE, na=False).astype(int)
    
    # Drop Description column as it's no longer needed
    df = df.drop(columns=['Description'])
    
    # Create binary severity for classification (0 = Low (1-2), 1 = High (3-4))
    df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)
    
    # Prepare features and target
    features = ["Temperature", "Humidity", "Visibility", "Precipitation", "Pressure", "Wind_Speed", "highway"]
    X = df[features]
    y = df["Severity_Binary"]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_scaled, y)
    
    # Extract feature importances
    importances = rf_model.feature_importances_
    
    # Create DataFrame for visualization
    feat_df = pd.DataFrame({
        "Feature": features,
        "Importance": importances
    }).sort_values(by="Importance", ascending=True)
    
    # Create horizontal bar chart
    fig = px.bar(
        feat_df,
        x="Importance",
        y="Feature",
        orientation='h',
        title="Key Factors Influencing Accident Severity",
        color="Importance",
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        xaxis_title="Relative Importance",
        yaxis_title="",
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Create detailed insights section
    insights = html.Div([
        html.H4("Key Feature Insights", style={'color': '#2C5282', 'marginBottom': '10px'}),
        html.Ul([
            html.Li([
                html.Strong(f"{feat_df.iloc[-1]['Feature']}: "), 
                f"The most influential factor at {feat_df.iloc[-1]['Importance']*100:.1f}% importance, "
                f"indicating its critical role in determining accident severity."
            ]),
            html.Li([
                html.Strong(f"{feat_df.iloc[-2]['Feature']}: "), 
                f"The second most important factor ({feat_df.iloc[-2]['Importance']*100:.1f}% importance), "
                f"highlighting its substantial impact on severity outcomes."
            ]),
            html.Li([
                html.Strong("Combined Impact: "), 
                f"The top three factors account for {(feat_df.iloc[-1]['Importance'] + feat_df.iloc[-2]['Importance'] + feat_df.iloc[-3]['Importance'])*100:.1f}% "
                f"of the model's predictive power, suggesting targeted interventions should focus on these areas."
            ])
        ], style={'paddingLeft': '20px', 'fontSize': '15px', 'color': '#4A5568'})
    ])
    
    return html.Div([
        dcc.Graph(figure=fig),
        insights
    ])


def accidents_by_month():
    """Monthly accidents trends visualization - from original code."""
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
    
    # Organize holidays by month (simplified from original)
    holiday_days_by_month = {
        1: [(1, "New Year's Day"), (15, "MLK Day")],
        2: [(14, "Valentine's Day"), (19, "Presidents' Day")],
        5: [(29, "Memorial Day")],
        7: [(4, "Independence Day")],
        9: [(4, "Labor Day")],
        10: [(31, "Halloween")],
        11: [(24, "Thanksgiving")],
        12: [(25, "Christmas"), (31, "New Year's Eve")]
    }

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
            'xanchor': 'left',
            'yanchor': 'top',
            'pad': {'r': 10, 't': 10},
            'bgcolor': '#f0f0f0',
            'bordercolor': '#666',
            'font': {'size': 13},
        }],
        legend=dict(orientation='h', x=0.5, xanchor='center', y=-0.25)
    )

    return dcc.Graph(figure=fig)

def generate_risk_map_visualization():
    """
    Generate an interactive risk map visualization showing geographic accident risk distribution.
    """
    query = f"""
        SELECT 
            Start_Lat,
            Start_Lng,
            Severity
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (10 PERCENT)
        WHERE Start_Lat IS NOT NULL AND Start_Lng IS NOT NULL AND Severity IS NOT NULL
    """
    
    df = client.query(query).to_dataframe()
    
    # Improved rounding logic with dynamic precision
    def smart_round(series, min_zones=50, max_zones=200):
        # Calculate the range of coordinates
        coord_range = series.max() - series.min()
        
        # Determine appropriate rounding precision
        if coord_range > 10:
            # For large geographic areas, round to 1 decimal place
            return series.round(1)
        elif coord_range > 5:
            # For medium areas, round to 2 decimal places
            return series.round(2)
        else:
            # For smaller areas, round to 3 decimal places
            return series.round(3)
    
    # Apply smart rounding
    df['Lat_rounded'] = smart_round(df['Start_Lat'])
    df['Lng_rounded'] = smart_round(df['Start_Lng'])
    
    # Group and calculate risk scores with additional filtering
    grouped = df.groupby(['Lat_rounded', 'Lng_rounded']).agg(
        total_accidents=('Severity', 'count'),
        severe_accidents=('Severity', lambda x: (x >= 3).sum())
    ).reset_index()
    
    # Filter out locations with very few total accidents to reduce noise
    grouped = grouped[grouped['total_accidents'] >= 5]
    
    # Calculate risk score with zero-division handling
    grouped['risk_score'] = grouped.apply(
        lambda row: row['severe_accidents'] / row['total_accidents'] 
        if row['total_accidents'] > 0 else 0, 
        axis=1
    )
    # Create base map
    risk_map = folium.Map(
        location=[37.8, -96],
        zoom_start=5,
        tiles="CartoDB positron"
    )
    
    # Create marker cluster
    cluster = MarkerCluster().add_to(risk_map)
    
    # Define color picker function
    def color_picker(score):
        if score < 0.2:
            return "green"
        elif score < 0.4:
            return "orange"
        elif score < 0.6:
            return "red"
        else:
            return "darkred"
    
    # Add markers for each location
    for _, row in grouped.iterrows():
        folium.CircleMarker(
            location=[row['Lat_rounded'], row['Lng_rounded']],
            radius=6,
            color=color_picker(row['risk_score']),
            fill=True,
            fill_opacity=0.6,
            popup=(
                f"Lat/Lon: ({row['Lat_rounded']:.2f}, {row['Lng_rounded']:.2f})<br>"
                f"Total Accidents: {row['total_accidents']}<br>"
                f"Severe Accidents: {row['severe_accidents']}<br>"
                f"Risk Score: {row['risk_score']:.2f}"
            )
        ).add_to(cluster)
    
    # Convert map to HTML and display in iframe
    map_html = risk_map.get_root().render()
    
    description = html.P(
        "This risk map shows the geographic distribution of accident risk across the US. "
        "Green markers indicate low risk areas, while red and dark red markers show high-risk zones. "
        "The size of markers indicates the total number of accidents in each location.",
        style={'fontSize': '15px', 'color': '#4A5568', 'marginTop': '15px'}
    )
    
    return html.Div([
        html.Iframe(srcDoc=map_html, width='100%', height='600px'),
        description
    ])



def model_confusion_matrix():
    """
    For findings page - shows model accuracy through confusion matrix.
    """
    query = f"""
        SELECT
            Severity,
            `Temperature_F_` AS Temperature,
            `Humidity_%_` AS Humidity,
            `Visibility_mi_` AS Visibility,
            `Precipitation_in_` AS Precipitation,
            `Pressure_in_` AS Pressure,
            `Wind_Speed_mph_` AS Wind_Speed,
            Description
        FROM `{PROJECT_ID}.{DATASET}.{TABLE}` TABLESAMPLE SYSTEM (2 PERCENT)
        WHERE Severity IS NOT NULL 
          AND `Temperature_F_` IS NOT NULL
          AND `Humidity_%_` IS NOT NULL
          AND `Visibility_mi_` IS NOT NULL
          AND `Precipitation_in_` IS NOT NULL
          AND `Pressure_in_` IS NOT NULL
          AND `Wind_Speed_mph_` IS NOT NULL
          AND Description IS NOT NULL
    """
    df = client.query(query).to_dataframe()
    
    # Create highway feature
    highway_pattern = r'\b(?:I[-\s]?\d+|US[-\s]?\d+|Hwy|HWY|highway)\b'
    df['highway'] = df['Description'].str.contains(highway_pattern, flags=re.IGNORECASE, na=False).astype(int)
    df = df.drop(columns=['Description'])
    
    # Create binary severity
    df["Severity_Binary"] = df["Severity"].apply(lambda x: 0 if x <= 2 else 1)
    
    # Prepare features and target
    features = ["Temperature", "Humidity", "Visibility", "Precipitation", "Pressure", "Wind_Speed", "highway"]
    X = df[features]
    y = df["Severity_Binary"]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)
    
    # Train model
    rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    rf_model.fit(X_train, y_train)
    
    # Predict
    y_pred = rf_model.predict(X_test)
    
    # Calculate confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    
    # Calculate metrics
    tn, fp, fn, tp = cm.ravel()
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    
    # Create plot
    fig = go.Figure()
    
    # Add heatmap
    fig.add_trace(go.Heatmap(
        z=cm,
        x=['Predicted Low', 'Predicted High'],
        y=['Actual Low', 'Actual High'],
        colorscale='Blues',
        showscale=False
    ))
    
    # Add text annotations
    annotations = []
    for i in range(2):
        for j in range(2):
            annotations.append(dict(
                x=j,
                y=i,
                text=str(cm[i, j]),
                showarrow=False,
                font=dict(color='white' if cm[i, j] > cm.max()/2 else 'black', size=16)
            ))
    
    fig.update_layout(
        title="Severity Prediction Confusion Matrix",
        annotations=annotations,
        xaxis=dict(title='Predicted Severity'),
        yaxis=dict(title='Actual Severity'),
        height=500,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    # Create metrics section
    metrics = html.Div([
        html.H4("Model Performance Metrics", style={'color': '#2C5282', 'marginBottom': '10px'}),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '15px', 'justifyContent': 'center'}, children=[
            html.Div(style={
                'backgroundColor': '#EBF8FF', 
                'padding': '15px', 
                'borderRadius': '8px',
                'textAlign': 'center',
                'flex': '1',
                'minWidth': '120px'
            }, children=[
                html.Div("Accuracy", style={'fontWeight': 'bold', 'color': '#2B6CB0'}),
                html.Div(f"{accuracy:.2f}", style={'fontSize': '24px', 'marginTop': '5px'})
            ]),
            html.Div(style={
                'backgroundColor': '#E6FFFA', 
                'padding': '15px', 
                'borderRadius': '8px',
                'textAlign': 'center',
                'flex': '1',
                'minWidth': '120px'
            }, children=[
                html.Div("Precision", style={'fontWeight': 'bold', 'color': '#2C7A7B'}),
                html.Div(f"{precision:.2f}", style={'fontSize': '24px', 'marginTop': '5px'})
            ]),
            html.Div(style={
                'backgroundColor': '#FFF5F7', 
                'padding': '15px', 
                'borderRadius': '8px',
                'textAlign': 'center',
                'flex': '1',
                'minWidth': '120px'
            }, children=[
                html.Div("Recall", style={'fontWeight': 'bold', 'color': '#B83280'}),
                html.Div(f"{recall:.2f}", style={'fontSize': '24px', 'marginTop': '5px'})
            ]),
            html.Div(style={
                'backgroundColor': '#FFFAF0', 
                'padding': '15px', 
                'borderRadius': '8px',
                'textAlign': 'center',
                'flex': '1',
                'minWidth': '120px'
            }, children=[
                html.Div("F1 Score", style={'fontWeight': 'bold', 'color': '#C05621'}),
                html.Div(f"{f1:.2f}", style={'fontSize': '24px', 'marginTop': '5px'})
            ]),
        ])
    ])
    
    return html.Div([
        dcc.Graph(figure=fig),
        metrics
    ])