"""
=========================================================
ML MODELS ENGINE
Startup Intelligence Platform

Regression
Classification
Scoring
Forecasting
Scenario Analysis
=========================================================
"""

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from sklearn.ensemble import (
    RandomForestRegressor,
    RandomForestClassifier
)

from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

import joblib

# ==========================================================
# FEATURES
# ==========================================================

VALUATION_FEATURES = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Employees",
    "Revenue (M USD)",
    "Market Share (%)"
]

REVENUE_FEATURES = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Employees",
    "Market Share (%)"
]

PROFIT_FEATURES = [
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Employees",
    "Revenue (M USD)",
    "Market Share (%)"
]

# ==========================================================
# TRAIN VALUATION MODEL
# ==========================================================

def train_valuation_model(df):

    X = df[VALUATION_FEATURES]

    y = df["Valuation (M USD)"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {

        "R2":
            r2_score(y_test, predictions),

        "MAE":
            mean_absolute_error(
                y_test,
                predictions
            ),

        "RMSE":
            np.sqrt(
                mean_squared_error(
                    y_test,
                    predictions
                )
            )
    }

    return model, metrics

# ==========================================================
# TRAIN REVENUE MODEL
# ==========================================================

def train_revenue_model(df):

    X = df[REVENUE_FEATURES]

    y = df["Revenue (M USD)"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=500,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {

        "R2":
            r2_score(y_test, predictions),

        "MAE":
            mean_absolute_error(
                y_test,
                predictions
            ),

        "RMSE":
            np.sqrt(
                mean_squared_error(
                    y_test,
                    predictions
                )
            )
    }

    return model, metrics

# ==========================================================
# TRAIN PROFITABILITY MODEL
# ==========================================================

def train_profitability_model(df):

    X = df[PROFIT_FEATURES]

    y = df["Profitable"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=500,
        max_depth=10,
        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    metrics = {

        "Accuracy":
            accuracy_score(
                y_test,
                predictions
            ),

        "Precision":
            precision_score(
                y_test,
                predictions,
                zero_division=0
            ),

        "Recall":
            recall_score(
                y_test,
                predictions,
                zero_division=0
            ),

        "F1":
            f1_score(
                y_test,
                predictions,
                zero_division=0
            )
    }

    return model, metrics

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

def get_feature_importance(
    model,
    feature_names
):

    importance = pd.DataFrame({

        "Feature":
            feature_names,

        "Importance":
            model.feature_importances_

    })

    return importance.sort_values(
        "Importance",
        ascending=False
    )

# ==========================================================
# VALUATION PREDICTION
# ==========================================================

def predict_valuation(
    model,
    funding,
    rounds,
    employees,
    revenue,
    market_share
):

    prediction = model.predict(
        [[
            funding,
            rounds,
            employees,
            revenue,
            market_share
        ]]
    )

    return float(prediction[0])

# ==========================================================
# REVENUE PREDICTION
# ==========================================================

def predict_revenue(
    model,
    funding,
    rounds,
    employees,
    market_share
):

    prediction = model.predict(
        [[
            funding,
            rounds,
            employees,
            market_share
        ]]
    )

    return float(prediction[0])

# ==========================================================
# PROFITABILITY PROBABILITY
# ==========================================================

def predict_profitability(
    model,
    funding,
    rounds,
    employees,
    revenue,
    market_share
):

    probability = (

        model.predict_proba(
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

    return float(probability)

# ==========================================================
# SUCCESS SCORE
# ==========================================================

def calculate_ml_success_score(
    valuation,
    revenue,
    profitability
):

    score = (

        valuation * 0.30

        +

        revenue * 0.30

        +

        profitability * 5

    )

    return round(score, 2)

# ==========================================================
# STARTUP RANKING
# ==========================================================

def rank_startups(
    df,
    valuation_model,
    revenue_model,
    profit_model
):

    result = df.copy()

    result["Predicted Valuation"] = (
        valuation_model.predict(
            result[VALUATION_FEATURES]
        )
    )

    result["Predicted Revenue"] = (
        revenue_model.predict(
            result[REVENUE_FEATURES]
        )
    )

    result["Profitability Probability"] = (
        profit_model.predict_proba(
            result[PROFIT_FEATURES]
        )[:, 1] * 100
    )

    result["ML Score"] = (

        result["Predicted Valuation"] * 0.30

        +

        result["Predicted Revenue"] * 0.30

        +

        result["Profitability Probability"] * 5

    )

    return result.sort_values(
        "ML Score",
        ascending=False
    )

# ==========================================================
# WHAT IF ANALYSIS
# ==========================================================

def what_if_analysis(
    valuation_model,
    funding,
    rounds,
    employees,
    revenue,
    market_share,
    funding_growth_percent
):

    new_funding = funding * (
        1 +
        funding_growth_percent / 100
    )

    prediction = valuation_model.predict(
        [[
            new_funding,
            rounds,
            employees,
            revenue,
            market_share
        ]]
    )

    return float(prediction[0])

# ==========================================================
# BULK FORECAST
# ==========================================================

def generate_forecasts(
    df,
    valuation_model,
    revenue_model
):

    result = df.copy()

    result["Forecasted Valuation"] = (
        valuation_model.predict(
            result[VALUATION_FEATURES]
        )
    )

    result["Forecasted Revenue"] = (
        revenue_model.predict(
            result[REVENUE_FEATURES]
        )
    )

    return result

# ==========================================================
# SAVE MODEL
# ==========================================================

def save_model(
    model,
    filepath
):

    joblib.dump(
        model,
        filepath
    )

# ==========================================================
# LOAD MODEL
# ==========================================================

def load_model(
    filepath
):

    return joblib.load(
        filepath
    )

# ==========================================================
# TRAIN ALL MODELS
# ==========================================================

def train_all_models(df):

    valuation_model, valuation_metrics = (
        train_valuation_model(df)
    )

    revenue_model, revenue_metrics = (
        train_revenue_model(df)
    )

    profitability_model, profitability_metrics = (
        train_profitability_model(df)
    )

    return {

        "valuation_model":
            valuation_model,

        "revenue_model":
            revenue_model,

        "profitability_model":
            profitability_model,

        "valuation_metrics":
            valuation_metrics,

        "revenue_metrics":
            revenue_metrics,

        "profitability_metrics":
            profitability_metrics
    }

# ==========================================================
# EXECUTIVE MODEL SUMMARY
# ==========================================================

def model_summary(models):

    summary = pd.DataFrame({

        "Model": [

            "Valuation",
            "Revenue",
            "Profitability"

        ],

        "Primary Metric": [

            models["valuation_metrics"]["R2"],
            models["revenue_metrics"]["R2"],
            models["profitability_metrics"]["Accuracy"]

        ]

    })

    return summary
