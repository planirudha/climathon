import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
import pandas as pd
import numpy as np

st.markdown(
    """
    <div style="text-align: center;">
        <h1>Urban Shield 🛡️</h1>
        <h4>Shielding the economy of tomorrow</h4>
    </div>
    """,
    unsafe_allow_html=True
)

st.header("Climate is changing the world and will change your business. Are you prepared?")
st.write("""
The globe is changing faster and faster due to climate change. Industries must provide a healthy economic 
system while remaining competitive. Climate change effects, such as rising temperatures, changing rainfall patterns, 
and increased frequency of extreme weather events pose a significant risk to industries and businesses. 
Preparation and resilience planning are key to mitigating these risks. URBAN SHIELD products provide key insights for businesses.
""")

st.header("How heatproof is a location?")
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

# Create a choropleth map using go.Figure and Choroplethmapbox
fig = go.Figure(
    go.Choroplethmapbox(
        geojson=gdf_loaded.geometry.__geo_interface__,  # Use __geo_interface__ for GeoJSON
        locations=gdf_loaded.index,
        z=gdf_loaded['Temperature'],  # Use 'z' instead of 'color'
        colorscale=[
            [0, 'rgba(68, 1, 84, 0.3)'],   # Dark purple with 60% opacity
            [0.5, 'rgba(253, 231, 36, 0.3)'],  # Yellow with 60% opacity
            [1, 'rgba(253, 0, 0, 0.3)']    # Red with 60% opacity
        ],
        colorbar=dict(
            title="Heat Risk",
            tickvals=[14380, 14500, 14650],
            ticktext=["Low", "Medium", "High"]  # Customize labels as needed
        ),
        hovertemplate=hover_text,
    )
)

# Update layout with Mapbox settings
fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_zoom=11,
    mapbox_center={"lat": lat, "lon": lon},
    width=800,
    height=600,
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    coloraxis_colorbar=dict(
        title="Heat Risk",
        tickmode="array",
        tickvals=[14650, 14500, 14380],
        ticktext=[
            "High",
            "Medium",
            "Low",
        ],
    )

)


# Display the choropleth map in the Streamlit app
st.plotly_chart(fig)

# Hard-coded data for different cities
data = {
    "City": ["Darmstadt", "Mainz", "Arheilgen", "Griesheim", "Frankfurt"],
    "Internal Heat Risk": [7, 6, 5, 8, 9],
    "Internal Flood Risk": [5, 3, 4, 7, 2],
    "Internal Heavy Rain Risk": [6, 4, 5, 6, 3],
    "Internal Storm Risk": [4, 5, 7, 3, 6],
    "Internal Fire Risk": [2, 3, 4, 5, 6],
    "External Heat Risk": [6, 5, 4, 7, 8],
    "External Flood Risk": [4, 2, 3, 6, 1],
    "External Heavy Rain Risk": [5, 3, 4, 5, 2],
    "External Storm Risk": [3, 4, 6, 2, 5],
    "External Fire Risk": [1, 2, 3, 4, 5],
}

    
# Create a DataFrame
df = pd.DataFrame(data)



# Create DataFrames with random data for internal and external scenarios
# np.random.seed(42)  # For reproducible results
# df_internal = pd.DataFrame({
#     'category': ['heat risk', 'flood risk', 'heavy rain risk', 'storm risk', 'fire risk', 'heat risk'],
#     'value': [7, 5, 6, 7, 3, 7]
# })

# df_external = pd.DataFrame({
#     'category': ['heat risk', 'flood risk', 'heavy rain risk', 'storm risk', 'fire risk', 'heat risk'],
#     'value': [6, 4, 5, 6, 2, 6]
# })

# Title of the app
st.title("Environmental Risk Assessment - Internal vs External")


# Dropdown for selecting a city
selected_city = st.selectbox("Select a city:", df["City"])

# Filter the DataFrame based on the selected city
filtered_data = df[df["City"] == selected_city]

# Prepare data for internal and external polar plots
polar_data_internal = {
    "category": ["Heat Risk", "Flood Risk", "Heavy Rain Risk", "Storm Risk", "Fire Risk"],
    "value": filtered_data.iloc[0, 1:6].values  # Getting values for internal risks
}

polar_data_external = {
    "category": ["GHG emmission", "Hazard Risk", "Fire Risk", "Noise Risk", "Water Risk"],
    "value": filtered_data.iloc[0, 6:11].values  # Getting values for external risks
}

polar_df_internal = pd.DataFrame(polar_data_internal)
polar_df_external = pd.DataFrame(polar_data_external)

# Function to create a polar plot
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

# Apply color based on the maximum risk in the dataset for internal and external risks
internal_max_risk = polar_df_internal['value'].max()
external_max_risk = polar_df_external['value'].max()
polar_color_internal = get_color(internal_max_risk)
polar_color_external = get_color(external_max_risk)

# Create the polar plots for the selected city's risks
polar_fig_internal = create_polar_plot(polar_df_internal, f"Internal Environmental Risks for {selected_city}", polar_color_internal)
polar_fig_external = create_polar_plot(polar_df_external, f"External Environmental Risks for {selected_city}", polar_color_external)

# Create columns for polar plots to display them side by side
col1, col2 = st.columns(2)

# Display the polar plots in the Streamlit app
with col1:
    st.plotly_chart(polar_fig_internal)

with col2:
    st.plotly_chart(polar_fig_external)

st.markdown(
    """**🟥**: High Risk **🟨**: Medium Risk**🟩**: Low Risk
    """
)

st.header("The one side for businesses to mitigate climate risks: CLIMATAI")
st.write("""
CLIMATAI combines data from multiple sources to provide predictive insights about upcoming climate 
changes and their potential impacts. By incorporating data about specific industries and businesses, we can help 
economic leaders make informed, climate-proof decisions. We believe that making a business climate-resilient is 
making it future-proof. By preparing for the changes ahead, businesses can ensure their operations thrive and 
remain competitive in our changing world.
""")

st.write("""
---
""")

# Add your logo
logo_path = "logo.png"  # Replace with the path to your logo image
st.image(logo_path, width=200)

st.write("""
Made with Love from Inga, Leonard, Silvio, Anirudha and Paul in a night with very little sleep.
""")