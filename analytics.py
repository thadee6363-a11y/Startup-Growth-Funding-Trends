"""
=========================================================
ANALYTICS ENGINE
Startup Intelligence Platform
Business Logic + KPI Calculations
=========================================================
"""

import pandas as pd
import numpy as np

# ==========================================================
# EXECUTIVE KPIs
# ==========================================================

def calculate_kpis(df: pd.DataFrame) -> dict:

    return {

        "total_startups":
            len(df),

        "total_funding":
            df["Funding Amount (M USD)"].sum(),

        "total_revenue":
            df["Revenue (M USD)"].sum(),

        "total_valuation":
            df["Valuation (M USD)"].sum(),

        "average_valuation":
            df["Valuation (M USD)"].mean(),

        "average_revenue":
            df["Revenue (M USD)"].mean(),

        "profitability_rate":
            df["Profitable"].mean() * 100,

        "unicorns":
            len(
                df[
                    df["Valuation (M USD)"] >= 1000
                ]
            )
    }

# ==========================================================
# STARTUP SCORING
# ==========================================================

def calculate_startup_score(
    df: pd.DataFrame
) -> pd.DataFrame:

    result = df.copy()

    result["Startup Score"] = (

        result["Revenue (M USD)"] * 0.30

        +

        result["Valuation (M USD)"] * 0.25

        +

        result["Market Share (%)"] * 25

        +

        result["Profitable"].astype(int) * 500

    )

    return result

# ==========================================================
# SUCCESS SCORE
# ==========================================================

def calculate_success_score(
    df: pd.DataFrame
) -> pd.DataFrame:

    result = df.copy()

    result["Success Score"] = (

        result["Revenue Efficiency"] * 100

        +

        result["Valuation Multiple"] * 50

        +

        result["Market Share (%)"] * 10

        +

        result["Profitable"].astype(int) * 500

    )

    return result

# ==========================================================
# INDUSTRY ANALYTICS
# ==========================================================

