"""
South Africa Data Dashboard
===========================

Interactive dashboard showing unemployment and education trends.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="South Africa Data Dashboard",
    page_icon="🇿🇦",
    layout="wide"
)

# Title
st.title("🇿🇦 South Africa - Unemployment & Education Dashboard")
st.markdown("### World Bank Development Indicators (1991-2023)")

@st.cache_data
def load_data():
    """Load data from CSV file."""
    # Try different possible paths
    possible_paths = [
        Path('data/processed/south_africa_combined.csv'),
        Path('../data/processed/south_africa_combined.csv'),
        Path('..') / 'data' / 'processed' / 'south_africa_combined.csv',
        Path('/mount/src/south-africa-data-analysis/data/processed/south_africa_combined.csv')
    ]
    
    df = None
    for path in possible_paths:
        if path.exists():
            df = pd.read_csv(path)
            break
    
    if df is None:
        st.error("Data file not found. Please check the data path.")
        return None
    
    # Rename columns to match database format
    df = df.rename(columns={
        'Year': 'year',
        'Unemployment_Rate': 'unemployment_rate',
        'Tertiary_Enrolment': 'tertiary_enrolment'
    })
    
    return df

df = load_data()

if df is None:
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

# Year range filter
year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# Filter data
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# Main dashboard - Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Avg Unemployment",
        f"{filtered_df['unemployment_rate'].mean():.1f}%",
        f"{filtered_df['unemployment_rate'].mean() - df['unemployment_rate'].mean():.1f}% vs overall"
    )

with col2:
    st.metric(
        "Avg Tertiary Enrolment",
        f"{filtered_df['tertiary_enrolment'].mean():.1f}%",
        f"{filtered_df['tertiary_enrolment'].mean() - df['tertiary_enrolment'].mean():.1f}% vs overall"
    )

with col3:
    latest_year = filtered_df['year'].max()
    latest_unemployment = filtered_df[filtered_df['year'] == latest_year]['unemployment_rate'].values[0]
    st.metric(
        f"Latest Unemployment ({latest_year})",
        f"{latest_unemployment:.1f}%"
    )

with col4:
    latest_enrolment = filtered_df[filtered_df['year'] == latest_year]['tertiary_enrolment'].values[0]
    st.metric(
        f"Latest Enrolment ({latest_year})",
        f"{latest_enrolment:.1f}%"
    )

# Charts
st.markdown("---")
st.subheader("Trends Over Time")

col1, col2 = st.columns(2)

with col1:
    # Unemployment trend
    fig1 = px.line(
        filtered_df, 
        x='year', 
        y='unemployment_rate',
        title='Unemployment Rate',
        labels={'year': 'Year', 'unemployment_rate': 'Rate (%)'},
        markers=True
    )
    fig1.update_traces(line_color='#2E86C1', marker_color='#2E86C1')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    # Education trend
    fig2 = px.line(
        filtered_df, 
        x='year', 
        y='tertiary_enrolment',
        title='Tertiary Enrolment Rate',
        labels={'year': 'Year', 'tertiary_enrolment': 'Rate (%)'},
        markers=True
    )
    fig2.update_traces(line_color='#28B463', marker_color='#28B463')
    st.plotly_chart(fig2, use_container_width=True)

# Combined chart
st.subheader("Unemployment vs Tertiary Enrolment")

fig3 = go.Figure()
fig3.add_trace(go.Scatter(
    x=filtered_df['year'],
    y=filtered_df['unemployment_rate'],
    name='Unemployment',
    mode='lines+markers',
    line=dict(color='#2E86C1', width=2),
    marker=dict(size=8)
))
fig3.add_trace(go.Scatter(
    x=filtered_df['year'],
    y=filtered_df['tertiary_enrolment'],
    name='Tertiary Enrolment',
    mode='lines+markers',
    line=dict(color='#28B463', width=2),
    marker=dict(size=8)
))
fig3.update_layout(
    title='Unemployment and Tertiary Enrolment (1991-2023)',
    xaxis_title='Year',
    yaxis_title='Rate (%)',
    hovermode='x unified'
)
st.plotly_chart(fig3, use_container_width=True)

# Scatter plot with manual trendline
st.subheader("Relationship: Education vs Unemployment")

# Calculate manual trendline
x = filtered_df['tertiary_enrolment'].values
y = filtered_df['unemployment_rate'].values

# Simple linear regression
x_mean = np.mean(x)
y_mean = np.mean(y)
slope = np.sum((x - x_mean) * (y - y_mean)) / np.sum((x - x_mean) ** 2)
intercept = y_mean - slope * x_mean

# Create trendline points
x_range = np.linspace(x.min(), x.max(), 100)
y_trend = slope * x_range + intercept

# Create scatter plot with manual trendline
fig4 = go.Figure()

# Scatter points
fig4.add_trace(go.Scatter(
    x=x,
    y=y,
    mode='markers+text',
    text=filtered_df['year'].astype(str),
    textposition='top center',
    name='Data Points',
    marker=dict(size=12, color='#2E86C1')
))

# Trendline
fig4.add_trace(go.Scatter(
    x=x_range,
    y=y_trend,
    mode='lines',
    name=f'Trendline (R² = 0.69)',
    line=dict(color='red', width=2)
))

fig4.update_layout(
    title=f'Education vs Unemployment (Correlation: {np.corrcoef(x, y)[0, 1]:.3f})',
    xaxis_title='Tertiary Enrolment (%)',
    yaxis_title='Unemployment Rate (%)',
    hovermode='closest'
)
st.plotly_chart(fig4, use_container_width=True)

# Data table
st.subheader("Data Table")
st.dataframe(
    filtered_df,
    column_config={
        "year": "Year",
        "unemployment_rate": st.column_config.NumberColumn("Unemployment Rate", format="%.2f%%"),
        "tertiary_enrolment": st.column_config.NumberColumn("Tertiary Enrolment", format="%.2f%%")
    },
    hide_index=True,
    use_container_width=True
)

# Download button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name="south_africa_data.csv",
    mime="text/csv"
)

# Correlation info
st.subheader("Key Statistics")
col1, col2, col3 = st.columns(3)

with col1:
    corr = np.corrcoef(filtered_df['tertiary_enrolment'], filtered_df['unemployment_rate'])[0, 1]
    st.metric("Correlation", f"{corr:.3f}", help="Pearson correlation coefficient")

with col2:
    st.metric("Total Years", len(filtered_df))

with col3:
    st.metric("Data Range", f"{filtered_df['year'].min()} - {filtered_df['year'].max()}")

# Footer
st.markdown("---")
st.caption("Data Source: World Bank Development Indicators")
st.caption("Built with Streamlit | South Africa Data Analysis Project")