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
    # Background banner with fade-in effect
    st.markdown("""
        <style>
            .fade-in {
                animation: fadeIn 2s ease-in-out;
            }
            @keyframes fadeIn {
                0% {opacity: 0;}
                100% {opacity: 1;}
            }
            .feature-box:hover {
                transform: scale(1.05);
                transition: transform 0.3s ease-in-out;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            }
            .footer {
                margin-top: 50px;
                padding: 20px 0;
                text-align: center;
                color: #888;
                font-size: 14px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap');
.video-container {
    position: relative;
    width: 100%;
    height: 500px;
    overflow: hidden;
    border-radius: 12px;
    margin-bottom: 1rem;
}

.video-container video {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.overlay-text {
    font-family: 'Great Vibes', cursive;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    font-size: 48px;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
    border-right: .15em solid white;
    animation: typing 4s steps(40, end), blink-caret 0.75s step-end infinite;
}

@keyframes typing {
    from { width: 0 }
    to { width: 66% }
}

@keyframes blink-caret {
    from, to { border-color: transparent }
    50% { border-color: white }
}
</style>

<div class="video-container">
    <video autoplay loop muted playsinline>
        <source src="https://raw.githubusercontent.com/mohammedabsal/GeoBoost/main/assest/video_1.mp4" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    <div class="overlay-text">GeoBoost Cultural Explorer</div>
</div>
""",
unsafe_allow_html=True
)

    # Title with fade-in effect
    
    st.markdown("<h1 class='fade-in' style='text-align:center; color:#2E86C1;'>Welcome to GeoBoost Cultural Explorer!</h1>", unsafe_allow_html=True)
    
    st.markdown(
        "<p class='fade-in' style='text-align:center; font-size:20px;'>Discover India's tourism trends, vibrant art forms, and cultural richness.<br>Navigate through our features to explore, learn, and get inspired!</p>",
        unsafe_allow_html=True
    )

    st.markdown("----")

    # Features section with slight animations
    features = [
        {
            "img": "https://cdn-icons-png.flaticon.com/512/854/854878.png",
            "title": "📊 Tourism Dashboard",
            "desc": "Get insights into India's tourism trends with interactive charts and real-time data."
        },
        {
            "img": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
            "title": "🗺️ Interactive Map",
            "desc": "Discover destinations and cultural hotspots with a visual experience."
        },
        {
            "img": "https://cdn-icons-png.flaticon.com/512/1823/1823493.png",
            "title": "🖼️ Art Gallery",
            "desc": "Browse a handpicked gallery of traditional and modern Indian art."
        },
        {
            "img": "https://cdn-icons-png.flaticon.com/512/3469/3469100.png",
            "title": "🎨 Art Forms",
            "desc": "Explore the origins and evolution of iconic Indian art forms."
        },
        {
            "img": "https://cdn-icons-png.flaticon.com/512/3062/3062634.png",
            "title": "🌱 Responsible Tourism",
            "desc": "Learn travel ethics and how to support sustainability and local communities."
        },
        {
            "img": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "title": "📖 AI Storyteller",
            "desc": "Generate your own personalized cultural journey using AI storytelling."
        },
    ]

    for i in range(0, len(features), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(features):
                with cols[j]:
                    st.markdown(f"""
                        <div class="feature-box" style="text-align: center; padding: 20px;">
                            <img src="{features[i + j]['img']}" width="80" style="margin-bottom: 10px;">
                            <h4>{features[i + j]['title']}</h4>
                            <p style="font-size: 16px; color: #555;">{features[i + j]['desc']}</p>
                        </div>
                    """, unsafe_allow_html=True)

    st.markdown("---")

    # Call-to-action
    st.markdown(
        "<div style='text-align:center; font-size:18px; color:#117A65;'>"
        "✨ Use the sidebar to start your cultural adventure now! ✨"
        "</div>",
        unsafe_allow_html=True
    )

    # Footer
    st.markdown("""
        <div class="footer">
            © 2025 GeoBoost. All rights reserved.
        </div>
    """, unsafe_allow_html=True)


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