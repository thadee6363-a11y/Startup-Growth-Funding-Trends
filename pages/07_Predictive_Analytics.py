import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    r2_score,
    accuracy_score
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Predictive Analytics",
    page_icon="🤖",
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

st.title("🤖 Predictive Analytics")
st.caption(
    "Machine Learning powered valuation, revenue and profitability forecasting"
)

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

features = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Employees",
    "Revenue (M USD)",
    "Market Share (%)"
]

# ==========================================================
# VALUATION MODEL
# ==========================================================

X_val = df[features]

y_val = df["Valuation (M USD)"]

X_train, X_test, y_train, y_test = train_test_split(
    X_val,
    y_val,
    test_size=0.2,
    random_state=42
)

valuation_model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

valuation_model.fit(
    X_train,
    y_train
)

valuation_pred = valuation_model.predict(
    X_test
)

valuation_r2 = r2_score(
    y_test,
    valuation_pred
)

# ==========================================================
# REVENUE MODEL
# ==========================================================

revenue_features = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Employees",
    "Market Share (%)"
]

X_rev = df[revenue_features]

y_rev = df["Revenue (M USD)"]

X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(
    X_rev,
    y_rev,
    test_size=0.2,
    random_state=42
)

revenue_model = RandomForestRegressor(
    n_estimators=300,
    random_state=42
)

revenue_model.fit(
    X_train_r,
    y_train_r
)

revenue_pred = revenue_model.predict(
    X_test_r
)

revenue_r2 = r2_score(
    y_test_r,
    revenue_pred
)

# ==========================================================
# PROFITABILITY MODEL
# ==========================================================

X_prof = df[features]

y_prof = df["Profitable"]

X_train_p, X_test_p, y_train_p, y_test_p = train_test_split(
    X_prof,
    y_prof,
    test_size=0.2,
    random_state=42
)

profit_model = RandomForestClassifier(
    n_estimators=300,
    random_state=42
)

profit_model.fit(
    X_train_p,
    y_train_p
)

profit_pred = profit_model.predict(
    X_test_p
)

profit_acc = accuracy_score(
    y_test_p,
    profit_pred
)

# ==========================================================
# KPI SECTION
# ==========================================================

c1, c2, c3 = st.columns(3)

c1.metric(
    "Valuation Model R²",
    f"{valuation_r2:.3f}"
)

c2.metric(
    "Revenue Model R²",
    f"{revenue_r2:.3f}"
)

c3.metric(
    "Profitability Accuracy",
    f"{profit_acc:.3f}"
)

st.divider()

# ==========================================================
# STARTUP SIMULATOR
# ==========================================================

st.subheader("🚀 Startup Growth Simulator")

col1, col2, col3 = st.columns(3)

with col1:

    funding = st.number_input(
        "Funding (M USD)",
        min_value=0.0,
        value=50.0
    )

    rounds = st.number_input(
        "Funding Rounds",
        min_value=1,
        value=3
    )

with col2:

    employees = st.number_input(
        "Employees",
        min_value=1,
        value=150
    )

    revenue = st.number_input(
        "Revenue (M USD)",
        min_value=0.0,
        value=20.0
    )

with col3:

    market_share = st.slider(
        "Market Share %",
        0.0,
        100.0,
        5.0
    )

# ==========================================================
# PREDICTION ENGINE
# ==========================================================

