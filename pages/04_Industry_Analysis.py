import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Industry Analysis",
    page_icon="🏭",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# ==========================================================
# HEADER
# ==========================================================

st.title("🏭 Industry Intelligence")
st.caption(
    "Deep sector benchmarking, competitive intelligence and industry performance analysis"
)

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Industry Filters")

selected_industries = st.sidebar.multiselect(
    "Industries",
    sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

selected_regions = st.sidebar.multiselect(
    "Regions",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

filtered_df = df[
    (df["Industry"].isin(selected_industries)) &
    (df["Region"].isin(selected_regions))
].copy()

# ==========================================================
# INDUSTRY AGGREGATION
# ==========================================================

industry_df = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean",
        "Employees": "sum",
        "Market Share (%)": "mean",
        "Profitable": "mean"
    })
    .reset_index()
)

industry_df["Profitability Rate"] = (
    industry_df["Profitable"] * 100
)

industry_df["Funding Efficiency"] = (
    industry_df["Revenue (M USD)"] /
    industry_df["Funding Amount (M USD)"]
)

industry_df["Industry Score"] = (
    industry_df["Revenue (M USD)"] * 0.30
    +
    industry_df["Valuation (M USD)"] * 0.25
    +
    industry_df["Market Share (%)"] * 50
    +
    industry_df["Profitability Rate"] * 5
)

# ==========================================================
# KPI SECTION
# ==========================================================

industry_count = filtered_df["Industry"].nunique()

largest_industry = (
    industry_df.sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Industry"]
)

highest_valuation = (
    industry_df["Valuation (M USD)"]
    .max()
)

best_profitability = (
    industry_df["Profitability Rate"]
    .max()
)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Industries",
    industry_count
)

c2.metric(
    "Largest Sector",
    largest_industry
)

c3.metric(
    "Highest Avg Valuation",
    f"${highest_valuation:,.0f}M"
)

c4.metric(
    "Best Profitability",
    f"{best_profitability:.1f}%"
)

st.divider()

# ==========================================================
# INDUSTRY SCOREBOARD
# ==========================================================

st.subheader("🏆 Industry Ranking")

ranking = (
    industry_df
    .sort_values(
        "Industry Score",
        ascending=False
    )
)

fig = px.bar(
    ranking,
    x="Industry",
    y="Industry Score",
    color="Industry",
    title="Industry Competitiveness Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# FUNDING VS REVENUE
# ==========================================================

st.subheader("Funding vs Revenue by Industry")

fig = px.scatter(
    industry_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    size="Valuation (M USD)",
    color="Industry",
    hover_name="Industry",
    title="Industry Capital Efficiency Map"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# FUNDING ANALYSIS
# ==========================================================

st.subheader("💰 Funding Intelligence")

col1,col2 = st.columns(2)

with col1:

    fig = px.bar(
        industry_df,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="Funding by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.pie(
        industry_df,
        names="Industry",
        values="Funding Amount (M USD)",
        title="Funding Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# REVENUE ANALYSIS
# ==========================================================

st.subheader("📈 Revenue Intelligence")

fig = px.treemap(
    industry_df,
    path=["Industry"],
    values="Revenue (M USD)",
    color="Revenue (M USD)",
    title="Revenue Contribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# VALUATION BENCHMARK
# ==========================================================

st.subheader("📊 Valuation Benchmark")

fig = px.bar(
    industry_df,
    x="Industry",
    y="Valuation (M USD)",
    color="Industry",
    title="Average Industry Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# PROFITABILITY ANALYSIS
# ==========================================================

st.subheader("🏆 Profitability Analysis")

fig = px.bar(
    industry_df,
    x="Industry",
    y="Profitability Rate",
    color="Industry",
    title="Industry Profitability"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# MARKET SHARE ANALYSIS
# ==========================================================

st.subheader("📌 Market Share Analysis")

fig = px.bar(
    industry_df,
    x="Industry",
    y="Market Share (%)",
    color="Industry",
    title="Average Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# EMPLOYEE SCALE
# ==========================================================

st.subheader("👥 Workforce Distribution")

fig = px.sunburst(
    industry_df,
    path=["Industry"],
    values="Employees",
    color="Employees"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# FUNDING EFFICIENCY
# ==========================================================

st.subheader("⚡ Funding Efficiency")

efficiency_rank = (
    industry_df
    .sort_values(
        "Funding Efficiency",
        ascending=False
    )
)

fig = px.bar(
    efficiency_rank,
    x="Industry",
    y="Funding Efficiency",
    color="Industry",
    title="Revenue Generated Per Funding Dollar"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# EXIT STATUS ANALYSIS
# ==========================================================

st.subheader("🚀 Exit Success Analysis")

exit_analysis = (
    filtered_df
    .groupby(
        ["Industry", "Exit Status"]
    )
    .size()
    .reset_index(name="Count")
)

fig = px.sunburst(
    exit_analysis,
    path=["Industry", "Exit Status"],
    values="Count",
    title="Industry Exit Outcomes"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# RADAR COMPARISON
# ==========================================================

st.subheader("Industry Radar Comparison")

compare_industries = st.multiselect(
    "Compare Industries",
    industry_df["Industry"].tolist(),
    default=industry_df["Industry"].tolist()[:3]
)

if len(compare_industries) > 0:

    radar_df = industry_df[
        industry_df["Industry"].isin(compare_industries)
    ]

    metrics = [
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Valuation (M USD)",
        "Market Share (%)",
        "Profitability Rate"
    ]

    fig = go.Figure()

    for _, row in radar_df.iterrows():

        fig.add_trace(
            go.Scatterpolar(
                r=[row[m] for m in metrics],
                theta=metrics,
                fill='toself',
                name=row["Industry"]
            )
        )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# INDUSTRY LEADERBOARD
# ==========================================================

st.subheader("📋 Industry Scorecard")

leaderboard = (
    industry_df[
        [
            "Industry",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Profitability Rate",
            "Market Share (%)",
            "Funding Efficiency",
            "Industry Score"
        ]
    ]
    .sort_values(
        "Industry Score",
        ascending=False
    )
)

st.dataframe(
    leaderboard,
    use_container_width=True
)

# ==========================================================
# AI INSIGHTS
# ==========================================================

st.subheader("🧠 Industry Insights")

top_revenue = (
    industry_df
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Industry"]
)

top_profitability = (
    industry_df
    .sort_values(
        "Profitability Rate",
        ascending=False
    )
    .iloc[0]["Industry"]
)

top_efficiency = (
    industry_df
    .sort_values(
        "Funding Efficiency",
        ascending=False
    )
    .iloc[0]["Industry"]
)

top_score = (
    industry_df
    .sort_values(
        "Industry Score",
        ascending=False
    )
    .iloc[0]["Industry"]
)

st.success(
    f"💰 Highest revenue industry: {top_revenue}"
)

st.success(
    f"🏆 Most profitable industry: {top_profitability}"
)

st.success(
    f"⚡ Most capital-efficient industry: {top_efficiency}"
)

st.success(
    f"🚀 Strongest overall industry: {top_score}"
)

# ==========================================================
# DOWNLOAD
# ==========================================================

csv = leaderboard.to_csv(index=False)

st.download_button(
    label="⬇ Download Industry Report",
    data=csv,
    file_name="industry_analysis_report.csv",
    mime="text/csv"
)
