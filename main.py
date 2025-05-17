import streamlit as st

st.set_page_config(
    page_title="GeoBoost Cultural Explorer",
    page_icon="🌏",
    layout="wide",
    initial_sidebar_state="expanded"
)
from map import show_map
from dash import show_dashboard
from gallery import show_gallery 
from artforms import show_artforms 
from visit import show_visit
from storyteller import show_storyteller

# Sidebar navigation
page= st.sidebar.selectbox(
    "Select a page",
    ["🏠 Home", "Tourism Dashboard", "Map", "gallery", "Art Forms", "Responsible Tourism Tips", "Story"
     ],
    index=0
)
# Set custom CSS for the sidebar
st.markdown(
    """
    <style>

    .sidebar .sidebar-content {

        background: linear-gradient(135deg, #FDEB71 0%, #F8D800 100%);
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .sidebar .sidebar-content h1 {


        font-size: 24px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;

    }
    .sidebar .sidebar-content h2 {

        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;

        margin-bottom: 10px;
    }
    .sidebar .sidebar-content p {
        font-size: 16px;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content a {
        color: #2c3e50;
        text-decoration: none;
        font-weight: bold;
        font-size: 16px;
        text-align: center;
        display: block;
        margin: 10px 0;
    }
    .sidebar .sidebar-content a:hover {

        text-decoration: underline;
        color: #2980b9;
    }
    .sidebar .sidebar-content button {
        background-color: #2980b9;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
        text-align: center;
    }
    .sidebar .sidebar-content button:hover {
        background-color: #3498db;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        margin-top: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True  
)

if page == "🏠 Home":
    # Banner image (replace with your own if desired)
    st.image("https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    st.markdown(
        "<h1 style='text-align:center; color:#2E86C1;'>🌏 Welcome to GeoBoost Cultural Explorer!</h1>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; font-size:20px;'>Discover India's tourism trends, vibrant art forms, and cultural richness.<br>Navigate through our features to explore, learn, and get inspired!</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Features grid
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=80)
        st.markdown("### 📊 Tourism Dashboard")
        st.markdown("Get insights into India's tourism trends with interactive charts and data.")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/684/684908.png", width=80)
        st.markdown("### 🗺️ Interactive Map")
        st.markdown("Explore destinations and cultural hotspots on an interactive map.")

    with col3:
        st.image("https://cdn-icons-png.flaticon.com/512/1823/1823493.png", width=80)
        st.markdown("### 🖼️ Art Gallery")
        st.markdown("Browse a curated gallery of traditional and modern Indian art forms.")

    st.markdown("---")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.image("https://cdn-icons-png.flaticon.com/512/3469/3469100.png", width=80)
        st.markdown("### 🎨 Art Forms")
        st.markdown("Dive deep into the origins and stories behind various Indian art forms.")

    with col5:
        st.image("https://cdn-icons-png.flaticon.com/512/3062/3062634.png", width=80)
        st.markdown("### 🌱 Responsible Tourism Tips")
        st.markdown("Learn how to travel responsibly and support local communities.")

    with col6:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=80)
        st.markdown("### 📖 AI Storyteller")
        st.markdown("Generate personalized cultural stories powered by AI.")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; font-size:18px; color:#117A65;'>"
        "✨ Start exploring using the navigation menu on the left! ✨"
        "</div>",
        unsafe_allow_html=True
    )

elif page == "Tourism Dashboard":
    show_dashboard()
elif page == "Map":
    show_map()
elif page == "gallery":
    show_gallery()
elif page == "Art Forms":
    show_artforms()
elif page == "Responsible Tourism Tips":
    show_visit()
elif page == "Story":
    show_storyteller()