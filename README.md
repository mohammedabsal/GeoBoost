# 🌏 GeoBoost Cultural Explorer

**GeoBoost Cultural Explorer** is an interactive Streamlit web app that enables users to explore India's diverse cultural landscape, including tourism, traditional arts, cuisine, festivals, and responsible travel practices.

It features interactive dashboards, dynamic maps, an art gallery, AI-powered cultural storytelling, and travel tips—all in one immersive experience!

---

## 🚀 Features

- 🏠 **Home**: Attractive landing page with highlights of key features.
- 📊 **Tourism Dashboard**: Visualize tourism trends such as arrivals and foreign exchange revenue using interactive Plotly charts.
- 🗺️ **Cultural Map**: Explore Indian states’ cultural heritage—festivals, foods, and art forms—on a Folium-powered map.
- 🖼️ **Art Gallery**: Browse curated Indian art, artists, and regional styles.
- 🎨 **Art Forms**: Discover traditional and modern art forms, their origin states, and prominent artists.
- 🌱 **Responsible Tourism Tips**: Get eco-friendly travel tips and etiquette guidelines for each state/city.
- 📖 **AI Storyteller**: Generate personalized cultural stories with AI and avatar integration (Cohere + Lottie + TTS).

---

## 🗂️ Project Structure

```

YourStory/
│
├── main.py                 # Streamlit entrypoint
├── map.py                  # Handles interactive cultural map
├── dash.py                 # Tourism dashboard
├── gallery.py              # Art gallery and image display
├── artforms.py             # Art forms filter and descriptions
├── visit.py                # Responsible tourism tips
├── storyteller.py          # AI-based cultural storyteller
│
├── data/
│   ├── artform.csv
│   ├── artist.csv
│   ├── country.csv
│   ├── festival.csv
│   ├── food.csv
│   ├── foods\_unique.csv
│   ├── inboundtourism.csv
│   ├── Indian\_Festivals\_By\_State\_With\_Coordinates.csv
│   ├── k\_dance.csv
│   ├── revenue.csv
│   ├── snippets.csv
│   └── timetovisit.csv
│
└── README.md

````

---

## 🛠️ Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/yourusername/GeoBoost-Cultural-Explorer.git
cd GeoBoost-Cultural-Explorer
````

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the app

```bash
streamlit run main.py
```

---

## ⚙️ Requirements

* Python 3.8+
* streamlit
* pandas
* plotly
* folium
* streamlit-folium
* streamlit-lottie
* requests

> Optional: `cohere`, `gtts`, etc. for AI storytelling features.

---

## 📊 Data Sources

All datasets are in the `data/` directory and include:

* Tourism statistics (`inboundtourism.csv`, `revenue.csv`)
* Art forms, regions, and artists (`artform.csv`, `artist.csv`)
* Indian food and festivals by state (`food.csv`, `festival.csv`)
* Cultural storytelling snippets (`snippets.csv`)
* Travel tips and seasons to visit (`timetovisit.csv`)

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you'd like to change or add.

---

## 📄 License

This project is licensed under the **MIT License**.
Feel free to use and modify it under the terms of the license.

---

## 🙏 Acknowledgements

* [Streamlit](https://streamlit.io/)
* [LottieFiles](https://lottiefiles.com/)
* [Cohere AI](https://cohere.ai/)
* [Hugging Face](https://huggingface.co/)
* All open data sources used
* Made with ❤️ by **Team GeoBoost**

```

