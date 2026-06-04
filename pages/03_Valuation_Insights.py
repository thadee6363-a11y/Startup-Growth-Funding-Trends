import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Valuation Insights",
    page_icon="📈",
    layout="wide"
)

# ==========================================================
# STYLING
# ==========================================================

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# ==========================================================
# FILTERS
# ==========================================================

st.sidebar.header("Valuation Filters")

industry = st.sidebar.multiselect(
    "Industry",
    sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

exit_status = st.sidebar.multiselect(
    "Exit Status",
    sorted(df["Exit Status"].unique()),
    default=sorted(df["Exit Status"].unique())
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region)) &
    (df["Exit Status"].isin(exit_status))
].copy()

# ==========================================================
# VALUATION ENGINE
# ==========================================================

filtered_df["Valuation Multiple"] = (
    filtered_df["Valuation (M USD)"]
    /
    filtered_df["Revenue (M USD)"]
)

filtered_df["Funding Efficiency"] = (
    filtered_df["Valuation (M USD)"]
    /
    filtered_df["Funding Amount (M USD)"]
)

# ==========================================================
# HEADER
# ==========================================================

st.title("📈 Valuation Intelligence")
st.caption(
    "Deep valuation analytics, benchmarking and investor intelligence"
)

# ==========================================================
# KPI SECTION
# ==========================================================

total_valuation = (
    filtered_df["Valuation (M USD)"]
    .sum()
)

avg_valuation = (
    filtered_df["Valuation (M USD)"]
    .mean()
)

median_valuation = (
    filtered_df["Valuation (M USD)"]
    .median()
)

highest_valuation = (
    filtered_df["Valuation (M USD)"]
    .max()
)

avg_multiple = (
    filtered_df["Valuation Multiple"]
    .mean()
)

unicorns = (
    filtered_df[
        filtered_df["Valuation (M USD)"] >= 1000
    ]
    .shape[0]
)

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Total Valuation",
    f"${total_valuation:,.0f}M"
)

c2.metric(
    "Average Valuation",
    f"${avg_valuation:,.0f}M"
)

c3.metric(
    "Median Valuation",
    f"${median_valuation:,.0f}M"
)

c4.metric(
    "Highest Valuation",
    f"${highest_valuation:,.0f}M"
)

c5.metric(
    "Avg Multiple",
    f"{avg_multiple:.2f}x"
)

c6.metric(
    "Unicorns",
    unicorns
)

st.divider()

# ==========================================================
# VALUATION DISTRIBUTION
# ==========================================================

st.subheader("Valuation Distribution")

left,right = st.columns(2)

with left:

    fig = px.histogram(
        filtered_df,
        x="Valuation (M USD)",
        nbins=30,
        title="Valuation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.box(
        filtered_df,
        y="Valuation (M USD)",
        color="Industry",
        title="Valuation Spread"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# INDUSTRY BENCHMARKS
# ==========================================================

st.subheader("Industry Valuation Benchmark")

industry_benchmark = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Valuation (M USD)": "mean",
        "Revenue (M USD)": "mean",
        "Valuation Multiple": "mean"
    })
    .reset_index()
)

fig = px.bar(
    industry_benchmark,
    x="Industry",
    y="Valuation (M USD)",
    color="Industry",
    title="Average Valuation by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# VALUATION MULTIPLE ANALYSIS
# ==========================================================

st.subheader("Valuation Multiple Analysis")

fig = px.box(
    filtered_df,
    x="Industry",
    y="Valuation Multiple",
    color="Industry",
    title="Valuation Multiple Benchmark"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# FUNDING VS VALUATION
# ==========================================================

st.subheader("Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    size="Revenue (M USD)",
    color="Industry",
    hover_name="Startup Name",
    title="Funding Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REVENUE VS VALUATION
# ==========================================================

st.subheader("Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    size="Funding Amount (M USD)",
    color="Industry",
    hover_name="Startup Name",
    trendline="ols",
    title="Revenue Impact on Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# TOP VALUED STARTUPS
# ==========================================================

st.subheader("Top Valued Startups")

top_valued = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    top_valued,
    x="Startup Name",
    y="Valuation (M USD)",
    color="Industry",
    title="Highest Valued Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# OVERVALUED STARTUPS
# ==========================================================

st.subheader("Potentially Overvalued Startups")

overvalued = (
    filtered_df
    .sort_values(
        "Valuation Multiple",
        ascending=False
    )
    .head(15)
)

st.dataframe(
    overvalued[
        [
            "Startup Name",
            "Industry",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Valuation Multiple"
        ]
    ],
    use_container_width=True
)

# ==========================================================
# UNDERVALUED STARTUPS
# ==========================================================

st.subheader("Potentially Undervalued Startups")

undervalued = (
    filtered_df
    .sort_values(
        "Valuation Multiple",
        ascending=True
    )
    .head(15)
)

st.dataframe(
    undervalued[
        [
            "Startup Name",
            "Industry",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Valuation Multiple"
        ]
    ],
    use_container_width=True
)

# ==========================================================
# REGIONAL VALUATION ANALYSIS
# ==========================================================

st.subheader("Regional Valuation Intelligence")

regional = (
    filtered_df
    .groupby("Region")
    .agg({
        "Valuation (M USD)": "mean",
        "Revenue (M USD)": "sum"
    })
    .reset_index()
)

fig = px.treemap(
    regional,
    path=["Region"],
    values="Revenue (M USD)",
    color="Valuation (M USD)",
    title="Regional Valuation Landscape"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# UNICORN ANALYSIS
# ==========================================================

st.subheader("🦄 Unicorn Analysis")

unicorn_df = filtered_df[
    filtered_df["Valuation (M USD)"] >= 1000
]

if len(unicorn_df) > 0:

    fig = px.pie(
        unicorn_df,
        names="Industry",
        values="Valuation (M USD)",
        title="Unicorn Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "No unicorn startups found in current filters."
    )

# ==========================================================
# VALUATION EFFICIENCY
# ==========================================================

st.subheader("Valuation Efficiency")

efficiency = (
    filtered_df
    .groupby("Industry")
    ["Funding Efficiency"]
    .mean()
    .reset_index()
)

fig = px.bar(
    efficiency,
    x="Industry",
    y="Funding Efficiency",
    color="Industry",
    title="Valuation Generated Per Funding Dollar"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# INVESTOR INSIGHTS
# ==========================================================

st.subheader("🧠 Investor Insights")

best_industry = (
    industry_benchmark
    .sort_values(
        "Valuation Multiple",
        ascending=False
    )
    .iloc[0]["Industry"]
)

best_region = (
    regional
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

highest_company = (
    filtered_df
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"🏆 Highest valuation multiple industry: {best_industry}"
)

st.success(
    f"🌍 Strongest valuation region: {best_region}"
)

st.success(
    f"🚀 Most valuable startup: {highest_company}"
)

st.success(
    f"🦄 Total unicorn startups detected: {unicorns}"
)

# ==========================================================
# LEADERBOARD
# ==========================================================

st.subheader("Valuation Leaderboard")

leaderboard = (
    filtered_df[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Funding Amount (M USD)",
            "Valuation Multiple"
        ]
    ]
    .sort_values(
        "Valuation (M USD)",
        ascending=False
    )
)

st.dataframe(
    leaderboard,
    use_container_width=True
)

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

csv = leaderboard.to_csv(index=False)

st.download_button(
    "⬇ Download Valuation Report",
    csv,
    file_name="valuation_insights_report.csv",
    mime="text/csv"
)
