import streamlit as st
import pandas as pd
import supabase
from supabase import create_client, Client
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import streamlit as st
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
def show_map():
    st.title("🗺️ Cultural Map")
    st.markdown("""
        <h2 style='color:#2c3e50;'>Explore India's Cultural Diversity</h2>
        <p style='font-size:16px;'>Discover the rich tapestry of festivals, food, and art across Indian states.</p>
    """, unsafe_allow_html=True)
    SUPABASE_URL = "https://ilbfnsqeymeohymvllyl.supabase.co"
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlsYmZuc3FleW1lb2h5bXZsbHlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAzMzk0NDIsImV4cCI6MjA2NTkxNTQ0Mn0.gKRFPn_ntqTg4kHta42c7Y2fgEnN8kGuBQFz3FP2IpA"
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    def load_table(table_name):
        try:
            response = supabase.table(table_name).select("*").execute()
            data = response.data
            if not data:
                st.warning(f"No data found in table '{table_name}'.")
                return pd.DataFrame()
            df = pd.DataFrame(data)
            # Do NOT convert columns to uppercase
            return df
        except Exception as e:
            st.error(f"Supabase error loading '{table_name}': {e}")
            return pd.DataFrame()

    # Load all datasets (all lowercase table names)
    festival_df = load_table("Indian_Festivals_By_State_With_Coordinates")
    food_df = load_table("food_unique")
    kdance_df = load_table("k_dance")
    st.sidebar.title("🌟 Explore India's Diversity")
    layer = st.sidebar.radio("Choose what to explore:", ["Festivals", "Food", "Art"])
    m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB positron")
    marker_cluster = MarkerCluster().add_to(m)

    if layer == "Festivals":
        st.markdown("""
            <h2 style='color:#FF5733;'>🎉 Indian Festivals Map</h2>
            <p style='font-size:16px;'>Explore the vibrant celebrations across Indian states, month-by-month!</p>
        """, unsafe_allow_html=True)

        for _, row in festival_df.iterrows():
            popup_content = f"""
            <div style='font-family: Arial, sans-serif; font-size: 14px;'>
                <h4 style='margin: 0; color: #8e44ad;'>{row['Month']}</h4>
                <b>Festival:</b> {row['Festival']}<br>
                <b>Description:</b> {row['Description']}<br>
            </div>
            """
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='red', icon='star')
            ).add_to(marker_cluster)

    elif layer == "Food":
        st.markdown("""
            <h2 style='color:#27ae60;'>🍽️ Indian Cuisine Highlights</h2>
            <p style='font-size:16px;'>Discover unique dishes and ingredients by region.</p>
        """, unsafe_allow_html=True)

        food_df = food_df.dropna(subset=["Latitude", "Longitude"])
        for _, row in food_df.iterrows():
            popup_content = f"""
            <div style='font-family: Arial, sans-serif; font-size: 14px;'>
                <h4 style='margin: 0; color: #c0392b;'>{row['name']}</h4>
                <b>State:</b> {row['state']}<br>
                <b>Ingredients:</b> {row['ingredients']}<br>
            </div>
            """
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(popup_content, max_width=300),
                icon=folium.Icon(color='green', icon='cutlery', prefix='fa')
            ).add_to(marker_cluster)

    elif layer == "Art":
        st.markdown("""
            <h2 style='color:#2980b9;'>🎼 Classical Arts Map</h2>
            <p style='font-size:16px;'>Experience the elegance of Kuchipudi and other cultural programs.</p>
        """, unsafe_allow_html=True)

        kdance_df = kdance_df.dropna(subset=["Latitude", "Longitude"])
        for _, row in kdance_df.iterrows():
            popup_content = f"""
            <div style='font-family: Arial, sans-serif; font-size: 14px;'>
                <h4 style='margin: 0; color: #34495e;'>{row['Name of the Programme']}</h4>
                <b>Troupe Leader:</b> {row['Name of the Troupe Leader']}<br>
                <b>Venue:</b> {row['Venue']}<br>
                <b>State:</b> {row['State']}<br>
                <b>Expenditure:</b> ₹{row['Expenditure']}<br>
            </div>
            """
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=folium.Popup(popup_content, max_width=350),
                icon=folium.Icon(color='blue', icon='music', prefix='fa')
            ).add_to(marker_cluster)
    st_folium(m, width=1000, height=600)
    st.markdown("""
        <div class="footer">
            © 2025 GeoBoost. All rights reserved.
        </div>
    """, unsafe_allow_html=True)
