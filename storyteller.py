import streamlit as st
import pandas as pd
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
        return pd.read_csv("data/snippets.csv")

    # ============ Cohere Story Generation ============
    def generate_story(regions, interests):
        df = load_snippets()
        filtered = df[df['Region'].isin(regions) & df['Category'].isin(interests)]

        if filtered.empty:
            return "No data available for the selected filters."

        context = ""
        for _, row in filtered.iterrows():
            context += f"{row['Title']} - {row['Description']}\n\n"

        region_str = ', '.join(regions)
        interest_str = ', '.join(interests)

        prompt = f"""
    You are an expert cultural travel storyteller.

    Your task is to write a rich, engaging travel story based on the following cultural context
    for each region and interest selected by the user. For each one give at most 4 lines of description:

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

    # ============ Upload Image to D-ID ============
    @st.cache_data(show_spinner=False)
    def upload_presenter_image():
        if not os.path.exists("presenter.png"):
            st.error("Missing presenter.png file.")
            return None

        with open("presenter.png", "rb") as f:
            image_data = f.read()

        response = requests.post(
            "https://api.d-id.com/images",
            headers={"Authorization": f"Bearer {DID_API_KEY}"},
            files={"image": ("presenter.png", image_data, "image/png")}

        )

        if response.status_code == 200:
            return response.json().get("id")
        else:
            st.error(f"Error uploading image: {response.text}")
            return None

    # ============ Generate D-ID Video ============
    def generate_did_video(text, presenter_image_id):
        url = "https://api.d-id.com/talks"
        headers = {
            "Authorization": f"Bearer {DID_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "script": {
                "type": "text",
                "input": text,
                "ssml": False,
                "provider": {
                    "type": "microsoft",
                    "voice_id": "en-IN-PrabhatNeural"
                }
            },
            "source_url": f"https://api.d-id.com/images/{presenter_image_id}"
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            st.error(f"Error generating video: {response.text}")
            return None

        talk_id = response.json().get("id")
        if not talk_id:
            st.error("Failed to get video ID.")
            return None

        # Poll for result
        for _ in range(20):
            time.sleep(2)
            status = requests.get(f"https://api.d-id.com/talks/{talk_id}", headers=headers)
            result = status.json()
            if result.get("result_url"):
                return result["result_url"]

        st.error("Timed out waiting for video.")
        return None
    st.title("🎭 Virtual Cultural Storyteller")
    st.markdown("Choose your preferences and let our AI generate and narrate a cultural travel story using a talking avatar.")

    data = load_snippets()
    regions = st.multiselect("Select Region(s)", options=sorted(data['Region'].unique()))
    interests = st.multiselect("Choose Interests", ["Dance", "Food", "Art"])

    if st.button("✨ Generate Animated Story"):
        if not regions or not interests:
            st.warning("Please select at least one region and one interest.")
        else:
            with st.spinner("Generating your cultural story..."):
                story = generate_story(regions, interests)
                st.subheader("📝 Your Story")
                st.markdown(f"<div style='background-color:#f4f4f4; padding:15px; border-radius:10px;'>{story}</div>", unsafe_allow_html=True)

            with st.spinner("Creating talking avatar..."):
                presenter_id = upload_presenter_image()
                if presenter_id:
                    video_url = generate_did_video(story, presenter_id)
                    if video_url:
                        st.subheader("🎬 Watch Your Avatar")
                        st.video(video_url)
