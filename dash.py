import pandas as pd
import streamlit as st
import snowflake.connector
import plotly.express as px

def show_dashboard():
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

    # --- Data Loaders ---
    @st.cache_data
    def load_inbound_data():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        df = pd.read_sql("SELECT * FROM INBOUNDTOURISM", conn)
        conn.close()
        return df

    @st.cache_data
    def load_country_data():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        df_country = pd.read_sql("SELECT * FROM COUNTRY", conn)
        conn.close()
        return df_country

    @st.cache_data
    def load_revenue_data():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        df_revenue = pd.read_sql("SELECT * FROM REVENUE", conn)
        conn.close()
        return df_revenue

    @st.cache_data
    def load_art_data():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        df_art = pd.read_sql("SELECT * FROM ARTIST", conn)
        conn.close()
        return df_art

    @st.cache_data
    def load_fest_data():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        df_fest = pd.read_sql("SELECT * FROM FESTIVAL", conn)
        conn.close()
        return df_fest

    @st.cache_data
    def load_food_data():
        conn = snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
        df_food = pd.read_sql("SELECT * FROM FOOD", conn)
        conn.close()
        return df_food

    # Load data
    df = load_inbound_data()
    df_country = load_country_data()
    df_revenue = load_revenue_data()
    df_art = load_art_data()
    df_fest = load_fest_data()
    df_food = load_food_data()

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
            options=["2020", "2021a", "2021b", "2022"],
            index=0
        )

        selected_months = st.sidebar.multiselect(
            "Select Months (Revenue)",
            options=df_revenue["MONTH"].unique(),
            default=df_revenue["MONTH"].unique()
        )

        filtered_revenue_df = df_revenue[df_revenue["MONTH"].isin(selected_months)]

        # Minimal Plotly Charts
        with st.spinner("Loading tourism insights..."):
            col1, col2 = st.columns(2)
            if "FTAs" in tourism_type:
                fig_ftas = px.line(
                    filtered_df,
                    x="YEAR",
                    y="FTAS_IN_INDIA_MILLION",
                    labels={"FTAS_IN_INDIA_MILLION": "FTAs (in Millions)", "YEAR": "YEAR"},
                    markers=True,
                    color_discrete_sequence=["#1ABC9C"]
                )
                fig_ftas.update_layout(title=None, showlegend=False)
                with col1:
                    st.plotly_chart(fig_ftas, use_container_width=True)

            if "NRIs" in tourism_type:
                fig_nris = px.hist(
                    filtered_df,
                    x="YEAR",
                    y="NRIS_ARRIVALS_MILLION",
                    labels={"NRIS_ARRIVALS_MILLION": "NRIs (in Millions)", "YEAR": "YEAR"},
                    markers=True,
                    color_discrete_sequence=["#F39C12"]
                )
                fig_nris.update_layout(title=None, showlegend=False)
                with col2:
                    st.plotly_chart(fig_nris, use_container_width=True)

            if "International Tourist Arrivals" in tourism_type:
                fig_itas = px.line(
                    filtered_df,
                    x="YEAR",
                    y="INTERNATIONAL_TOURIST_ARRIVALS_MILLION",
                    labels={"INTERNATIONAL_TOURIST_ARRIVALS_MILLION": "ITAs (in Millions)", "YEAR": "YEAR"},
                    markers=True,
                    color_discrete_sequence=["#8E44AD"]
                )
                fig_itas.update_layout(title=None, showlegend=False)
                st.plotly_chart(fig_itas, use_container_width=True)

            fig_pie = px.pie(
                filtered_country_df,
                names="COUNTRY",
                values=year_column,
                title=None,
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("<div class='section-header'>💰 Tourism Revenue</div>", unsafe_allow_html=True)
            bar_chart = px.bar(
                filtered_revenue_df,
                x="MONTH",
                y="FEE_FROM_TOURISM",
                labels={"MONTH": "MONTH", "FEE_FROM_TOURISM": "Revenue (₹ crore)"},
                color="MONTH",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            bar_chart.update_layout(title=None, showlegend=False)
            st.plotly_chart(bar_chart, use_container_width=True)

            line_chart = px.line(
                filtered_revenue_df,
                x="MONTH",
                y=f"PERCENTAGE_CHANGE_{selected_year}",
                labels={"MONTH": "MONTH", f"PERCENTAGE_CHANGE_{selected_year}": "Percentage Change (%)"},
                markers=True,
                color_discrete_sequence=["#E74C3C"]
            )
            line_chart.update_layout(title=None, showlegend=False)
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
        st.table(df_country.head(10))

        st.markdown("<div class='section-header'>🎉 Top 10 Festivals in India</div>", unsafe_allow_html=True)
        st.markdown("Celebrate the vibrant festivals across India. Below is a table showcasing the top 10 festivals from various states. 🪔")
        st.table(df_fest.head(10))

        st.markdown("<div class='section-header'>🍽️ Top 10 Foods in India</div>", unsafe_allow_html=True)
        st.markdown("Discover the variety of traditional Indian cuisine. Below is a table showcasing the top 10 foods from different states. 🍛")
        st.table(df_food.head(10))

    # --- ART PAGE ---
    elif page == "🖼️ Art":
        st.markdown("<div class='section-header'>🖼️ Art Page Coming Soon</div>", unsafe_allow_html=True)
        st.markdown("Detailed state-wise cultural data will be available here. Stay tuned for more updates! 🎨")