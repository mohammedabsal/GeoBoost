import streamlit as st
import pandas as pd
import snowflake.connector
import requests
import time
import cohere
from streamlit_lottie import st_lottie

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def show_storyteller():
    # ============ API KEYS ============
    co = cohere.Client("1bxiGdTKWg09SX91C9Cl62yzVOGqgyxWfZXBBayA")

    # ============ Load Snippets ============
    @st.cache_data
    def load_snippets():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        query = "SELECT * FROM SNIPPETS"
        return pd.read_sql(query, conn)

    # ============ Generate Story ============
    def generate_story(regions, interests):
        df = load_snippets()
        filtered = df[df['REGION'].isin(regions) & df['CATEGORY'].isin(interests)]

        if filtered.empty:
            return "No data available for the selected filters."

        context = ""
        for _, row in filtered.iterrows():
            context += f"{row['TITLE']} - {row['DESCRIPTION']}\n\n"

        region_str = ', '.join(regions)
        interest_str = ', '.join(interests)

        prompt = f"""
        You are an expert cultural travel storyteller.

        Your task is to write a rich, engaging travel story based on the following cultural context
        for each region and interest selected by the user. For each one give at most 3 lines of description:

        {context}

        The user is interested in exploring the culture of **{region_str}** with a focus on **{interest_str}**.

        📝 Structure the story with:
        - A short, immersive introduction
        - 1 section per interest (e.g., "Dance in North India" with interesting emojis)
        - Cultural insights, names of styles or forms, and local stories with emojis
        - A warm conclusion inviting the reader to explore more with emojis

        Make the story vivid, structured, and informative, written for a curious traveler. Keep the length within 200–300 words with emojis.
        """
        response = co.generate(
            model='command-r-plus',
            prompt=prompt,
            max_tokens=300,
            temperature=0.7
        )
        return response.generations[0].text.strip()

    # ============ UI Layout ============
    st.set_page_config(page_title="Cultural Storyteller", page_icon="🎭", layout="wide")
    st.markdown("""
        <style>
            .title-text {
                font-size: 2.5em; font-weight: bold; color: #7D3C98;
                text-align: center; margin-top: 20px;
            }
            .sub-text {
                font-size: 1.1em; color: #555; text-align: center;
                margin-bottom: 30px;
            }
            .story-box {
                background-color: #f9f9f9;
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                transition: all 0.3s ease;
            }
            .story-box:hover {
                transform: scale(1.01);
                box-shadow: 0px 6px 14px rgba(0, 0, 0, 0.15);
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title-text">🎭 Virtual Cultural Storyteller</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Choose your preferences and let AI narrate your dream cultural journey through India! 🌏✨</div>', unsafe_allow_html=True)

    # Load Lottie animation
    lottie_culture = load_lottie_url("https://lottie.host/732c78b1-2d80-4080-bc7f-2de6c79c8cf5/IZJwAEnTfN.json")
    st_lottie(lottie_culture, height=250, speed=1)

    # Filters
    data = load_snippets()
    col1, col2 = st.columns(2)
    with col1:
        regions = st.multiselect("🌍 Select Region(s):", sorted(data['REGION'].unique()))
    with col2:
        interests = st.multiselect("🎨 Choose Interests:", ["Dance", "Food", "Art"])

    if st.button("✨ Generate My Cultural Story"):
        if not regions or not interests:
            st.warning("⚠️ Please select at least one region and one interest.")
        else:
            with st.spinner("Crafting your story... 🎨📜"):
                time.sleep(1)
                story = generate_story(regions, interests)
                st.markdown('<div class="story-box">', unsafe_allow_html=True)
                st.markdown(f"### 🌟 Your Cultural Story\n\n{story}")
                st.markdown('</div>', unsafe_allow_html=True)
