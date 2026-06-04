import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Startup Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.metric-container {
    background: #1e293b;
    padding: 15px;
    border-radius: 12px;
    text-align:center;
}

h1,h2,h3 {
    color:white;
}

[data-testid="stSidebar"]{
    background:#111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("startup_data.csv")

    return df

df = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🚀 Startup Intelligence")

industry_filter = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region_filter = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

exit_filter = st.sidebar.multiselect(
    "Exit Status",
    options=df["Exit Status"].unique(),
    default=df["Exit Status"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Region"].isin(region_filter)) &
    (df["Exit Status"].isin(exit_filter))
]

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🚀 Startup Intelligence Platform")
st.caption("Deep Analytics | Funding Intelligence | Valuation Prediction")

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

st.subheader("Executive Dashboard")

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Startups",
    f"{len(filtered_df):,}"
)

c2.metric(
    "Total Funding",
    f"${filtered_df['Funding Amount (M USD)'].sum():,.0f}M"
)

c3.metric(
    "Avg Valuation",
    f"${filtered_df['Valuation (M USD)'].mean():,.0f}M"
)

c4.metric(
    "Revenue",
    f"${filtered_df['Revenue (M USD)'].sum():,.0f}M"
)

c5.metric(
    "Employees",
    f"{filtered_df['Employees'].sum():,}"
)

c6.metric(
    "Profitability %",
    f"{filtered_df['Profitable'].mean()*100:.1f}%"
)

st.divider()

# ---------------------------------------------------
# FUNDING VS REVENUE
# ---------------------------------------------------

st.subheader("Funding Intelligence")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Revenue (M USD)",
    size="Valuation (M USD)",
    color="Industry",
    hover_name="Startup Name",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# INDUSTRY FUNDING
# ---------------------------------------------------

col1,col2 = st.columns(2)

with col1:

    industry_funding = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        title="Funding by Industry"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    industry_revenue = (
        filtered_df.groupby("Industry")
        ["Revenue (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        industry_revenue,
        names="Industry",
        values="Revenue (M USD)",
        title="Revenue Share"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# VALUATION ANALYTICS
# ---------------------------------------------------

st.subheader("Valuation Intelligence")

filtered_df["Valuation Multiple"] = (
    filtered_df["Valuation (M USD)"] /
    filtered_df["Revenue (M USD)"]
)

fig = px.box(
    filtered_df,
    x="Industry",
    y="Valuation Multiple",
    color="Industry"
)

st.plotly_chart(fig, use_container_width=True)

top_valued = filtered_df.nlargest(
    10,
    "Valuation Multiple"
)

st.dataframe(
    top_valued[
        [
            "Startup Name",
            "Industry",
            "Valuation Multiple",
            "Valuation (M USD)"
        ]
    ]
)

# ---------------------------------------------------
# PROFITABILITY
# ---------------------------------------------------

st.subheader("Profitability Insights")

profitability = (
    filtered_df.groupby("Industry")
    ["Profitable"]
    .mean()
    .reset_index()
)

fig = px.bar(
    profitability,
    x="Industry",
    y="Profitable",
    color="Industry",
    title="Industry Profitability"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# REGIONAL ANALYSIS
# ---------------------------------------------------

st.subheader("Regional Intelligence")

regional = (
    filtered_df.groupby("Region")
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
    values="Funding Amount (M USD)",
    color="Revenue (M USD)"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# EXIT ANALYSIS
# ---------------------------------------------------

st.subheader("Exit Analysis")

exit_stats = (
    filtered_df.groupby("Exit Status")
    .agg({
        "Revenue (M USD)": "mean",
        "Valuation (M USD)": "mean"
    })
    .reset_index()
)

fig = px.bar(
    exit_stats,
    x="Exit Status",
    y="Valuation (M USD)",
    color="Exit Status"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# CORRELATION HEATMAP
# ---------------------------------------------------

st.subheader("Correlation Analysis")

numeric_cols = filtered_df.select_dtypes(
    include=np.number
)

corr = numeric_cols.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# SUCCESS SCORE
# ---------------------------------------------------

st.subheader("Startup Success Engine")

filtered_df["Success Score"] = (
    filtered_df["Revenue (M USD)"] * 0.3
    +
    filtered_df["Valuation (M USD)"] * 0.2
    +
    filtered_df["Market Share (%)"] * 20
    +
    filtered_df["Profitable"] * 500
)

top_success = filtered_df.nlargest(
    15,
    "Success Score"
)

fig = px.bar(
    top_success,
    x="Startup Name",
    y="Success Score",
    color="Industry"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# ML VALUATION PREDICTION
# ---------------------------------------------------

st.subheader("AI Valuation Predictor")

features = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

X = df[features]
y = df["Valuation (M USD)"]

X_train,X_test,y_train,y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

model.fit(X_train,y_train)

preds = model.predict(X_test)

r2 = r2_score(y_test,preds)

st.info(f"Model R² Score : {r2:.3f}")

col1,col2,col3,col4,col5 = st.columns(5)

funding = col1.number_input(
    "Funding",
    value=50.0
)

rounds = col2.number_input(
    "Rounds",
    value=3
)

revenue = col3.number_input(
    "Revenue",
    value=20.0
)

employees = col4.number_input(
    "Employees",
    value=200
)

market_share = col5.number_input(
    "Market Share %",
    value=5.0
)

if st.button("Predict Valuation"):

    prediction = model.predict(
        [[
            funding,
            rounds,
            revenue,
            employees,
            market_share
        ]]
    )[0]

    st.success(
        f"Predicted Valuation = ${prediction:,.2f} Million"
    )

# ---------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------

st.subheader("🤖 Automated Insights")

highest_funding_industry = (
    filtered_df.groupby("Industry")
    ["Funding Amount (M USD)"]
    .mean()
    .idxmax()
)

highest_revenue_industry = (
    filtered_df.groupby("Industry")
    ["Revenue (M USD)"]
    .mean()
    .idxmax()
)

best_region = (
    filtered_df.groupby("Region")
    ["Valuation (M USD)"]
    .mean()
    .idxmax()
)

profit_rate = (
    filtered_df["Profitable"]
    .mean()
    *100
)

st.success(
    f"🏆 Highest funded industry: {highest_funding_industry}"
)

st.success(
    f"💰 Highest revenue industry: {highest_revenue_industry}"
)

st.success(
    f"🌎 Best valuation region: {best_region}"
)

st.success(
    f"📈 Profitability rate: {profit_rate:.1f}%"
)

# ---------------------------------------------------
# RAW DATA
# ---------------------------------------------------

with st.expander("View Dataset"):

    st.dataframe(filtered_df)

# ---------------------------------------------------
# DOWNLOAD
# ---------------------------------------------------

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="startup_analysis.csv",
    mime="text/csv"
)
