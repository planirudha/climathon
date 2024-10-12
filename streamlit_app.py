import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np

st.title("Urben Sheild 🛡️ - Shielding the economy of tomorrow")

st.header("Climate is changing the world and will change your business. Are you prepared?")
st.write("""
The globe is changing faster and faster due to climate change. Industries must provide a healthy economic 
system while remaining competitive. Climate change effects, such as rising temperatures, changing rainfall patterns, 
and increased frequency of extreme weather events pose a significant risk to industries and businesses. 
Preparation and resilience planning are key to mitigating these risks. URBAN SHIELD products provide key insights for businesses.
""")
# Constants
total_points = 61
lat = 49.872833  # Input latitude
lon = 8.651222   # Input longitude

# Load GeoDataFrame and temperature data
gdf_loaded = gpd.read_file("shapes_temperatures_30_30.shp")
temperatures_loaded = pd.read_csv("temperatures_30_30.csv")

# Get the temperature data
temperatures_loaded = temperatures_loaded['Temperature'].to_list()

# Add the temperature data to the GeoDataFrame
gdf_loaded['Temperature'] = temperatures_loaded

hover_data = {'Temperature': total_points*[False]}

# Function to create hover text for choropleth map
def create_hover_label(value):
    if value > 14550:
        return "<b>High Risk</b>"
    elif 14550 >= value >= 14400:
        return "<b>Medium Risk</b>"
    else:
        return "<b>Low Risk</b>"

# Create hover text for temperatures
hover_text = [create_hover_label(val) for val in temperatures_loaded]
# Create choropleth map
fig_map = px.choropleth_map(
    gdf_loaded,
    geojson=gdf_loaded.geometry,
    locations=gdf_loaded.index,
    color='Temperature',
    color_continuous_scale="Viridis",
    opacity=0.3,
    hover_name=hover_text,
    hover_data={'Temperature': False},
    center={"lat": lat, "lon": lon}
)

# Update layout for color axis
fig_map.update_layout(
    coloraxis_colorbar=dict(
        title="Heat Risk",
        tickmode="array",
        tickvals=[14650, 14500, 14380],
        ticktext=["High", "Medium", "Low"],
    ),
    margin={"r":0, "t":0, "l":0, "b":0},
    title="Choropleth Map of Temperature Risk",
    height=600  # Set a specific height for the map
)
fig_map.show()
# Display the choropleth map in the Streamlit app
# st.plotly_chart(fig_map)

# Create DataFrames with random data for internal and external scenarios
np.random.seed(42)  # For reproducible results
df_internal = pd.DataFrame({
    'category': ['heat risk', 'flood risk', 'heavy rain risk', 'storm risk', 'fire risk', 'heat risk'],
    'value': [7, 5, 6, 7, 3, 7]
})

df_external = pd.DataFrame({
    'category': ['heat risk', 'flood risk', 'heavy rain risk', 'storm risk', 'fire risk', 'heat risk'],
    'value': [6, 4, 5, 6, 2, 6]
})

# Title of the app
st.title("Environmental Risk Assessment - Internal vs External")

# # Sidebar sliders for risk adjustment
# st.sidebar.header("Adjust Risk Levels")
# risk_adjustment_internal = st.sidebar.slider("Internal Risk Adjustment", -3, 3, 0, 1)
# risk_adjustment_external = st.sidebar.slider("External Risk Adjustment", -3, 3, 0, 1)

# # Adjust values based on sidebar input
# df_internal['value'] += risk_adjustment_internal
# df_external['value'] += risk_adjustment_external

# Function to create a polar plot with color-coding for risk levels
def create_polar_plot(df, title, color):
    fig = go.Figure(go.Scatterpolar(
        r=df['value'],
        theta=df['category'],
        fill='toself',
        name='Risk',
        marker=dict(color=color)  # Adding color to the trace
    ))

    # Update the layout
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        title=title,
        showlegend=False,
        height=400  # Set a specific height for the polar plots
    )

    return fig

# Function to determine color based on risk level
def get_color(value):
    if value >= 7:
        return 'red'  # High risk
    elif value >= 4:
        return 'yellow'  # Medium risk
    else:
        return 'green'  # Low risk

# Apply color based on the maximum risk in the dataset
internal_color = get_color(df_internal['value'].max())
external_color = get_color(df_external['value'].max())

# Create two polar plots
fig_internal = create_polar_plot(df_internal, "Internal Risks with Adjustments", internal_color)
fig_external = create_polar_plot(df_external, "External Risks with Adjustments", external_color)

# Create columns for polar plots to display them side by side
col1, col2 = st.columns(2)

# Display the polar plots in the Streamlit app
with col1:
    st.plotly_chart(fig_internal)

with col2:
    st.plotly_chart(fig_external)