def industry_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    industry = (

        df.groupby("Industry")

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

    industry["Profitability Rate"] = (
        industry["Profitable"] * 100
    )

    industry["Industry Score"] = (

        industry["Revenue (M USD)"] * 0.35

        +

        industry["Valuation (M USD)"] * 0.25

        +

        industry["Market Share (%)"] * 50

        +

        industry["Profitability Rate"] * 5

    )

    return industry

# ==========================================================
# REGIONAL ANALYTICS
# ==========================================================

def regional_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    regional = (

        df.groupby("Region")

        .agg({

            "Funding Amount (M USD)": "sum",

            "Revenue (M USD)": "sum",

            "Valuation (M USD)": "mean",

            "Employees": "sum",

            "Profitable": "mean",

            "Startup Name": "count"

        })

        .reset_index()

    )

    regional.rename(
        columns={
            "Startup Name":
            "Startup Count"
        },
        inplace=True
    )

    regional["Profitability Rate"] = (
        regional["Profitable"] * 100
    )

    regional["Regional Score"] = (

        regional["Revenue (M USD)"] * 0.30

        +

        regional["Valuation (M USD)"] * 0.25

        +

        regional["Profitability Rate"] * 5

    )

    return regional

# ==========================================================
# PROFITABILITY ANALYSIS
# ==========================================================

def profitability_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    profitability = (

        df.groupby("Industry")

        .agg({

            "Profitable": "mean",

            "Revenue (M USD)": "mean",

            "Valuation (M USD)": "mean"

        })

        .reset_index()

    )

    profitability["Profitability Rate"] = (
        profitability["Profitable"] * 100
    )

    return profitability

# ==========================================================
# FUNDING ANALYSIS
# ==========================================================

def funding_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    return (

        df.groupby("Industry")

        ["Funding Amount (M USD)"]

        .sum()

        .reset_index()

        .sort_values(
            "Funding Amount (M USD)",
            ascending=False
        )

    )

# ==========================================================
# VALUATION ANALYSIS
# ==========================================================

def valuation_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    valuation = (

        df.groupby("Industry")

        .agg({

            "Valuation (M USD)": "mean",

            "Revenue (M USD)": "mean"

        })

        .reset_index()

    )

    valuation["Valuation Multiple"] = (

        valuation["Valuation (M USD)"]

        /

        valuation["Revenue (M USD)"]

    )

    return valuation

# ==========================================================
# CAPITAL EFFICIENCY
# ==========================================================

def capital_efficiency(
    df: pd.DataFrame
) -> pd.DataFrame:

    result = df.copy()

    result["Capital Efficiency"] = np.where(

        result["Funding Amount (M USD)"] > 0,

        result["Revenue (M USD)"]

        /

        result["Funding Amount (M USD)"],

        0

    )

    return result

# ==========================================================
# UNICORN ANALYSIS
# ==========================================================

def unicorn_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    return df[
        df["Valuation (M USD)"] >= 1000
    ]

# ==========================================================
# TOP STARTUPS
# ==========================================================

def top_startups(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:

    ranked = calculate_startup_score(df)

    return (

        ranked

        .sort_values(
            "Startup Score",
            ascending=False
        )

        .head(top_n)

    )

# ==========================================================
# OVERVALUED STARTUPS
# ==========================================================

def overvalued_startups(
    df: pd.DataFrame
) -> pd.DataFrame:

    threshold = (
        df["Valuation Multiple"]
        .quantile(0.90)
    )

    return df[
        df["Valuation Multiple"]
        >= threshold
    ]

# ==========================================================
# UNDERVALUED STARTUPS
# ==========================================================

def undervalued_startups(
    df: pd.DataFrame
) -> pd.DataFrame:

    threshold = (
        df["Valuation Multiple"]
        .quantile(0.10)
    )

    return df[
        df["Valuation Multiple"]
        <= threshold
    ]

# ==========================================================
# INVESTMENT OPPORTUNITIES
# ==========================================================

def investment_opportunities(
    df: pd.DataFrame
) -> pd.DataFrame:

    return df[

        (
            df["Revenue Efficiency"]
            >
            df["Revenue Efficiency"].median()
        )

        &

        (
            df["Profitable"]
            == True
        )

    ]

# ==========================================================
# RISK DETECTION
# ==========================================================

def risk_detection(
    df: pd.DataFrame
) -> pd.DataFrame:

    high_multiple = (
        df["Valuation Multiple"]
        .quantile(0.95)
    )

    return df[
        df["Valuation Multiple"]
        >= high_multiple
    ]

# ==========================================================
# EXIT ANALYSIS
# ==========================================================

def exit_analysis(
    df: pd.DataFrame
) -> pd.DataFrame:

    return (

        df.groupby(
            "Exit Status"
        )

        .size()

        .reset_index(
            name="Count"
        )

    )

# ==========================================================
# CORRELATION MATRIX
# ==========================================================

def correlation_matrix(
    df: pd.DataFrame
) -> pd.DataFrame:

    numeric_df = (
        df.select_dtypes(
            include=np.number
        )
    )

    return numeric_df.corr()

# ==========================================================
# AI INSIGHTS GENERATOR
# ==========================================================

def generate_ai_insights(
    df: pd.DataFrame
) -> dict:

    insights = {}

    top_industry = (

        df.groupby("Industry")

        ["Revenue (M USD)"]

        .sum()

        .idxmax()

    )

    top_region = (

        df.groupby("Region")

        ["Revenue (M USD)"]

        .sum()

        .idxmax()

    )

    top_startup = (

        calculate_startup_score(df)

        .sort_values(
            "Startup Score",
            ascending=False
        )

        .iloc[0]["Startup Name"]

    )

    profitability = (
        df["Profitable"]
        .mean()
        * 100
    )

    insights["top_industry"] = top_industry

    insights["top_region"] = top_region

    insights["top_startup"] = top_startup

    insights["profitability_rate"] = profitability

    insights["unicorn_count"] = len(
        unicorn_analysis(df)
    )

    return insights

# ==========================================================
# EXECUTIVE REPORT
# ==========================================================

def executive_report(
    df: pd.DataFrame
) -> pd.DataFrame:

    kpis = calculate_kpis(df)

    report = pd.DataFrame({

        "Metric": [

            "Total Startups",
            "Total Funding",
            "Total Revenue",
            "Total Valuation",
            "Profitability Rate",
            "Unicorn Count"

        ],

        "Value": [

            kpis["total_startups"],
            kpis["total_funding"],
            kpis["total_revenue"],
            kpis["total_valuation"],
            kpis["profitability_rate"],
            kpis["unicorns"]

        ]

    })

    return report

# ==========================================================
# BENCHMARK SCORECARD
# ==========================================================

def benchmark_scorecard(
    df: pd.DataFrame
) -> pd.DataFrame:

    scorecard = (

        df.groupby("Industry")

        .agg({

            "Revenue (M USD)": "mean",

            "Valuation (M USD)": "mean",

            "Revenue Efficiency": "mean",

            "Profitable": "mean"

        })

        .reset_index()

    )

    scorecard["Profitability Rate"] = (
        scorecard["Profitable"] * 100
    )

    return scorecard

# ==========================================================
# EXPORT CSV
# ==========================================================

def export_csv(
    df: pd.DataFrame
) -> bytes:

    return df.to_csv(
        index=False
    ).encode("utf-8")
