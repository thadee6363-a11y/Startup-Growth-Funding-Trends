import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="AI Insights",
    page_icon="🧠",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():
    return pd.read_csv("startup_data.csv")

df = load_data()

# ======================================================
# HEADER
# ======================================================

st.title("🧠 AI Insights Engine")
st.caption(
    "Automated executive intelligence, opportunity detection and strategic recommendations"
)

# ======================================================
# FILTERS
# ======================================================

st.sidebar.header("AI Filters")

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

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter))
].copy()

# ======================================================
# FEATURE ENGINEERING
# ======================================================

filtered_df["Valuation Multiple"] = (
    filtered_df["Valuation (M USD)"]
    /
    filtered_df["Revenue (M USD)"]
)

filtered_df["Funding Efficiency"] = (
    filtered_df["Revenue (M USD)"]
    /
    filtered_df["Funding Amount (M USD)"]
)

filtered_df["Success Score"] = (
    filtered_df["Revenue (M USD)"] * 0.30
    +
    filtered_df["Valuation (M USD)"] * 0.25
    +
    filtered_df["Market Share (%)"] * 25
    +
    filtered_df["Profitable"].astype(int) * 500
)

# ======================================================
# EXECUTIVE KPIs
# ======================================================

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Startups",
    len(filtered_df)
)

c2.metric(
    "Funding",
    f"${filtered_df['Funding Amount (M USD)'].sum():,.0f}M"
)

c3.metric(
    "Revenue",
    f"${filtered_df['Revenue (M USD)'].sum():,.0f}M"
)

c4.metric(
    "Profitability",
    f"{filtered_df['Profitable'].mean()*100:.1f}%"
)

st.divider()

# ======================================================
# EXECUTIVE SUMMARY
# ======================================================

st.subheader("📋 Executive Summary")

top_industry = (
    filtered_df
    .groupby("Industry")
    ["Revenue (M USD)"]
    .mean()
    .idxmax()
)

top_region = (
    filtered_df
    .groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

top_startup = (
    filtered_df
    .sort_values(
        "Success Score",
        ascending=False
    )
    .iloc[0]["Startup Name"]
)

profitability_rate = (
    filtered_df["Profitable"]
    .mean()
    * 100
)

st.info(f"""
### Executive Narrative

• The strongest performing sector is **{top_industry}**.

• The leading startup ecosystem is **{top_region}**.

• The highest-ranked startup is **{top_startup}**.

• Overall profitability across startups is **{profitability_rate:.1f}%**.

• Revenue growth and valuation remain strongly correlated across the ecosystem.
""")

# ======================================================
# INDUSTRY INSIGHTS
# ======================================================

st.subheader("🏭 Industry Intelligence")

industry = (
    filtered_df
    .groupby("Industry")
    .agg({
        "Funding Amount (M USD)": "sum",
        "Revenue (M USD)": "sum",
        "Valuation (M USD)": "mean",
        "Profitable": "mean"
    })
    .reset_index()
)

industry["Profitability Rate"] = (
    industry["Profitable"] * 100
)

fig = px.bar(
    industry,
    x="Industry",
    y="Revenue (M USD)",
    color="Industry",
    title="Industry Revenue Leadership"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

best_industry = (
    industry
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Industry"]
)

st.success(
    f"AI Insight: {best_industry} currently generates the highest economic output."
)

# ======================================================
# REGIONAL INSIGHTS
# ======================================================

st.subheader("🌎 Regional Intelligence")

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

fig = px.treemap(
    regional,
    path=["Region"],
    values="Revenue (M USD)",
    color="Valuation (M USD)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

best_region = (
    regional
    .sort_values(
        "Revenue (M USD)",
        ascending=False
    )
    .iloc[0]["Region"]
)

st.success(
    f"AI Insight: {best_region} is the strongest startup ecosystem by revenue generation."
)

# ======================================================
# VALUATION INSIGHTS
# ======================================================

st.subheader("📈 Valuation Intelligence")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    size="Funding Amount (M USD)",
    color="Industry",
    hover_name="Startup Name"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

highest_multiple = (
    filtered_df
    .sort_values(
        "Valuation Multiple",
        ascending=False
    )
    .iloc[0]
)

st.success(
    f"AI Insight: {highest_multiple['Startup Name']} has the highest valuation multiple ({highest_multiple['Valuation Multiple']:.2f}x)."
)

# ======================================================
# PROFITABILITY INSIGHTS
# ======================================================

st.subheader("💵 Profitability Intelligence")

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
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

best_profit = (
    profitability
    .sort_values(
        "Profitable",
        ascending=False
    )
    .iloc[0]["Industry"]
)

st.success(
    f"AI Insight: {best_profit} has the highest profitability rate."
)

# ======================================================
# OPPORTUNITY DETECTION
# ======================================================

st.subheader("🎯 Opportunity Detection")

opportunities = filtered_df[
    (filtered_df["Funding Efficiency"] > filtered_df["Funding Efficiency"].median())
    &
    (filtered_df["Profitable"] == True)
]

st.metric(
    "High-Potential Opportunities",
    len(opportunities)
)

st.dataframe(
    opportunities[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Funding Efficiency",
            "Revenue (M USD)",
            "Valuation (M USD)"
        ]
    ].head(15),
    use_container_width=True
)

# ======================================================
# RISK DETECTION
# ======================================================

st.subheader("⚠ Risk Detection")

risks = filtered_df[
    (
        filtered_df["Valuation Multiple"]
        >
        filtered_df["Valuation Multiple"].quantile(0.90)
    )
]

st.metric(
    "Potential Overvaluation Cases",
    len(risks)
)

st.dataframe(
    risks[
        [
            "Startup Name",
            "Industry",
            "Valuation Multiple",
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# ======================================================
# TOP STARTUPS
# ======================================================

st.subheader("🚀 AI Startup Ranking")

ranking = (
    filtered_df[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Success Score"
        ]
    ]
    .sort_values(
        "Success Score",
        ascending=False
    )
)

fig = px.bar(
    ranking.head(15),
    x="Startup Name",
    y="Success Score",
    color="Industry"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ======================================================
# STRATEGIC RECOMMENDATIONS
# ======================================================

st.subheader("🎯 Strategic Recommendations")

recommendations = []

recommendations.append(
    f"Increase investment focus toward {best_industry} due to strong revenue generation."
)

recommendations.append(
    f"Expand ecosystem initiatives in {best_region} where startup productivity is highest."
)

recommendations.append(
    "Prioritize startups showing both profitability and high funding efficiency."
)

recommendations.append(
    "Monitor companies with excessive valuation multiples for potential valuation risk."
)

recommendations.append(
    "Use profitability as a stronger decision factor than funding volume alone."
)

for rec in recommendations:
    st.success(rec)

# ======================================================
# EXECUTIVE REPORT
# ======================================================

st.subheader("📄 Executive Report")

report = pd.DataFrame({
    "Metric":[
        "Top Industry",
        "Top Region",
        "Top Startup",
        "Profitability Rate"
    ],
    "Value":[
        top_industry,
        top_region,
        top_startup,
        f"{profitability_rate:.1f}%"
    ]
})

st.dataframe(
    report,
    use_container_width=True
)

# ======================================================
# DOWNLOAD
# ======================================================

report_csv = ranking.to_csv(index=False)

st.download_button(
    label="⬇ Download AI Executive Report",
    data=report_csv,
    file_name=f"AI_Report_{datetime.now().date()}.csv",
    mime="text/csv"
)
