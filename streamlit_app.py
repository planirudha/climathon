import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Erstelle einen DataFrame mit zufälligen Daten für zwei Szenarien: intern und extern
np.random.seed(42)  # Für reproduzierbare Ergebnisse
df_internal = pd.DataFrame({
    'category': ['heat risk', 'flood risk', 'heavy rain risk', 'storm risk', 'fire risk', 'heat risk'],
    'value': [7, 5, 6, 7, 3, 7],
    'temperature': np.random.uniform(25, 35, 6),
    'precipitation': np.random.uniform(50, 150, 6),
    'wind': np.random.uniform(10, 30, 6)
})

df_external = pd.DataFrame({
    'category': ['heat risk', 'flood risk', 'heavy rain risk', 'storm risk', 'fire risk', 'heat risk'],
    'value': [6, 4, 5, 6, 2, 6],
    'temperature': np.random.uniform(20, 30, 6),
    'precipitation': np.random.uniform(40, 120, 6),
    'wind': np.random.uniform(15, 25, 6)
})

# Title of the app
st.title("Environmental Risk Assessment - Internal vs External")

# Sidebar sliders for additional parameters (Temperature, Precipitation, Wind)
st.sidebar.header("Adjust Parameters")

temperature_adjustment = st.sidebar.slider("Temperature Adjustment (°C)", -5.0, 5.0, 0.0, 0.1)
precipitation_adjustment = st.sidebar.slider("Precipitation Adjustment (%)", -50, 50, 0, 1)
wind_adjustment = st.sidebar.slider("Wind Adjustment (km/h)", -10, 10, 0, 1)

# Adjusting values based on sidebar input
df_internal['temperature'] += temperature_adjustment
df_internal['precipitation'] *= (1 + precipitation_adjustment / 100)
df_internal['wind'] += wind_adjustment

df_external['temperature'] += temperature_adjustment
df_external['precipitation'] *= (1 + precipitation_adjustment / 100)
df_external['wind'] += wind_adjustment

# Function to create a polar plot
def create_polar_plot(df, title):
    fig = go.Figure(go.Scatterpolar(
        r=df['value'],
        theta=df['category'],
        fill='toself',
        name='Risk'
    ))

    # Additional traces for temperature, precipitation, wind
    fig.add_trace(go.Scatterpolar(
        r=df['temperature'],
        theta=df['category'],
        fill='none',
        name='Temperature'
    ))

    fig.add_trace(go.Scatterpolar(
        r=df['precipitation'],
        theta=df['category'],
        fill='none',
        name='Precipitation'
    ))

    fig.add_trace(go.Scatterpolar(
        r=df['wind'],
        theta=df['category'],
        fill='none',
        name='Wind'
    ))

    # Update the layout
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title=title
    )

    return fig

# Create two polar plots
fig_internal = create_polar_plot(df_internal, "Internal Risks with Adjustments")
fig_external = create_polar_plot(df_external, "External Risks with Adjustments")

# Display the polar plots in the Streamlit app
st.plotly_chart(fig_internal)
st.plotly_chart(fig_external)

