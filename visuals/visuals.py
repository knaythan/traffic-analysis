import os
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import HeatMap

# Reusable visual components
def severity_distribution(output_dir="output"):
    output_file = f"{output_dir}/severity_distribution.html"
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping...")
        return
    severity_counts = df["Severity"].value_counts().sort_index()
    fig = px.bar(x=severity_counts.index, y=severity_counts.values,
                 labels={'x': 'Severity Level', 'y': 'Number of Accidents'},
                 title='Accident Severity Distribution')
    fig.write_html(output_file)
    return fig

def feature_correlation(output_dir="output"):
    output_file = f"{output_dir}/feature_correlation.html"
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping...")
        return
    print("Generating feature correlation heatmap...")
    corr_matrix = df.select_dtypes(include='number').corr()
    fig = px.imshow(corr_matrix, text_auto=True,
                    color_continuous_scale='Viridis',
                    title='Feature Correlation Heatmap')
    fig.write_html(output_file)
    return fig

# def precipitation_vs_severity(output_dir="output"):
#     output_file = f"{output_dir}/precipitation_vs_severity.html"
#     if os.path.exists(output_file):
#         print(f"{output_file} already exists. Skipping...")
#         return
#     if "Precipitation(in)" not in df.columns or "Severity" not in df.columns:
#         print("Required columns 'Precipitation(in)' or 'Severity' are missing in the dataset. Skipping...")
#         return
#     fig = px.scatter(df, x="Precipitation(in)", y="Severity", log_x=True,
#                      title="Precipitation vs Severity (Log Scale)",
#                      labels={"Precipitation(in)": "Precipitation (in)", "Severity": "Severity"})
#     fig.write_html(output_file)
#     return fig

def precipitation_vs_severity(output_dir="output"):
    output_file = f"{output_dir}/precipitation_vs_severity.html"
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping...")
        return
    if "Precipitation(in)" not in df.columns or "Severity" not in df.columns:
        print("Required columns 'Precipitation(in)' or 'Severity' are missing in the dataset. Skipping...")
        return

    print("Preprocessing data for optimized rendering...")

    # Step 1: Drop NaNs
    temp_df = df[["Precipitation(in)", "Severity"]].dropna()

    # Step 2: Binning precipitation values (log-friendly)
    temp_df["PrecipBin"] = pd.cut(temp_df["Precipitation(in)"], 
                                   bins=[0, 0.01, 0.1, 0.5, 1, 2, 5, 10], 
                                   include_lowest=True)

    # Step 3: Aggregate by bin + severity
    agg_df = temp_df.groupby(["PrecipBin", "Severity"]).size().reset_index(name="Count")
    agg_df["PrecipMid"] = agg_df["PrecipBin"].apply(lambda x: x.mid)

    # Step 4: Plot aggregated points
    fig = px.scatter(agg_df, x="PrecipMid", y="Severity", size="Count", 
                     title="Precipitation vs Severity (Binned, Log Scale)",
                     labels={"PrecipMid": "Precipitation (in)", "Severity": "Severity"},
                     log_x=True, size_max=40)

    # Step 5: Save with external JS
    fig.write_html(output_file, include_plotlyjs='cdn')
    print(f"Optimized plot saved to {output_file}")
    return fig

def accidents_by_state(output_dir="output"):
    output_file = f"{output_dir}/accidents_by_state.html"
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping...")
        return
    state_counts = df["State"].value_counts().sort_values(ascending=False)
    fig = px.bar(x=state_counts.index, y=state_counts.values,
                 labels={'x': 'State', 'y': 'Number of Accidents'},
                 title='Accident Distribution by State')
    fig.write_html(output_file)
    return fig

def accident_heatmap(output_dir="output"):
    output_file = f"{output_dir}/accident_heatmap.html"
    if os.path.exists(output_file):
        print(f"{output_file} already exists. Skipping...")
        return
    try:
        df_map = df[["Start_Lat", "Start_Lng"]].dropna()
        if len(df_map) > 3000000:
            df_map = df_map.sample(n=3000000, random_state=42)
        m = folium.Map(location=[37.8, -96], zoom_start=5, tiles="CartoDB Voyager")
        marker_cluster = folium.plugins.MarkerCluster().add_to(m)
        for lat, lng in df_map.values:
            folium.Marker(location=[lat, lng]).add_to(marker_cluster)
        m.save(output_file)
        return m
    except Exception as e:
        print(f"Error rendering heatmap: {str(e)}")
        return None

# Example usage
if __name__ == "__main__":
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Load your dataset here
    # Replace 'your_dataset.csv' with the actual path to your dataset
    df = pd.read_csv("../data/us_accidents.csv")

    # Generate and save visuals
    severity_distribution(output_dir)
    feature_correlation(output_dir)
    precipitation_vs_severity(output_dir)
    accidents_by_state(output_dir)
    accident_heatmap(output_dir)