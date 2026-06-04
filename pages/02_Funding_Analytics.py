import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Funding Analytics",
    page_icon="💰",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
}

.metric-card{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 4px 10px rgba(0,0,0,.08);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("Funding Filters")

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

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
].copy()

# =========================================================
# HEADER
# =========================================================

st.title("💰 Funding Analytics")
st.caption(
    "Investor-grade funding intelligence and capital flow analytics"
)

# =========================================================
# KPI SECTION
# =========================================================

total_funding = filtered_df["Funding Amount (M USD)"].sum()

avg_funding = filtered_df["Funding Amount (M USD)"].mean()

median_funding = filtered_df["Funding Amount (M USD)"].median()

avg_rounds = filtered_df["Funding Rounds"].mean()

largest_round = filtered_df["Funding Amount (M USD)"].max()

funded_startups = len(filtered_df)

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Total Funding",
    f"${total_funding:,.0f}M"
)

c2.metric(
    "Avg Funding",
    f"${avg_funding:,.1f}M"
)

c3.metric(
    "Median Funding",
    f"${median_funding:,.1f}M"
)

c4.metric(
    "Avg Rounds",
    f"{avg_rounds:.1f}"
)

c5.metric(
    "Largest Funding",
    f"${largest_round:,.0f}M"
)

c6.metric(
    "Funded Startups",
    f"{funded_startups:,}"
)

st.divider()

# =========================================================
# FUNDING DISTRIBUTION
# =========================================================

st.subheader("Funding Distribution")

left,right = st.columns(2)

with left:

    fig = px.histogram(
        filtered_df,
        x="Funding Amount (M USD)",
        nbins=30,
        title="Funding Amount Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.box(
        filtered_df,
        y="Funding Amount (M USD)",
        color="Industry",
        title="Funding Spread"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# FUNDING BY INDUSTRY
# =========================================================

st.subheader("Industry Funding Analysis")

industry_funding = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean"
    })
    .reset_index()
)

fig = px.bar(
    industry_funding,
    x="Industry",
    y="Funding Amount (M USD)",
    color="Industry",
    title="Capital Allocation by Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# FUNDING EFFICIENCY
# =========================================================

st.subheader("Funding Efficiency")

filtered_df["Funding Efficiency"] = (
    filtered_df["Revenue (M USD)"]
    /
    filtered_df["Funding Amount (M USD)"]
)

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
    title="Revenue Generated Per Funding Dollar"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# FUNDING VS REVENUE
# =========================================================

st.subheader("Funding vs Revenue")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    size="Valuation (M USD)",
    color="Industry",
    hover_name="Startup Name",
    title="Capital Efficiency Map"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# FUNDING ROUNDS ANALYSIS
# =========================================================

st.subheader("Funding Rounds Analysis")

round_analysis = (
    filtered_df
    .groupby("Funding Rounds")
    .agg({
        "Funding Amount (M USD)": "mean",
        "Valuation (M USD)": "mean",
        "Revenue (M USD)": "mean"
    })
    .reset_index()
)

fig = px.line(
    round_analysis,
    x="Funding Rounds",
    y="Valuation (M USD)",
    markers=True,
    title="Average Valuation by Funding Rounds"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# REGIONAL FUNDING
# =========================================================

st.subheader("Regional Funding Intelligence")

regional = (
    filtered_df
    .groupby("Region")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum"
    })
    .reset_index()
)

fig = px.treemap(
    regional,
    path=["Region"],
    values="Funding Amount (M USD)",
    color="Revenue (M USD)",
    title="Regional Capital Allocation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# FUNDING CONCENTRATION
# =========================================================

st.subheader("Funding Concentration Risk")

top10_share = (
    filtered_df
    .nlargest(
        10,
        "Funding Amount (M USD)"
    )["Funding Amount (M USD)"]
    .sum()
)

market_share = (
    top10_share /
    filtered_df["Funding Amount (M USD)"].sum()
) * 100

st.metric(
    "Top 10 Funding Concentration",
    f"{market_share:.1f}%"
)

fig = px.pie(
    filtered_df.nlargest(
        15,
        "Funding Amount (M USD)"
    ),
    names="Startup Name",
    values="Funding Amount (M USD)",
    title="Largest Funded Startups"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =========================================================
# TOP FUNDED STARTUPS
# =========================================================

st.subheader("Top Funded Startups")

top_funded = (
    filtered_df
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    top_funded[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Funding Amount (M USD)",
            "Funding Rounds",
            "Valuation (M USD)",
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

# =========================================================
# INVESTOR INSIGHTS
# =========================================================

st.subheader("📈 Investor Insights")

highest_funded_industry = (
    industry_funding
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .iloc[0]["Industry"]
)

best_efficiency = (
    efficiency
    .sort_values(
        "Funding Efficiency",
        ascending=False
    )
    .iloc[0]["Industry"]
)

largest_region = (
    regional
    .sort_values(
        "Funding Amount (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

st.success(
    f"🏆 Highest funded sector: {highest_funded_industry}"
)

st.success(
    f"⚡ Most capital-efficient sector: {best_efficiency}"
)

st.success(
    f"🌎 Largest funded region: {largest_region}"
)

st.success(
    f"💰 Top 10 startups control {market_share:.1f}% of total funding"
)

# =========================================================
# DOWNLOAD REPORT
# =========================================================

csv = top_funded.to_csv(index=False)

st.download_button(
    label="⬇ Download Funding Report",
    data=csv,
    file_name="funding_analytics_report.csv",
    mime="text/csv"
)
