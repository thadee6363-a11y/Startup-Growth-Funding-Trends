import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Regional Analysis",
    page_icon="🌎",
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

st.title("🌎 Regional Intelligence")
st.caption(
    "Analyze startup ecosystems, funding concentration, revenue generation and regional competitiveness"
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Regional Filters")

industries = st.sidebar.multiselect(
    "Industry",
    sorted(df["Industry"].unique()),
    default=sorted(df["Industry"].unique())
)

exit_status = st.sidebar.multiselect(
    "Exit Status",
    sorted(df["Exit Status"].unique()),
    default=sorted(df["Exit Status"].unique())
)

filtered_df = df[
    (df["Industry"].isin(industries)) &
    (df["Exit Status"].isin(exit_status))
].copy()

# ==========================================================
# REGIONAL AGGREGATION
# ==========================================================

regional = (
    filtered_df
    .groupby("Region")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean",
        "Employees": "sum",
        "Market Share (%)": "mean",
        "Profitable": "mean",
        "Startup Name": "count"
    })
    .reset_index()
)

regional.rename(
    columns={
        "Startup Name": "Startup Count"
    },
    inplace=True
)

regional["Profitability Rate"] = (
    regional["Profitable"] * 100
)

regional["Funding Efficiency"] = (
    regional["Revenue (M USD)"]
    /
    regional["Funding Amount (M USD)"]
)

regional["Regional Score"] = (
    regional["Revenue (M USD)"] * 0.30
    +
    regional["Valuation (M USD)"] * 0.25
    +
    regional["Market Share (%)"] * 50
    +
    regional["Profitability Rate"] * 5
)

# ==========================================================
# KPI SECTION
# ==========================================================

regions = regional["Region"].nunique()

top_region = (
    regional.sort_values(
        "Regional Score",
        ascending=False
    )
    .iloc[0]["Region"]
)

total_funding = (
    regional["Funding Amount (M USD)"]
    .sum()
)

total_revenue = (
    regional["Revenue (M USD)"]
    .sum()
)

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Regions",
    regions
)

c2.metric(
    "Top Ecosystem",
    top_region
)

c3.metric(
    "Funding",
    f"${total_funding:,.0f}M"
)

c4.metric(
    "Revenue",
    f"${total_revenue:,.0f}M"
)

st.divider()

# ==========================================================
# REGIONAL SCOREBOARD
# ==========================================================

st.subheader("🏆 Regional Competitiveness")

scoreboard = (
    regional
    .sort_values(
        "Regional Score",
        ascending=False
    )
)

fig = px.bar(
    scoreboard,
    x="Region",
    y="Regional Score",
    color="Region",
    title="Regional Competitiveness Score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# FUNDING ANALYSIS
# ==========================================================

st.subheader("💰 Funding Landscape")

col1,col2 = st.columns(2)

with col1:

    fig = px.bar(
        regional,
        x="Region",
        y="Funding Amount (M USD)",
        color="Region",
        title="Funding by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.pie(
        regional,
        names="Region",
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

st.subheader("📈 Revenue Analysis")

fig = px.treemap(
    regional,
    path=["Region"],
    values="Revenue (M USD)",
    color="Revenue (M USD)",
    title="Revenue Contribution by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# VALUATION BENCHMARK
# ==========================================================

st.subheader("📊 Regional Valuation Benchmark")

fig = px.bar(
    regional,
    x="Region",
    y="Valuation (M USD)",
    color="Region",
    title="Average Valuation by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# FUNDING VS REVENUE
# ==========================================================

st.subheader("Funding vs Revenue")

fig = px.scatter(
    regional,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    size="Valuation (M USD)",
    color="Region",
    hover_name="Region",
    title="Regional Capital Efficiency"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# STARTUP DENSITY
# ==========================================================

st.subheader("🏢 Startup Density")

fig = px.bar(
    regional,
    x="Region",
    y="Startup Count",
    color="Region",
    title="Number of Startups by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# PROFITABILITY
# ==========================================================

st.subheader("🏆 Profitability Benchmark")

fig = px.bar(
    regional,
    x="Region",
    y="Profitability Rate",
    color="Region",
    title="Profitability Rate by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# WORKFORCE ANALYSIS
# ==========================================================

st.subheader("👥 Workforce Distribution")

fig = px.sunburst(
    regional,
    path=["Region"],
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

st.subheader("⚡ Capital Efficiency")

efficiency = (
    regional
    .sort_values(
        "Funding Efficiency",
        ascending=False
    )
)

fig = px.bar(
    efficiency,
    x="Region",
    y="Funding Efficiency",
    color="Region",
    title="Revenue Generated Per Funding Dollar"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# EXIT ANALYSIS
# ==========================================================

st.subheader("🚀 Exit Outcomes")

exit_analysis = (
    filtered_df
    .groupby(
        ["Region", "Exit Status"]
    )
    .size()
    .reset_index(name="Count")
)

fig = px.sunburst(
    exit_analysis,
    path=["Region", "Exit Status"],
    values="Count",
    title="Exit Distribution by Region"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# INDUSTRY MIX
# ==========================================================

st.subheader("🏭 Industry Mix by Region")

industry_mix = (
    filtered_df
    .groupby(
        ["Region", "Industry"]
    )
    .size()
    .reset_index(name="Count")
)

fig = px.sunburst(
    industry_mix,
    path=["Region", "Industry"],
    values="Count",
    title="Industry Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REGIONAL COMPARISON
# ==========================================================

st.subheader("📡 Regional Radar Comparison")

selected_regions = st.multiselect(
    "Compare Regions",
    regional["Region"].tolist(),
    default=regional["Region"].tolist()[:3]
)

if len(selected_regions) > 0:

    compare_df = regional[
        regional["Region"].isin(selected_regions)
    ]

    metrics = [
        "Funding Amount (M USD)",
        "Revenue (M USD)",
        "Valuation (M USD)",
        "Profitability Rate",
        "Startup Count"
    ]

    fig = go.Figure()

    for _, row in compare_df.iterrows():

        fig.add_trace(
            go.Scatterpolar(
                r=[row[m] for m in metrics],
                theta=metrics,
                fill='toself',
                name=row["Region"]
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        showlegend=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# LEADERBOARD
# ==========================================================

st.subheader("📋 Regional Scorecard")

leaderboard = (
    regional[
        [
            "Region",
            "Startup Count",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Profitability Rate",
            "Funding Efficiency",
            "Regional Score"
        ]
    ]
    .sort_values(
        "Regional Score",
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

st.subheader("🧠 Regional Insights")

best_funding = (
    regional
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

best_revenue = (
    regional
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

best_profitability = (
    regional
    .sort_values(
        "Profitability Rate",
        ascending=False
    )
    .iloc[0]["Region"]
)

best_efficiency = (
    regional
    .sort_values(
        "Funding Efficiency",
        ascending=False
    )
    .iloc[0]["Region"]
)

st.success(
    f"💰 Highest funded ecosystem: {best_funding}"
)

st.success(
    f"📈 Highest revenue ecosystem: {best_revenue}"
)

st.success(
    f"🏆 Most profitable ecosystem: {best_profitability}"
)

st.success(
    f"⚡ Most capital-efficient ecosystem: {best_efficiency}"
)

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

csv = leaderboard.to_csv(index=False)

st.download_button(
    label="⬇ Download Regional Report",
    data=csv,
    file_name="regional_analysis_report.csv",
    mime="text/csv"
)
