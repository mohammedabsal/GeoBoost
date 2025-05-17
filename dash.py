import pandas as pd
import streamlit as st
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

    df = pd.read_csv("data/inboundtourism.csv")
    df_country = pd.read_csv("data/country.csv")
    df_revenue = pd.read_csv("data/revenue.csv")
    df_art = pd.read_csv("data/artform.csv",quotechar='"')
    df_fest = pd.read_csv("data/festival.csv",quotechar='"')
    df_food = pd.read_csv("data/food.csv",quotechar='"')

    # Clean the datasets (handle missing values)
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
            min_value=int(df["Year"].min()),
            max_value=int(df["Year"].max()),
            value=(int(df["Year"].min()), int(df["Year"].max()))
        )

        filtered_df = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

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

        year_column = f"Number of Arrivals {year_country}"
        filtered_country_df = df_country[["Country of Nationality", year_column]].copy()
        filtered_country_df[year_column] = pd.to_numeric(filtered_country_df[year_column], errors="coerce")
        filtered_country_df = filtered_country_df[filtered_country_df[year_column] > 0]

        countries = st.sidebar.multiselect(
            "Select Countries",
            options=filtered_country_df["Country of Nationality"].unique(),
            default=filtered_country_df["Country of Nationality"].unique()
        )

        filtered_country_df = filtered_country_df[filtered_country_df["Country of Nationality"].isin(countries)]

        selected_year = st.sidebar.selectbox(
            "Select Year (Revenue)",
            options=["2020", "2021", "2022"],
            index=0
        )

        selected_months = st.sidebar.multiselect(
            "Select Months (Revenue)",
            options=df_revenue["Month"].unique(),
            default=df_revenue["Month"].unique()
        )

        filtered_revenue_df = df_revenue[df_revenue["Month"].isin(selected_months)]

        # Animations: Use Streamlit's built-in spinner for smooth transitions
        with st.spinner("Loading tourism insights..."):
            col1, col2 = st.columns(2)
            if "FTAs" in tourism_type:
                fig_ftas = px.line(
                    filtered_df,
                    x="Year",
                    y="FTAs_in_India_Million",
                    title="🌐 Foreign Tourist Arrivals (FTAs) Over the Years",
                    labels={"FTAs_in_India_Million": "FTAs (in Millions)", "Year": "Year"},
                    markers=True,
                    color_discrete_sequence=["#1ABC9C"]
                )
                with col1:
                    st.plotly_chart(fig_ftas, use_container_width=True)

            if "NRIs" in tourism_type:
                fig_nris = px.line(
                    filtered_df,
                    x="Year",
                    y="NRIs_Arrivals_Million",
                    title="🧳 Non-Resident Indian Arrivals (NRIs) Over the Years",
                    labels={"NRIs_Arrivals_Million": "NRIs (in Millions)", "Year": "Year"},
                    markers=True,
                    color_discrete_sequence=["#F39C12"]
                )
                with col2:
                    st.plotly_chart(fig_nris, use_container_width=True)

            if "International Tourist Arrivals" in tourism_type:
                fig_itas = px.line(
                    filtered_df,
                    x="Year",
                    y="International_Tourist_Arrivals_Million",
                    title="✈️ International Tourist Arrivals Over the Years",
                    labels={"International_Tourist_Arrivals_Million": "ITAs (in Millions)", "Year": "Year"},
                    markers=True,
                    color_discrete_sequence=["#8E44AD"]
                )
                st.plotly_chart(fig_itas, use_container_width=True)

            fig_pie = px.pie(
                filtered_country_df,
                names="Country of Nationality",
                values=year_column,
                title=f"🌍 Tourist Arrivals by Country in {year_country}",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("<div class='section-header'>💰 Tourism Revenue</div>", unsafe_allow_html=True)
            bar_chart = px.bar(
                filtered_revenue_df,
                x="Month",
                y="FEE from tourism (In ₹ crore)",
                title=f"📅 Tourism Revenue by Month in {selected_year}",
                labels={"Month": "Month", "FEE from tourism (In ₹ crore)": "Revenue (₹ crore)"},
                color="Month",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            st.plotly_chart(bar_chart, use_container_width=True)

            line_chart = px.line(
                filtered_revenue_df,
                x="Month",
                y=f"Percentage Change {selected_year}#2",
                title=f"📈 Percentage Change in Revenue for {selected_year}",
                labels={"Month": "Month", f"Percentage Change {selected_year}#2": "Percentage Change (%)"},
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
        st.table(df_art)

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