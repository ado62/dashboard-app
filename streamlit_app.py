import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from pathlib import Path

# Page config
st.set_page_config(page_title="CSV Dashboard", layout="wide")

# Title
st.title("📊 CSV Dashboard")
st.write("Python dashboard reading CSV source data with charts, tables, map, and logs.")

# Load data
@st.cache_data
def load_data():
    csv_path = Path(__file__).parent / "data" / "sample_data.csv"
    return pd.read_csv(csv_path)

@st.cache_data
def load_logs():
    log_path = Path(__file__).parent / "data" / "sample_logs.csv"
    return pd.read_csv(log_path)

df = load_data()
logs_df = load_logs()

# Overview metrics
st.divider()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Records", len(df))
col2.metric("Unique Categories", df["category"].nunique())
col3.metric("Unique Regions", df["region"].nunique())
col4.metric("Average Value", f"{df['value'].mean():.0f}")

# Charts & Table
st.divider()
tab1, tab2, tab3, tab4 = st.tabs(["📈 Trend", "🗺️ Map", "📋 Table", "📝 Logs"])

with tab1:
    # Time-series chart
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    daily_data = df.dropna(subset=["date", "value"]).groupby("date")["value"].sum().reset_index()
    if len(daily_data) > 0:
        fig = px.line(
            daily_data,
            x="date",
            y="value",
            title="Value trend over time",
            markers=True,
            line_shape="linear",
        )
        fig.update_layout(hovermode="x unified", height=400)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No date/value data available")

with tab2:
    # Map
    points = df.dropna(subset=["latitude", "longitude"])
    if len(points) > 0:
        center_lat = points["latitude"].mean()
        center_lon = points["longitude"].mean()
        
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=4,
            tiles="OpenStreetMap"
        )
        
        for _, row in points.iterrows():
            folium.CircleMarker(
                location=[row["latitude"], row["longitude"]],
                radius=8,
                popup=f"{row['region']}<br>{row['category']}<br>Value: {row['value']}",
                color="#2563eb",
                fill=True,
                fillColor="#93c5fd",
                fillOpacity=0.8,
            ).add_to(m)
        
        st_folium(m, width=700, height=500)
    else:
        st.info("No location data (latitude/longitude) available")

with tab3:
    # Data table
    st.subheader("Data Preview")
    display_cols = ["date", "category", "region", "value", "note"]
    st.dataframe(df[display_cols], use_container_width=True, height=400)
    
    st.write(f"**Total rows:** {len(df)}")

with tab4:
    # Logs
    st.subheader("System Logs")
    if len(logs_df) > 0:
        for _, log in logs_df.iterrows():
            level_color = {
                "INFO": "ℹ️",
                "WARN": "⚠️",
                "ERROR": "❌",
            }.get(log["level"], "📌")
            st.write(f"**{level_color} {log['timestamp']}** — `{log['level']}`")
            st.write(f"*{log['source']}*: {log['message']}")
            st.divider()
    else:
        st.info("No logs available")
