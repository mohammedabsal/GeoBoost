import streamlit as st
import pandas as pd

def show_artforms():
    st.markdown("<h1 style='text-align:center;'>🎨 Art Forms Exploration</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>✨ Explore various art forms and their origins. Use the filters to discover hidden gems! ✨</p>", unsafe_allow_html=True)
    st.markdown("---")

    data = pd.read_csv('data/artist.csv')

    # Sidebar Filters
    st.sidebar.header("🔎 Filter Artworks")
    art_form = st.sidebar.multiselect("🖼️ Art Form", options=data['title'].unique(), default=data['title'].unique())
    region = st.sidebar.multiselect("🗺️ Region", options=data['origin'].unique(), default=data['origin'].unique())
    artist = st.sidebar.multiselect("👩‍🎨 Artist", options=data['artist'].unique(), default=data['artist'].unique())
    search_query = st.text_input("🔍 Search Artworks", "")

    # Filter Data
    filtered_data = data[
        (data['title'].isin(art_form)) &
        (data['origin'].isin(region)) &
        (data['artist'].isin(artist)) &
        (data.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1) if search_query else True)
    ]

    if filtered_data.empty:
        st.warning("😕 No artworks match the selected filters or search query.")
    else:
        st.markdown("#### 🖼️ Artworks Gallery")
        for index, row in filtered_data.iterrows():
            with st.container():
                cols = st.columns([1, 2])
                with cols[0]:
                    st.image(row['image_url'], caption=row['title'], use_container_width=True)
                with cols[1]:
                    st.markdown(f"**🎨 Art Form:** {row['title']}")
                    st.markdown(f"**👩‍🎨 Artist:** {row['artist']}")
                    st.markdown(f"**🗺️ Region:** {row['origin']}")
                    st.markdown(f"**📝 Description:** {row['description']}")
                    if st.button(f"▶️ Watch Video: {row['title']}", key=f"video_{index}"):
                        st.video(row['video_url'])
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