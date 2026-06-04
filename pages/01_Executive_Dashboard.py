import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

.main{
    background-color:#F8FAFC;
}

.kpi-card{
    background:white;
    padding:18px;
    border-radius:15px;
    box-shadow:0px 4px 12px rgba(0,0,0,0.08);
}

.big-font{
    font-size:34px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Filters")

industry = st.sidebar.multiselect(
    "Industry",
    options=sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

exit_status = st.sidebar.multiselect(
    "Exit Status",
    options=sorted(df["Exit Status"].unique()),
    default=sorted(df["Exit Status"].unique())
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region)) &
    (df["Exit Status"].isin(exit_status))
]

# =====================================================
# SUCCESS SCORE
# =====================================================

filtered_df = filtered_df.copy()

filtered_df["Success Score"] = (
    filtered_df["Revenue (M USD)"] * 0.30 +
    filtered_df["Valuation (M USD)"] * 0.20 +
    filtered_df["Market Share (%)"] * 20 +
    filtered_df["Profitable"].astype(int) * 500
)

# =====================================================
# HEADER
# =====================================================

st.title("📊 Executive Dashboard")
st.caption(
    "Executive view of startup ecosystem performance, funding trends, valuation quality and profitability."
)

# =====================================================
# KPI SECTION
# =====================================================

total_startups = len(filtered_df)

total_funding = (
    filtered_df["Funding Amount (M USD)"]
    .sum()
)

total_revenue = (
    filtered_df["Revenue (M USD)"]
    .sum()
)

avg_valuation = (
    filtered_df["Valuation (M USD)"]
    .mean()
)

profitability_rate = (
    filtered_df["Profitable"]
    .mean()
    * 100
)

total_employees = (
    filtered_df["Employees"]
    .sum()
)

k1,k2,k3,k4,k5,k6 = st.columns(6)

k1.metric(
    "Startups",
    f"{total_startups:,}"
)

k2.metric(
    "Funding",
    f"${total_funding:,.0f}M"
)

k3.metric(
    "Revenue",
    f"${total_revenue:,.0f}M"
)

k4.metric(
    "Avg Valuation",
    f"${avg_valuation:,.0f}M"
)

k5.metric(
    "Employees",
    f"{total_employees:,}"
)

k6.metric(
    "Profitability",
    f"{profitability_rate:.1f}%"
)

st.divider()

# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

left,right = st.columns([2,1])

with left:

    fig = px.scatter(
        filtered_df,
        x="Funding Amount (M USD)",
        y="Revenue (M USD)",
        size="Valuation (M USD)",
        color="Industry",
        hover_name="Startup Name",
        title="Funding vs Revenue vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    industry_summary = (
        filtered_df
        .groupby("Industry")
        .agg({
            "Funding Amount (M USD)": "sum",
            "Revenue (M USD)": "sum",
            "Valuation (M USD)": "mean"
        })
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    st.subheader("Industry Ranking")

    st.dataframe(
        industry_summary,
        use_container_width=True
    )

# =====================================================
# FUNDING DISTRIBUTION
# =====================================================

st.subheader("💰 Funding Intelligence")

c1,c2 = st.columns(2)

with c1:

    funding_by_industry = (
        filtered_df
        .groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        funding_by_industry,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="Funding by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with c2:

    fig = px.histogram(
        filtered_df,
        x="Funding Amount (M USD)",
        nbins=25,
        title="Funding Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# REVENUE & VALUATION
# =====================================================

st.subheader("📈 Revenue & Valuation")

col1,col2 = st.columns(2)

with col1:

    fig = px.treemap(
        filtered_df,
        path=["Industry"],
        values="Revenue (M USD)",
        color="Revenue (M USD)",
        title="Revenue Contribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry",
        title="Valuation Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# PROFITABILITY ANALYSIS
# =====================================================

st.subheader("🏆 Profitability Analysis")

profitability = (
    filtered_df
    .groupby("Industry")
    ["Profitable"]
    .mean()
    .reset_index()
)

profitability["Profitable"] *= 100

fig = px.bar(
    profitability,
    x="Industry",
    y="Profitable",
    color="Industry",
    title="Profitability Rate by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REGIONAL PERFORMANCE
# =====================================================

st.subheader("🌎 Regional Performance")

regional = (
    filtered_df
    .groupby("Region")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean"
    })
    .reset_index()
)

fig = px.sunburst(
    regional,
    path=["Region"],
    values="Revenue (M USD)",
    color="Funding Amount (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP STARTUPS
# =====================================================

st.subheader("🚀 Top Startups by Success Score")

top_startups = (
    filtered_df
    .sort_values(
        "Success Score",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_startups,
    x="Startup Name",
    y="Success Score",
    color="Industry",
    title="Top Performing Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# EXECUTIVE INSIGHTS
# =====================================================

st.subheader("🧠 Executive Insights")

highest_funding_industry = (
    filtered_df
    .groupby("Industry")
    ["Funding Amount (M USD)"]
    .mean()
    .idxmax()
)

highest_revenue_industry = (
    filtered_df
    .groupby("Industry")
    ["Revenue (M USD)"]
    .mean()
    .idxmax()
)

best_region = (
    filtered_df
    .groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

top_company = (
    filtered_df
    .sort_values(
        "Success Score",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

st.success(
    f"🏆 Highest funded industry: {highest_funding_industry}"
)

st.success(
    f"💰 Highest revenue industry: {highest_revenue_industry}"
)

st.success(
    f"🌍 Strongest valuation region: {best_region}"
)

st.success(
    f"🚀 Top startup overall: {top_company}"
)

# =====================================================
# TOP 20 TABLE
# =====================================================

st.subheader("📋 Executive Leaderboard")

leaderboard = (
    filtered_df[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Success Score"
        ]
    ]
    .sort_values(
        "Success Score",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    leaderboard,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================

csv = leaderboard.to_csv(index=False)

st.download_button(
    "⬇ Download Executive Report",
    csv,
    file_name="executive_dashboard_report.csv",
    mime="text/csv"
)
