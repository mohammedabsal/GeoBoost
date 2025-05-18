import streamlit as st
import snowflake.connector
import pandas as pd

def show_artforms():
    st.markdown("<h1 style='text-align:center;'>🎨 Art Forms Exploration</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>✨ Explore various art forms and their ORIGINs. Use the filters to discover hidden gems! ✨</p>", unsafe_allow_html=True)
    st.markdown("---")
    conn = snowflake.connector.connect(
    user=st.secrets["snowflake"]["user"],
    password=st.secrets["snowflake"]["password"],
    account=st.secrets["snowflake"]["account"],
    warehouse=st.secrets["snowflake"]["warehouse"],
    database=st.secrets["snowflake"]["database"],
    schema=st.secrets["snowflake"]["schema"]
)

    query = "SELECT * FROM ARTIST"
    data = pd.read_sql(query, conn)
    # Sidebar Filters
    st.sidebar.header("🔎 Filter Artworks")
    art_form = st.sidebar.multiselect("🖼️ Art Form", options=data['TITLE'].unique(), default=data['TITLE'].unique())
    region = st.sidebar.multiselect("🗺️ Region", options=data['ORIGIN'].unique(), default=data['ORIGIN'].unique())
    artist = st.sidebar.multiselect("👩‍🎨 ARTIST", options=data['ARTIST'].unique(), default=data['ARTIST'].unique())
    search_query = st.text_input("🔍 Search Artworks", "")

    # Filter Data
    filtered_data = data[
        (data['TITLE'].isin(art_form)) &
        (data['ORIGIN'].isin(region)) &
        (data['ARTIST'].isin(artist)) &
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
                    img_url = row['IMAGE_URL']
                    if isinstance(img_url, str) and img_url.strip().startswith('http'):
                        st.image(img_url, caption=row['TITLE'], use_container_width=True)
                    else:
                        st.warning("No image available.")
                with cols[1]:
                    st.markdown(f"**🎨 Art Form:** {row['TITLE']}")
                    st.markdown(f"**👩‍🎨 ARTIST:** {row['ARTIST']}")
                    st.markdown(f"**🗺️ Region:** {row['ORIGIN']}")
                    st.markdown(f"**📝 DESCRIPTION:** {row['DESCRIPTION']}")
                    if st.button(f"▶️ Watch Video: {row['TITLE']}", key=f"video_{index}"):
                        vid_url = row['VIDEO_URL']
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