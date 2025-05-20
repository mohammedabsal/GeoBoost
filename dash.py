import streamlit as st
import pandas as pd
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

    # Connect to Snowflake
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
    inbound_df = inbound_df.apply(pd.to_numeric, errors='ignore')
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

    # --- Line Chart: Trends Over Years ---
    st.header("📈 YEAR-wise Tourism Trends")
    if selected_metrics:
        fig = px.line(
            filtered_df,
            x="YEAR",
            y=[metrics[m] for m in selected_metrics],
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Bold,
            labels={"value": "Number of Tourists (Million)", "variable": "Metric", "YEAR": "YEAR"},
            template="plotly"
        )
        fig.update_layout(legend_title_text="Metric")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please select at least one metric to display.")

    # --- Bar Chart: Single Year Comparison ---
    st.header(f"📊 Metric Comparison for {single_year}")
    if selected_metrics:
        bar_data = {
            "Metric": [m for m in selected_metrics],
            "Value": [float(single_year_df[metrics[m]]) for m in selected_metrics]
        }
        bar_df = pd.DataFrame(bar_data)
        fig_bar = px.bar(
            bar_df,
            x="Metric",
            y="Value",
            color="Metric",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            labels={"Value": "Number of Tourists (Million)", "Metric": "Metric"},
            template="plotly"
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    # --- Percentage Change Visualization ---
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
        # Melt the DataFrame to long format for Plotly
        melted = filtered_df.melt(
            id_vars=["YEAR"],
            value_vars=[change_metrics[m] for m in selected_change],
            var_name="Metric",
            value_name="Percentage Change"
        )
        # Map back to friendly names
        metric_name_map = {v: k for k, v in change_metrics.items()}
        melted["Metric"] = melted["Metric"].map(metric_name_map)

        fig2 = px.line(
            melted,
            x="YEAR",
            y="Percentage Change",
            color="Metric",
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Pastel,
            labels={"Percentage Change": "Percentage Change (%)", "YEAR": "Year", "Metric": "Metric"},
            template="plotly"
        )
        fig2.update_layout(legend_title_text="Metric")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Please select at least one percentage change metric.")

    # Sidebar filters
    st.sidebar.header("🔎 Filter Options")
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
    filtered_df = df[df["MONTH"].isin(months)]


    st.title("💰 India Tourism Revenue Dashboard")
    st.markdown("""
    Explore monthly tourism revenue and trends.  
    Use the filters to customize your view.  
    """)

    # Layout: Two columns for bar and pie chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Monthly Revenue")
        fig1 = px.bar(
            filtered_df,
            x="MONTH",
            y="FEE_FROM_TOURISM",
            color="MONTH",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            labels={"FEE_FROM_TOURISM": "Tourism Revenue (₹ crore)", "MONTH": "MONTH"},
            template="plotly_white"
        )
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Revenue Share by Month")
        fig2 = px.pie(
            filtered_df,
            names="MONTH",
            values="FEE_FROM_TOURISM",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4,
            template="plotly_white"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Percentage Change Chart
    st.subheader(f"Monthly {selected_pct.replace('_', ' ').title()}")
    fig3 = px.line(
        filtered_df,
        x="MONTH",
        y=selected_pct,
        markers=True,
        color_discrete_sequence=["#E45756"],
        labels={selected_pct: "Percentage Change (%)", "MONTH": "MONTH"},
        template="plotly_white"
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Data Table and Download
    with st.expander("📋 Show Data Table"):
        st.dataframe(filtered_df)
        st.download_button(
            "Download Filtered Data",
            filtered_df.to_csv(index=False),
            "revenue_filtered.csv"
        )

    # --- Country-wise Tourist Arrivals ---
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

    # Sort and plot with Plotly
    tourists_sorted = country_df.sort_values(by=arrivals_col, ascending=False)
    fig3 = px.bar(
        tourists_sorted,
        x=arrivals_col,
        y='COUNTRY',
        orientation='h',
        color=arrivals_col,
        color_continuous_scale='viridis',
        labels={arrivals_col: "Tourists", "COUNTRY": "Country"},
        title=f"Number of Tourists by Country ({year})"
    )
    fig3.update_layout(yaxis={'categoryorder':'total ascending'}, title=None)
    st.plotly_chart(fig3, use_container_width=True)