if st.button("Generate Predictions"):

    valuation_prediction = valuation_model.predict(
        [[
            funding,
            rounds,
            employees,
            revenue,
            market_share
        ]]
    )[0]

    revenue_prediction = revenue_model.predict(
        [[
            funding,
            rounds,
            employees,
            market_share
        ]]
    )[0]

    profitability_probability = (
        profit_model.predict_proba(
            [[
                funding,
                rounds,
                employees,
                revenue,
                market_share
            ]]
        )[0][1]
        * 100
    )

    success_score = (
        valuation_prediction * 0.30
        +
        revenue_prediction * 0.30
        +
        profitability_probability * 5
    )

    st.subheader("Prediction Results")

    r1, r2, r3, r4 = st.columns(4)

    r1.metric(
        "Predicted Valuation",
        f"${valuation_prediction:,.1f}M"
    )

    r2.metric(
        "Predicted Revenue",
        f"${revenue_prediction:,.1f}M"
    )

    r3.metric(
        "Profitability Chance",
        f"{profitability_probability:.1f}%"
    )

    r4.metric(
        "Success Score",
        f"{success_score:,.0f}"
    )

    # ------------------------------------------------------
    # Gauge
    # ------------------------------------------------------

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=profitability_probability,
            title={"text":"Profitability Probability"},
            gauge={
                "axis":{"range":[0,100]}
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

st.subheader("📊 Valuation Drivers")

importance = pd.DataFrame({

    "Feature": features,

    "Importance":
        valuation_model.feature_importances_

})

importance = importance.sort_values(
    "Importance",
    ascending=False
)

fig = px.bar(
    importance,
    x="Feature",
    y="Importance",
    title="Feature Importance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# ACTUAL VS PREDICTED
# ==========================================================

st.subheader("Actual vs Predicted Valuation")

compare_df = pd.DataFrame({

    "Actual": y_test,
    "Predicted": valuation_pred

})

fig = px.scatter(
    compare_df,
    x="Actual",
    y="Predicted",
    trendline="ols"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# VALUATION DISTRIBUTION
# ==========================================================

st.subheader("Valuation Prediction Distribution")

pred_df = pd.DataFrame({

    "Predicted Valuation":
        valuation_model.predict(
            X_val
        )

})

fig = px.histogram(
    pred_df,
    x="Predicted Valuation",
    nbins=25
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# REVENUE FORECASTING
# ==========================================================

st.subheader("Revenue Forecast Distribution")

rev_pred_df = pd.DataFrame({

    "Predicted Revenue":
        revenue_model.predict(
            X_rev
        )

})

fig = px.box(
    rev_pred_df,
    y="Predicted Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# WHAT-IF ANALYSIS
# ==========================================================

st.subheader("🔍 What-If Scenario Analysis")

scenario_funding = st.slider(
    "Increase Funding %",
    0,
    300,
    50
)

scenario_input = np.array([
    [
        funding * (1 + scenario_funding/100),
        rounds,
        employees,
        revenue,
        market_share
    ]
])

scenario_prediction = (
    valuation_model.predict(
        scenario_input
    )[0]
)

st.metric(
    "Scenario Valuation",
    f"${scenario_prediction:,.1f}M"
)

# ==========================================================
# STARTUP RANKING MODEL
# ==========================================================

st.subheader("🏆 ML Startup Ranking")

df["Predicted Valuation"] = (
    valuation_model.predict(X_val)
)

df["Predicted Revenue"] = (
    revenue_model.predict(X_rev)
)

df["Profitability Probability"] = (
    profit_model.predict_proba(X_prof)[:,1]
    * 100
)

df["ML Score"] = (
    df["Predicted Valuation"] * 0.30
    +
    df["Predicted Revenue"] * 0.30
    +
    df["Profitability Probability"] * 5
)

ranking = (
    df[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Predicted Valuation",
            "Predicted Revenue",
            "Profitability Probability",
            "ML Score"
        ]
    ]
    .sort_values(
        "ML Score",
        ascending=False
    )
)

st.dataframe(
    ranking.head(25),
    use_container_width=True
)

# ==========================================================
# AI INSIGHTS
# ==========================================================

st.subheader("🧠 Predictive Insights")

top_startup = ranking.iloc[0]["Startup Name"]

top_region = (
    df.groupby("Region")
    ["ML Score"]
    .mean()
    .idxmax()
)

top_industry = (
    df.groupby("Industry")
    ["ML Score"]
    .mean()
    .idxmax()
)

st.success(
    f"🚀 Highest ML-ranked startup: {top_startup}"
)

st.success(
    f"🌎 Highest potential region: {top_region}"
)

st.success(
    f"🏭 Highest potential industry: {top_industry}"
)

# ==========================================================
# DOWNLOAD REPORT
# ==========================================================

csv = ranking.to_csv(index=False)

st.download_button(
    label="⬇ Download ML Predictions",
    data=csv,
    file_name="predictive_analytics_report.csv",
    mime="text/csv"
)
