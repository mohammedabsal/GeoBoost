import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import requests
import snowflake.connector
def show_visit():
    # Load Lottie animations
    @st.cache_data
    def load_lottie_url(url: str):
        response = requests.get(url)
        if response.status_code != 200:
            return None
        return response.json()

    travel_animation = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_5ngs2ksb.json")
    eco_friendly_animation = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json")
    support_locals_animation = load_lottie_url("https://lottie.host/771f24c4-f1d8-4119-8996-97da110c9dbc/5vAAmTcgZJ.json")

    # Inject custom CSS
    st.markdown("""
        <style>
        body {
            background-color: #f0f2f6;
        }
        .visit-card {
            background: linear-gradient(135deg, #EAF6F6 0%, #d7f0d7 100%);
            border-radius: 20px;
            padding: 1.5em;
            margin: 1.5em 0;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .visit-card:hover {
            transform: scale(1.02);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.15);
        }
        .visit-section-title {
            font-size: 1.5em;
            font-weight: 600;
            color: #2C3E50;
            margin-bottom: 0.3em;
        }
        .visit-section-content {
            font-size: 1.1em;
            color: #4A4A4A;
            margin-top: 0.3em;
        }
        @media screen and (max-width: 900px) {
            .stColumns {flex-direction: column;}
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 style='text-align:center; color:#117A65;'>🌿 Responsible Tourism Guide</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align:center; font-size:18px;'>
        Discover how to travel mindfully 🌏<br>
        Support local communities, preserve traditions, and reduce your footprint.<br>
        <span style='color:#117A65;'>Pick a destination to start your eco-journey!</span>
        </div>
        <hr>
    """, unsafe_allow_html=True)

    # Load data
    conn = snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )
    query = "SELECT * FROM TIMETOVISIT"
    data = pd.read_sql(query, conn)
    # Sidebar
    if travel_animation:
        st_lottie(travel_animation, height=180, key="travel_animation")
        st.header("🌍 Explore India Mindfully")
        st.markdown("Select a state or city below:")

    states = data['STATE_CITY'].unique()
    selected_state = st.selectbox("📍 Choose your destination", states)

    info = data[data['STATE_CITY'] == selected_state].iloc[0]

    # Main Content Sections
    st.markdown(f"<div class='visit-card'><div class='visit-section-title'>📍 Destination: <span style='color:#117A65;'>{selected_state}</span></div>", unsafe_allow_html=True)

    # Best Time to Visit
    col1, col2 = st.columns([1, 2])
    with col1:
        if eco_friendly_animation:
            st_lottie(eco_friendly_animation, height=120, key="eco_friendly_animation")
    with col2:
        st.markdown(f"""
            <div class='visit-section-title'>🗓️ Best Time to Visit</div>
            <div class='visit-section-content'>{info['BEST_TIME_TO_VISIT']}</div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Support Locals
    st.markdown("<div class='visit-card'>", unsafe_allow_html=True)
    col3, col4 = st.columns([2, 1])
    with col3:
        st.markdown(f"""
            <div class='visit-section-title'>🧺 How to Support Locals</div>
            <div class='visit-section-content'>{info['SUPPORT_LOCALS']}</div>
        """, unsafe_allow_html=True)
    with col4:
        if support_locals_animation:
            st_lottie(support_locals_animation, height=120, key="support_locals_animation")
    st.markdown("</div>", unsafe_allow_html=True)

    # Cultural Etiquette & Eco Practices
    st.markdown("<div class='visit-card'>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class='visit-section-title'>🙏 Cultural Etiquette</div>
        <div class='visit-section-content'>{info['CULTURAL_ETIQUETTE']}</div>
        <div class='visit-section-title' style='margin-top:1em;'>🌱 Eco-Friendly Tips</div>
        <div class='visit-section-content'>{info['ECO_FRIENDLY']}</div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            © 2025 GeoBoost. All rights reserved.
        </div>
    """, unsafe_allow_html=True)