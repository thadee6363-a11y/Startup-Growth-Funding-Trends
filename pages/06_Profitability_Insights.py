import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Profitability Insights",
    page_icon="💵",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# =====================================================
# HEADER
# =====================================================

st.title("💵 Profitability Intelligence")
st.caption(
    "Analyze sustainable growth, profitability drivers and capital efficiency"
)

# =====================================================
# SIDEBAR FILTERS
# =====================================================

st.sidebar.header("Profitability Filters")

industry_filter = st.sidebar.multiselect(
    "Industry",
    sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

region_filter = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

exit_filter = st.sidebar.multiselect(
    "Exit Status",
    sorted(df["Exit Status"].unique()),
    default=sorted(df["Exit Status"].unique())
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter)) &
    (df["Exit Status"].isin(exit_filter))
].copy()

# =====================================================
# PROFITABILITY ENGINE
# =====================================================

filtered_df["Profitability Score"] = (
    filtered_df["Revenue (M USD)"] * 0.35
    +
    filtered_df["Market Share (%)"] * 20
    +
    filtered_df["Valuation (M USD)"] * 0.15
    +
    filtered_df["Profitable"].astype(int) * 500
)

filtered_df["Revenue Efficiency"] = (
    filtered_df["Revenue (M USD)"]
    /
    filtered_df["Funding Amount (M USD)"]
)

filtered_df["Valuation Efficiency"] = (
    filtered_df["Valuation (M USD)"]
    /
    filtered_df["Funding Amount (M USD)"]
)

# =====================================================
# KPI SECTION
# =====================================================

total_startups = len(filtered_df)

profitable_count = (
    filtered_df["Profitable"]
    .sum()
)

profitability_rate = (
    filtered_df["Profitable"]
    .mean()
    * 100
)

avg_revenue = (
    filtered_df["Revenue (M USD)"]
    .mean()
)

avg_efficiency = (
    filtered_df["Revenue Efficiency"]
    .mean()
)

top_score = (
    filtered_df["Profitability Score"]
    .max()
)

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Startups",
    total_startups
)

c2.metric(
    "Profitable",
    int(profitable_count)
)

c3.metric(
    "Profitability %",
    f"{profitability_rate:.1f}%"
)

c4.metric(
    "Avg Revenue",
    f"${avg_revenue:,.1f}M"
)

c5.metric(
    "Revenue Efficiency",
    f"{avg_efficiency:.2f}"
)

c6.metric(
    "Top Profit Score",
    f"{top_score:,.0f}"
)

st.divider()

# =====================================================
# PROFITABLE VS NON-PROFITABLE
# =====================================================

st.subheader("🏆 Profitability Distribution")

profit_dist = (
    filtered_df["Profitable"]
    .value_counts()
    .reset_index()
)

profit_dist.columns = [
    "Status",
    "Count"
]

profit_dist["Status"] = (
    profit_dist["Status"]
    .map({
        True: "Profitable",
        False: "Non-Profitable"
    })
)

fig = px.pie(
    profit_dist,
    names="Status",
    values="Count",
    title="Profitability Breakdown"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INDUSTRY PROFITABILITY
# =====================================================

st.subheader("🏭 Industry Profitability")

industry_profit = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Profitable": "mean",
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean"
    })
    .reset_index()
)

industry_profit["Profitable"] *= 100

