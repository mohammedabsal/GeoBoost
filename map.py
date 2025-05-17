import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import streamlit as st
def show_map():
    st.title("🗺️ Cultural Map")
    st.markdown("""
        <h2 style='color:#2c3e50;'>Explore India's Cultural Diversity</h2>
        <p style='font-size:16px;'>Discover the rich tapestry of festivals, food, and art across Indian states.</p>
    """, unsafe_allow_html=True)
    festival_df = pd.read_csv("data/Indian_Festivals_By_State_With_Coordinates.csv")
    food_df = pd.read_csv("data/foods_unique.csv")
    kdance_df = pd.read_csv("data/k_dance.csv")

    # Sidebar controls
    st.sidebar.title("🌟 Explore India's Diversity")
    layer = st.sidebar.radio("Choose what to explore:", ["Festivals", "Food", "Art"])

    # Base map setup
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

    # Render map
    st_folium(m, width=1000, height=600)

    # Footer animation using Lottie
    st.markdown("""
        <hr>
        <center><h4 style='color:gray;'>Made with ❤️ by Team GeoBoost</h4></center>
    """, unsafe_allow_html=True)