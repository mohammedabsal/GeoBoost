import streamlit as st
from supabase import create_client, Client
import pandas as pd
def show_artforms():
    st.markdown("<h1 style='text-align:center;'>🎨 Art Forms Exploration</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>✨ Explore various art forms and their ORIGINs. Use the filters to discover hidden gems! ✨</p>", unsafe_allow_html=True)
    st.markdown("---")
    SUPABASE_URL = st.secrets["SUPABASE_URL"]
    SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    # Load Data
    @st.cache_data
    def load_data():
        try:
            response = supabase.table("artist").select("*").execute()
            data = response.data
            if not data:
                return pd.DataFrame()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Supabase error: {e}")
            return pd.DataFrame()

    data = load_data()
    if data.empty:
        st.warning("No artworks found in the database.")
        return
    # Sidebar Filters
    st.sidebar.header("🔎 Filter Artworks")
    art_form = st.sidebar.multiselect("🖼️ Art Form", options=data['title'].unique(), default=list(data['title'].unique()))
    region = st.sidebar.multiselect("🗺️ Region", options=data['origin'].unique(), default=list(data['origin'].unique()))
    artist = st.sidebar.multiselect("👩‍🎨 ARTIST", options=data['artist'].unique(), default=list(data['artist'].unique()))
    search_query = st.text_input("🔍 Search Artworks", "")

    # Filter Data
    filtered_data = data[
        data['title'].isin(art_form) &
        data['origin'].isin(region) &
        data['artist'].isin(artist)
    ]
    if search_query:
        filtered_data = filtered_data[filtered_data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]

    if filtered_data.empty:
        st.warning("😕 No artworks match the selected filters or search query.")
    else:
        st.markdown("#### 🖼️ Artworks Gallery")
        for index, row in filtered_data.iterrows():
            with st.container():
                cols = st.columns([1, 2])
                with cols[0]:
                    img_url = row['image_url']
                    if isinstance(img_url, str) and img_url.strip().startswith('http'):
                        st.image(img_url, caption=row['title'])
                    else:
                        st.warning("No image available.")
                with cols[1]:
                    st.markdown(f"**🎨 Art Form:** {row['title']}")
                    st.markdown(f"**👩‍🎨 ARTIST:** {row['artist']}")
                    st.markdown(f"**🗺️ Region:** {row['origin']}")
                    st.markdown(f"**📝 DESCRIPTION:** {row['description']}")
                    if st.button(f"▶️ Watch Video: {row['title']}", key=f"video_{index}"):
                        vid_url = row['video_url']
                        if isinstance(vid_url, str) and vid_url.strip().startswith('http'):
                            st.video(vid_url)
                        else:
                            st.warning("No video available.")
                st.markdown("---")

    # Responsive Design
    st.markdown("""
        <style>
            @media (max-width: 900px) {
                .stImage {
                    width: 100% !important;
                }
            }
            .stButton>button {
                background-color: #f0ad4e;
                color: white;
                border-radius: 8px;
                margin-top: 8px;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            © 2025 GeoBoost. All rights reserved.
        </div>
    """, unsafe_allow_html=True)