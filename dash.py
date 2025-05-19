import pandas as pd
import streamlit as st
import plotly.express as px
from sqlalchemy import create_engine
def show_dashboard():
    engine = create_engine(
    f'snowflake://{st.secrets["snowflake"]["user"]}:{st.secrets["snowflake"]["password"]}@{st.secrets["snowflake"]["account"]}/{st.secrets["snowflake"]["database"]}/{st.secrets["snowflake"]["schema"]}?warehouse={st.secrets["snowflake"]["warehouse"]}'
)
    st.markdown("""
        <style>
            .main-title {text-align:center; font-size:2.5em; font-weight:bold; color:#2E86C1;}
            .section-header {font-size:1.5em; font-weight:bold; color:#117A65; margin-top:2em;}
            .stButton>button {background-color: #F39C12; color: white; border-radius: 8px;}
            .stDataFrame {background-color: #FDFEFE;}
            .sidebar .sidebar-content {background: linear-gradient(135deg, #FDEB71 0%, #F8D800 100%);}
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>🌏 GeoBoost Tourism & Culture Dashboard</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>Explore India's tourism trends, cultural richness, and vibrant art forms. Use the sidebar to navigate and filter data. ✨</p>", unsafe_allow_html=True)
    st.markdown("---")
    @st.cache_data
    def load_inbound_data():
        df = pd.read_sql("SELECT * FROM INBOUNDTOURISM", engine)
        return df
    @st.cache_data
    def load_country_data():
        df_country = pd.read_sql("SELECT * FROM COUNTRY", engine)
        return df_country
    @st.cache_data
    def load_revenue_data():
        df_revenue = pd.read_sql("SELECT * FROM REVENUE", engine)
        return df_revenue
    @st.cache_data
    def load_art_data():
        df_art = pd.read_sql("SELECT * FROM ART", engine)
        return df_art
    @st.cache_data
    def load_fest_data():
        df_fest = pd.read_sql("SELECT * FROM FESTIVAL", engine)
        return df_fest
    @st.cache_data
    def load_food_data():
        df_food = pd.read_sql("SELECT * FROM FOOD", engine)
        return df_food
    df = load_inbound_data()
    df_country = load_country_data()
    df_revenue = load_revenue_data()
    df_art = load_art_data()
    df_fest = load_fest_data()
    df_food = load_food_data()
    df.columns = df.columns.str.upper()
    df_country.columns = df_country.columns.str.upper()
    df_revenue.columns = df_revenue.columns.str.upper()
    df_art.columns = df_art.columns.str.upper()
    df_fest.columns = df_fest.columns.str.upper()
    df_food.columns = df_food.columns.str.upper()
    # Load data
    st.markdown("<div class='section-header'>📊 Data Loading...</div>", unsafe_allow_html=True)
    df = df.fillna(0)
    df_country = df_country.fillna(0)
    df_revenue = df_revenue.fillna(0)

    # Sidebar navigation
    st.sidebar.markdown("## 🧭 Navigation")
    page = st.sidebar.radio("Go to", ["🏨 Tourism", "🎭 Culture", "🖼️ Art"])

    # --- TOURISM PAGE ---
    if page == "🏨 Tourism":
        st.markdown("<div class='section-header'>📊 Tourism Dashboard</div>", unsafe_allow_html=True)
        st.markdown("""
        <ul>
            <li>📈 <b>Year-wise Trends:</b> FTAs, NRIs, International Tourist Arrivals</li>
            <li>🌍 <b>Country-wise Arrivals:</b> Interactive pie chart</li>
            <li>💰 <b>Revenue Trends:</b> Month-wise & Year-wise</li>
        </ul>
        """, unsafe_allow_html=True)

        st.sidebar.header("🎚️ Filter Options")
        year_range = st.sidebar.slider(
            "Select Year Range (Inbound Tourism)",
            min_value=int(df["YEAR"].min()),
            max_value=int(df["YEAR"].max()),
            value=(int(df["YEAR"].min()), int(df["YEAR"].max()))
        )

        filtered_df = df[(df["YEAR"] >= year_range[0]) & (df["YEAR"] <= year_range[1])]
        tourism_type = st.sidebar.multiselect(
            "Select Tourism Types to Display",
            options=["FTAs", "NRIs", "International Tourist Arrivals"],
            default=["FTAs", "NRIs", "International Tourist Arrivals"]
        )

        year_country = st.sidebar.selectbox(
            "Select Year (Country-wise Arrivals)",
            options=["2019", "2020", "2021", "2022"],
            index=0
        )

        year_column = f"NUMBEROFARRIVALS{year_country}"
        filtered_country_df = df_country[["COUNTRY", year_column]].copy()
        filtered_country_df[year_column] = pd.to_numeric(filtered_country_df[year_column], errors="coerce")
        filtered_country_df = filtered_country_df[filtered_country_df[year_column] > 0]

        countries = st.sidebar.multiselect(
            "Select Countries",
            options=filtered_country_df["COUNTRY"].unique(),
            default=filtered_country_df["COUNTRY"].unique()
        )

        filtered_country_df = filtered_country_df[filtered_country_df["COUNTRY"].isin(countries)]

        selected_year = st.sidebar.selectbox(
            "Select Year (Revenue)",
            options=["2020", "2021a","2021b" ,"2022"],
            index=0
        )

        selected_months = st.sidebar.multiselect(
            "Select Months (Revenue)",
            options=df_revenue["MONTH"].unique(),
            default=df_revenue["MONTH"].unique()
        )

        filtered_revenue_df = df_revenue[df_revenue["MONTH"].isin(selected_months)]

        # Animations: Use Streamlit's built-in spinner for smooth transitions
        with st.spinner("Loading tourism insights..."):
            col1, col2 = st.columns(2)
            if "FTAs" in tourism_type:
                fig_ftas = px.line(
                    filtered_df,
                    x="YEAR",
                    y="FTAS_IN_INDIA_MILLION",
                    title="🌐 Foreign Tourist Arrivals (FTAs) Over the Years",
                    labels={"FTAS_IN_INDIA_MILLION": "FTAs (in Millions)", "YEAR": "YEAR"},
                    markers=True,
                    color_discrete_sequence=["#1ABC9C"]
                )
                with col1:
                    st.plotly_chart(fig_ftas, use_container_width=True)

            if "NRIs" in tourism_type:
                fig_nris = px.line(
                    filtered_df,
                    x="YEAR",
                    y="NRIS_ARRIVALS_MILLION",
                    title="🧳 Non-Resident Indian Arrivals (NRIs) Over the Years",
                    labels={"NRIS_ARRIVALS_MILLION": "NRIs (in Millions)", "YEAR": "YEAR"},
                    markers=True,
                    color_discrete_sequence=["#F39C12"]
                )
                with col2:
                    st.plotly_chart(fig_nris, use_container_width=True)

            if "International Tourist Arrivals" in tourism_type:
                fig_itas = px.line(
                    filtered_df,
                    x="YEAR",
                    y="INTERNATIONAL_TOURIST_ARRIVALS_MILLION",
                    title="✈️ International Tourist Arrivals Over the Years",
                    labels={"international_tourist_arrivals_million": "ITAs (in Millions)", "YEAR": "YEAR"},
                    markers=True,
                    color_discrete_sequence=["#8E44AD"]
                )
                st.plotly_chart(fig_itas, use_container_width=True)

            fig_pie = px.pie(
                filtered_country_df,
                names="COUNTRY",
                values=year_column,
                title=f"🌍 Tourist Arrivals by Country in {year_country}",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("<div class='section-header'>💰 Tourism Revenue</div>", unsafe_allow_html=True)
            bar_chart = px.bar(
                filtered_revenue_df,
                x="MONTH",
                y="FEE_FROM_TOURISM",
                title=f"📅 Tourism Revenue by Month in {selected_year}",
                labels={"MONTH": "MONTH", "FEE_FROM_TOURISM": "Revenue (₹ crore)"},
                color="month",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(bar_chart, use_container_width=True)

            line_chart = px.line(
                filtered_revenue_df,
                x="MONTH",
                y=f"PERCENTAGE_CHANGE_{selected_year}",
                title=f"📈 Percentage Change in Revenue for {selected_year}",
                labels={"MONTH": "MONTH", f"PERCENTAGE_CHANGE_{selected_year}": "Percentage Change (%)"},
                markers=True,
                color_discrete_sequence=["#E74C3C"]
            )
            st.plotly_chart(line_chart, use_container_width=True)

            with st.expander("🔎 See Filtered Data Tables"):
                st.markdown("**Inbound Tourism Data**")
                st.dataframe(filtered_df)
                st.markdown("**Country-wise Data**")
                st.dataframe(filtered_country_df)
                st.markdown("**Revenue Data**")
                st.dataframe(filtered_revenue_df)

    # --- CULTURE PAGE ---
    elif page == "🎭 Culture":
        st.markdown("<div class='section-header'>🎨 Top 10 Art Forms in India</div>", unsafe_allow_html=True)
        st.markdown("Explore the rich cultural heritage of India through its diverse art forms. Below is a table showcasing the top 10 art forms from various states. 🌟")
        st.table(df_country)

        st.markdown("<div class='section-header'>🎉 Top 10 Festivals in India</div>", unsafe_allow_html=True)
        st.markdown("Celebrate the vibrant festivals across India. Below is a table showcasing the top 10 festivals from various states. 🪔")
        st.table(df_fest)

        st.markdown("<div class='section-header'>🍽️ Top 10 Foods in India</div>", unsafe_allow_html=True)
        st.markdown("Discover the variety of traditional Indian cuisine. Below is a table showcasing the top 10 foods from different states. 🍛")
        st.table(df_food)

    # --- ART PAGE ---
    elif page == "🖼️ Art":
        st.markdown("<div class='section-header'>🖼️ Art Page Coming Soon</div>", unsafe_allow_html=True)
        st.markdown("Detailed state-wise cultural data will be available here. Stay tuned for more updates! 🎨")