fig = px.bar(
    industry_profit,
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
# REGIONAL PROFITABILITY
# =====================================================

st.subheader("🌎 Regional Profitability")

regional_profit = (
    filtered_df
    .groupby("Region")
    .agg({
        "Profitable": "mean"
    })
    .reset_index()
)

regional_profit["Profitable"] *= 100

fig = px.bar(
    regional_profit,
    x="Region",
    y="Profitable",
    color="Region",
    title="Profitability Rate by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# REVENUE VS PROFITABILITY
# =====================================================

st.subheader("📈 Revenue Impact")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    size="Funding Amount (M USD)",
    color="Profitable",
    hover_name="Startup Name",
    title="Revenue, Valuation & Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# FUNDING VS PROFITABILITY
# =====================================================

st.subheader("💰 Funding Impact")

fig = px.box(
    filtered_df,
    x="Profitable",
    y="Funding Amount (M USD)",
    color="Profitable",
    title="Funding Distribution by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# VALUATION VS PROFITABILITY
# =====================================================

st.subheader("📊 Valuation Impact")

valuation_compare = (
    filtered_df
    .groupby("Profitable")
    ["Valuation (M USD)"]
    .mean()
    .reset_index()
)

valuation_compare["Profitable"] = (
    valuation_compare["Profitable"]
    .astype(str)
)

fig = px.bar(
    valuation_compare,
    x="Profitable",
    y="Valuation (M USD)",
    color="Profitable",
    title="Average Valuation by Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# CAPITAL EFFICIENCY
# =====================================================

st.subheader("⚡ Capital Efficiency")

efficiency = (
    filtered_df
    .groupby("Industry")
    ["Revenue Efficiency"]
    .mean()
    .reset_index()
    .sort_values(
        "Revenue Efficiency",
        ascending=False
    )
)

fig = px.bar(
    efficiency,
    x="Industry",
    y="Revenue Efficiency",
    color="Industry",
    title="Revenue Generated Per Funding Dollar"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP PROFITABLE STARTUPS
# =====================================================

st.subheader("🚀 Profitability Leaderboard")

leaders = (
    filtered_df
    .sort_values(
        "Profitability Score",
        ascending=False
    )
    .head(20)
)

fig = px.bar(
    leaders,
    x="Startup Name",
    y="Profitability Score",
    color="Industry",
    title="Top Profitability Scores"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# EXIT STATUS ANALYSIS
# =====================================================

st.subheader("🎯 Exit Outcomes")

exit_profit = (
    filtered_df
    .groupby("Exit Status")
    .agg({
        "Profitable": "mean"
    })
    .reset_index()
)

exit_profit["Profitable"] *= 100

fig = px.bar(
    exit_profit,
    x="Exit Status",
    y="Profitable",
    color="Exit Status",
    title="Profitability by Exit Status"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# HEATMAP
# =====================================================

st.subheader("🔥 Correlation Analysis")

numeric_df = filtered_df.select_dtypes(
    include=np.number
)

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Profitability Drivers Correlation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# INDUSTRY SCORECARD
# =====================================================

st.subheader("📋 Industry Profitability Scorecard")

scorecard = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Profitable": "mean",
        "Revenue Efficiency": "mean",
        "Valuation Efficiency": "mean",
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean"
    })
    .reset_index()
)

scorecard["Profitability Rate"] = (
    scorecard["Profitable"] * 100
)

st.dataframe(
    scorecard[
        [
            "Industry",
            "Profitability Rate",
            "Revenue Efficiency",
            "Valuation Efficiency",
            "Revenue (M USD)",
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# =====================================================
# AI INSIGHTS
# =====================================================

st.subheader("🧠 Profitability Insights")

best_industry = (
    industry_profit
    .sort_values(
        "Profitable",
        ascending=False
    )
    .iloc[0]["Industry"]
)

best_region = (
    regional_profit
    .sort_values(
        "Profitable",
        ascending=False
    )
    .iloc[0]["Region"]
)

best_efficiency = (
    efficiency
    .sort_values(
        "Revenue Efficiency",
        ascending=False
    )
    .iloc[0]["Industry"]
)

top_company = (
    leaders.iloc[0]["Startup Name"]
)

st.success(
    f"🏆 Most profitable industry: {best_industry}"
)

st.success(
    f"🌎 Most profitable region: {best_region}"
)

st.success(
    f"⚡ Highest revenue efficiency industry: {best_efficiency}"
)

st.success(
    f"🚀 Top profitability startup: {top_company}"
)

# =====================================================
# LEADERBOARD TABLE
# =====================================================

st.subheader("📊 Startup Profitability Leaderboard")

leaderboard = (
    filtered_df[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Revenue (M USD)",
            "Funding Amount (M USD)",
            "Valuation (M USD)",
            "Revenue Efficiency",
            "Profitability Score",
            "Profitable"
        ]
    ]
    .sort_values(
        "Profitability Score",
        ascending=False
    )
)

st.dataframe(
    leaderboard,
    use_container_width=True
)

# =====================================================
# DOWNLOAD REPORT
# =====================================================

csv = leaderboard.to_csv(index=False)

st.download_button(
    label="⬇ Download Profitability Report",
    data=csv,
    file_name="profitability_insights_report.csv",
    mime="text/csv"
)
