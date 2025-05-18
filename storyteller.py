import streamlit as st
import pandas as pd
import snowflake.connector
import requests
import time
import os
import cohere
def show_storyteller():
# Initialize Cohere client
    co = cohere.Client("1bxiGdTKWg09SX91C9Cl62yzVOGqgyxWfZXBBayA")
    DID_API_KEY = "bW9oYW1tZWRhYnNhbDUzOEBnbWFpbC5jb20:JmwZ7kC4KEWGCzd_kMNVY"
    # ============ Load Cultural Snippets ============
    @st.cache_data
    def load_snippets():
        conn= snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        query = "SELECT * FROM SNIPPETS"
        return pd.read_sql(query, conn)

    # ============ Cohere Story Generation ============
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