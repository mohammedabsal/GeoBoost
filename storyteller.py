import streamlit as st
import pandas as pd
import requests
import supabase
from supabase import create_client, Client
import time
import cohere
from streamlit_lottie import st_lottie
SUPABASE_URL = "https://ilbfnsqeymeohymvllyl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlsYmZuc3FleW1lb2h5bXZsbHlsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTAzMzk0NDIsImV4cCI6MjA2NTkxNTQ0Mn0.gKRFPn_ntqTg4kHta42c7Y2fgEnN8kGuBQFz3FP2IpA"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
@st.cache_data
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
def show_storyteller():
    co = cohere.Client(st.secrets["COHERE_API_KEY"])
    @st.cache_data
    def load_snippets():
        try:
            response = supabase.table("snippets").select("*").execute()
            data = response.data
            if not data:
                return pd.DataFrame()
            return pd.DataFrame(data)
        except Exception as e:
            st.error(f"Supabase error: {e}")
            return pd.DataFrame()

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
    data = load_snippets()
    col1, col2 = st.columns(2)
    with col1:
        regions = st.multiselect("🌍 Select Region(s):", sorted(data['REGION'].unique()))
    with col2:
        interests = st.multiselect("🎨 Choose Interests:", ["Dance", "Food", "Art"])
    lottie_culture = load_lottie_url("https://lottie.host/00a25b81-7f6d-47a3-b9b8-cd982bfeac57/0Csz7nhtoI.json")
    st_lottie(lottie_culture, height=250, speed=1)
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
                st.markdown("""
        <div class="footer">
            © 2025 GeoBoost. All rights reserved.
        </div>
    """, unsafe_allow_html=True)
