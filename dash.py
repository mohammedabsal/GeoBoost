import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import altair as alt
import warnings

# Suppress SQLAlchemy warning
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy")

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

    # Connect to Snowflake
    @st.cache_data
    def get_snowflake_connection():
        return snowflake.connector.connect(
            user=st.secrets["snowflake"]["user"],
            password=st.secrets["snowflake"]["password"],
            account=st.secrets["snowflake"]["account"],
            warehouse=st.secrets["snowflake"]["warehouse"],
            database=st.secrets["snowflake"]["database"],
            schema=st.secrets["snowflake"]["schema"]
        )
    conn = get_snowflake_connection()
    def load_revenue_data():
        df_revenue = pd.read_sql("SELECT * FROM REVENUE", conn)
        return df_revenue
    def load_country_data():
        df_country = pd.read_sql("SELECT * FROM COUNTRY", conn)
        return df_country
    def load_inbound_data():
        df_inbound = pd.read_sql("SELECT * FROM INBOUNDTOURISM", conn)
        return df_inbound
    # Load data from Snowflake
    df = load_revenue_data()
    country_df = load_country_data()
    inbound_df = load_inbound_data()
    inbound_df.columns = [c.strip() for c in inbound_df.columns]
    # Fix FutureWarning for pd.to_numeric
    for col in inbound_df.columns:
        try:
            inbound_df[col] = pd.to_numeric(inbound_df[col])
        except Exception:
            continue

    # Sidebar filters
    st.sidebar.header("🔎 Filter Options")
    metrics = {
        "Foreign Tourist Arrivals (FTAs)": "FTAS_IN_INDIA_MILLION",
        "NRIs Arrivals": "NRIS_ARRIVALS_MILLION",
        "International Tourist Arrivals": "INTERNATIONAL_TOURIST_ARRIVALS_MILLION"
    }
    selected_metrics = st.sidebar.multiselect(
        "Select metrics to display",
        list(metrics.keys()),
        default=list(metrics.keys())
    )
    year_range = st.sidebar.slider(
        "Select Year Range",
        int(inbound_df["YEAR"].min()),
        int(inbound_df["YEAR"].max()),
        (int(inbound_df["YEAR"].min()), int(inbound_df["YEAR"].max()))
    )
    single_year = st.sidebar.selectbox(
        "Select Year for Comparison",
        sorted(inbound_df["YEAR"].unique()),
        index=len(inbound_df["YEAR"].unique())-1
    )

    # Filter data by year range
    filtered_df = inbound_df[(inbound_df["YEAR"] >= year_range[0]) & (inbound_df["YEAR"] <= year_range[1])]
    single_year_df = inbound_df[inbound_df["YEAR"] == single_year]

    st.title("🇮🇳 India Inbound Tourism Dashboard")
    st.markdown("""
    Welcome to the interactive dashboard for India's inbound tourism!  
    Use the sidebar to filter by year and metrics.  
    Explore trends, compare years, and see percentage changes with colorful, interactive charts.
    """)

    with st.expander("📋 Show Raw Data"):
        st.dataframe(filtered_df)

    # --- Line Chart: Trends Over Years (Altair) ---
    st.header("📈 YEAR-wise Tourism Trends")
    if selected_metrics:
        melted = filtered_df.melt(
            id_vars=["YEAR"],
            value_vars=[metrics[m] for m in selected_metrics],
            var_name="Metric",
            value_name="Value"
        )
        chart = alt.Chart(melted).mark_line(point=True).encode(
            x=alt.X("YEAR:O", title="Year"),
            y=alt.Y("Value:Q", title="Number of Tourists (Million)"),
            color=alt.Color("Metric:N", title="Metric"),
            tooltip=["YEAR", "Metric", "Value"]
        ).properties(
            width="container",
            height=400
        ).configure_legend(
            orient="top"
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Please select at least one metric to display.")

    # --- Bar Chart: Single Year Comparison (Altair) ---
    st.header(f"📊 Metric Comparison for {single_year}")
    if selected_metrics:
        bar_data = {
            "Metric": [m for m in selected_metrics],
            "Value": [float(single_year_df[metrics[m]].iloc[0]) for m in selected_metrics]
        }
        bar_df = pd.DataFrame(bar_data)
        bar_chart = alt.Chart(bar_df).mark_bar(size=40).encode(
            x=alt.X("Metric:N", title="Metric"),
            y=alt.Y("Value:Q", title="Number of Tourists (Million)"),
            color=alt.Color("Metric:N", scale=alt.Scale(scheme="category20b")),
            tooltip=["Metric", "Value"]
        ).properties(
            width="container",
            height=400
        )
        st.altair_chart(bar_chart, use_container_width=True)

    # --- Percentage Change Visualization (Altair) ---
    st.header("🔄 Year-wise Percentage Change")
    change_metrics = {
        "FTAs % Change": "PERCENTAGE_CHANGE_FTAS",
        "NRIs % Change": "PERCENTAGE_CHANGE_NRIS",
        "ITAs % Change": "PERCENTAGE_CHANGE_ITAS"
    }
    selected_change = st.multiselect(
        "Select percentage change metrics",
        list(change_metrics.keys()),
        default=list(change_metrics.keys())
    )
    if selected_change:
        melted = filtered_df.melt(
            id_vars=["YEAR"],
            value_vars=[change_metrics[m] for m in selected_change],
            var_name="Metric",
            value_name="Percentage Change"
        )
        metric_name_map = {v: k for k, v in change_metrics.items()}
        melted["Metric"] = melted["Metric"].map(metric_name_map)
        pct_chart = alt.Chart(melted).mark_line(point=True).encode(
            x=alt.X("YEAR:O", title="Year"),
            y=alt.Y("Percentage Change:Q", title="Percentage Change (%)"),
            color=alt.Color("Metric:N", title="Metric", scale=alt.Scale(scheme="pastel1")),
            tooltip=["YEAR", "Metric", "Percentage Change"]
        ).properties(
            width="container",
            height=400
        )
        st.altair_chart(pct_chart, use_container_width=True)
    else:
        st.info("Please select at least one percentage change metric.")

    # --- Revenue Section ---
    st.sidebar.header("🔎 Revenue Filter Options")
    months = st.sidebar.multiselect(
        "Select Months",
        df["MONTH"].unique(),
        default=list(df["MONTH"].unique())
    )
    pct_options = [
        "PERCENTAGE_CHANGE_2020",
        "PERCENTAGE_CHANGE_2021",
        "PERCENTAGE_CHANGE_20_21",
        "PERCENTAGE_CHANGE_22_21"
    ]
    selected_pct = st.sidebar.selectbox(
        "Select Percentage Change Column",
        pct_options,
        format_func=lambda x: x.replace("_", " ").title()
    )

    # Filtered data
    filtered_rev_df = df[df["MONTH"].isin(months)]

    st.title("💰 India Tourism Revenue Dashboard")
    st.markdown("""
    Explore monthly tourism revenue and trends.  
    Use the filters to customize your view.  
    """)

    # Layout: Two columns for bar and pie chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Revenue")
        bar_chart_rev = alt.Chart(filtered_rev_df).mark_bar(size=40).encode(
            x=alt.X("MONTH:N", title="Month", sort=list(df["MONTH"].unique())),
            y=alt.Y("FEE_FROM_TOURISM:Q", title="Tourism Revenue (₹ crore)"),
            color=alt.Color("MONTH:N", scale=alt.Scale(scheme="category20b")),
            tooltip=["MONTH", "FEE_FROM_TOURISM"]
        ).properties(
            width="container",
            height=400
        )
        st.altair_chart(bar_chart_rev, use_container_width=True)

    with col2:
        st.subheader("Revenue Share by Month")
        fig2 = px.pie(
            filtered_rev_df,
            names="MONTH",
            values="FEE_FROM_TOURISM",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Percentage Change Chart (Altair)
    st.subheader(f"Monthly {selected_pct.replace('_', ' ').title()}")
    pct_chart_rev = alt.Chart(filtered_rev_df).mark_line(point=True).encode(
        x=alt.X("MONTH:N", title="Month", sort=list(df["MONTH"].unique())),
        y=alt.Y(f"{selected_pct}:Q", title="Percentage Change (%)"),
        color=alt.value("#E45756"),
        tooltip=["MONTH", selected_pct]
    ).properties(
        width="container",
        height=400
    )
    st.altair_chart(pct_chart_rev, use_container_width=True)

    # Data Table and Download
    with st.expander("📋 Show Data Table"):
        st.dataframe(filtered_rev_df)
        st.download_button(
            "Download Filtered Data",
            filtered_rev_df.to_csv(index=False),
            "revenue_filtered.csv"
        )

    # --- Country-wise Tourist Arrivals (Altair Bar) ---
    st.header("🌍 Country-wise Tourist Visits to India")
    with st.expander("Show Country-wise Tourist Data"):
        st.dataframe(country_df)

    # Choose year to display
    year = st.selectbox(
        "Select Year for Tourist Arrivals",
        ["2019", "2020", "2021", "2022"],
        index=0
    )
    arrivals_col = f"NUMBEROFARRIVALS{year}"

    tourists_sorted = country_df.sort_values(by=arrivals_col, ascending=False)
    bar_chart_country = alt.Chart(tourists_sorted).mark_bar(size=20).encode(
        x=alt.X(f"{arrivals_col}:Q", title="Tourists"),
        y=alt.Y("COUNTRY:N", sort='-x', title="Country"),
        color=alt.Color(f"{arrivals_col}:Q", scale=alt.Scale(scheme="viridis")),
        tooltip=["COUNTRY", arrivals_col]
    ).properties(
        width="container",
        height=600,
        title=f"Number of Tourists by Country ({year})"
    )
    st.altair_chart(bar_chart_country, use_container_width=True)