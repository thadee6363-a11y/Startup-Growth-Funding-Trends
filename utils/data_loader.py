"""
==========================================================
DATA LOADER MODULE
Startup Intelligence Platform
==========================================================
"""

import pandas as pd
import numpy as np
import streamlit as st

# ==========================================================
# EXPECTED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [
    "Startup Name",
    "Industry",
    "Region",
    "Funding Amount (M USD)",
    "Funding Rounds",
    "Revenue (M USD)",
    "Valuation (M USD)",
    "Employees",
    "Market Share (%)",
    "Profitable",
    "Exit Status"
]

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_data(
    filepath: str = "data/startup_data.csv"
) -> pd.DataFrame:
    """
    Load startup dataset

    Parameters
    ----------
    filepath : str

    Returns
    -------
    DataFrame
    """

    try:

        df = pd.read_csv(filepath)

        validate_columns(df)

        df = clean_data(df)

        df = create_features(df)

        return df

    except FileNotFoundError:

        raise FileNotFoundError(
            f"Dataset not found: {filepath}"
        )

    except Exception as e:

        raise Exception(
            f"Data loading error: {e}"
        )

# ==========================================================
# VALIDATE DATA
# ==========================================================

def validate_columns(
    df: pd.DataFrame
) -> None:
    """
    Validate schema
    """

    missing_columns = [
        col
        for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            f"""
            Missing Columns:
            {missing_columns}
            """
        )

# ==========================================================
# CLEAN DATA
# ==========================================================

def clean_data(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Basic cleaning
    """

    df = df.copy()

    # ------------------------------------------------------
    # Remove duplicates
    # ------------------------------------------------------

    df.drop_duplicates(
        inplace=True
    )

    # ------------------------------------------------------
    # Startup Name
    # ------------------------------------------------------

    df["Startup Name"] = (
        df["Startup Name"]
        .astype(str)
        .str.strip()
    )

    # ------------------------------------------------------
    # Fill numeric columns
    # ------------------------------------------------------

    numeric_cols = [

        "Funding Amount (M USD)",
        "Funding Rounds",
        "Revenue (M USD)",
        "Valuation (M USD)",
        "Employees",
        "Market Share (%)"

    ]

    for col in numeric_cols:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

            df[col].fillna(
                df[col].median(),
                inplace=True
            )

    # ------------------------------------------------------
    # Fill categorical columns
    # ------------------------------------------------------

    categorical_cols = [

        "Industry",
        "Region",
        "Exit Status"

    ]

    for col in categorical_cols:

        if col in df.columns:

            df[col].fillna(
                "Unknown",
                inplace=True
            )

    # ------------------------------------------------------
    # Boolean cleanup
    # ------------------------------------------------------

    if "Profitable" in df.columns:

        if df["Profitable"].dtype != bool:

            df["Profitable"] = (
                df["Profitable"]
                .astype(str)
                .str.lower()
                .map({
                    "true": True,
                    "false": False,
                    "1": True,
                    "0": False,
                    "yes": True,
                    "no": False
                })
            )

            df["Profitable"].fillna(
                False,
                inplace=True
            )

    return df

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def create_features(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Create analytics features
    """

    df = df.copy()

    # ------------------------------------------------------
    # Revenue Efficiency
    # ------------------------------------------------------

    df["Revenue Efficiency"] = np.where(
        df["Funding Amount (M USD)"] > 0,
        df["Revenue (M USD)"]
        /
        df["Funding Amount (M USD)"],
        0
    )

    # ------------------------------------------------------
    # Valuation Multiple
    # ------------------------------------------------------

    df["Valuation Multiple"] = np.where(
        df["Revenue (M USD)"] > 0,
        df["Valuation (M USD)"]
        /
        df["Revenue (M USD)"],
        0
    )

    # ------------------------------------------------------
    # Funding Efficiency
    # ------------------------------------------------------

    df["Funding Efficiency"] = np.where(
        df["Funding Amount (M USD)"] > 0,
        df["Valuation (M USD)"]
        /
        df["Funding Amount (M USD)"],
        0
    )

    # ------------------------------------------------------
    # Revenue Per Employee
    # ------------------------------------------------------

    df["Revenue Per Employee"] = np.where(
        df["Employees"] > 0,
        df["Revenue (M USD)"]
        /
        df["Employees"],
        0
    )

    # ------------------------------------------------------
    # Valuation Per Employee
    # ------------------------------------------------------

    df["Valuation Per Employee"] = np.where(
        df["Employees"] > 0,
        df["Valuation (M USD)"]
        /
        df["Employees"],
        0
    )

    # ------------------------------------------------------
    # Startup Score
    # ------------------------------------------------------

    df["Startup Score"] = (

        df["Revenue (M USD)"] * 0.30

        +

        df["Valuation (M USD)"] * 0.25

        +

        df["Market Share (%)"] * 20

        +

        df["Profitable"].astype(int) * 500

    )

    # ------------------------------------------------------
    # Unicorn Flag
    # ------------------------------------------------------

    df["Unicorn"] = np.where(
        df["Valuation (M USD)"] >= 1000,
        "Yes",
        "No"
    )

    return df

# ==========================================================
# FILTER DATA
# ==========================================================

def filter_data(
    df: pd.DataFrame,
    industries=None,
    regions=None,
    exit_status=None
) -> pd.DataFrame:
    """
    Universal filtering utility
    """

    filtered = df.copy()

    if industries:

        filtered = filtered[
            filtered["Industry"].isin(
                industries
            )
        ]

    if regions:

        filtered = filtered[
            filtered["Region"].isin(
                regions
            )
        ]

    if exit_status:

        filtered = filtered[
            filtered["Exit Status"].isin(
                exit_status
            )
        ]

    return filtered

# ==========================================================
# KPI SUMMARY
# ==========================================================

def get_kpis(
    df: pd.DataFrame
) -> dict:
    """
    Return executive KPIs
    """

    return {

        "startups":
            len(df),

        "funding":
            round(
                df[
                    "Funding Amount (M USD)"
                ].sum(),
                2
            ),

        "revenue":
            round(
                df[
                    "Revenue (M USD)"
                ].sum(),
                2
            ),

        "valuation":
            round(
                df[
                    "Valuation (M USD)"
                ].sum(),
                2
            ),

        "profitability":
            round(
                df[
                    "Profitable"
                ].mean() * 100,
                2
            ),

        "unicorns":
            len(
                df[
                    df["Unicorn"] == "Yes"
                ]
            )
    }

# ==========================================================
# INDUSTRY SUMMARY
# ==========================================================

def industry_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Industry aggregation
    """

    return (

        df.groupby("Industry")

        .agg({

            "Funding Amount (M USD)":
                "sum",

            "Revenue (M USD)":
                "sum",

            "Valuation (M USD)":
                "mean",

            "Profitable":
                "mean"

        })

        .reset_index()

    )

# ==========================================================
# REGION SUMMARY
# ==========================================================

def region_summary(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Regional aggregation
    """

    return (

        df.groupby("Region")

        .agg({

            "Funding Amount (M USD)":
                "sum",

            "Revenue (M USD)":
                "sum",

            "Valuation (M USD)":
                "mean",

            "Profitable":
                "mean"

        })

        .reset_index()

    )

# ==========================================================
# TOP STARTUPS
# ==========================================================

def top_startups(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Return highest ranked startups
    """

    return (

        df.sort_values(
            "Startup Score",
            ascending=False
        )

        .head(top_n)

    )

# ==========================================================
# EXPORT CSV
# ==========================================================

def dataframe_to_csv(
    df: pd.DataFrame
) -> bytes:
    """
    Convert dataframe to CSV
    """

    return df.to_csv(
        index=False
    ).encode("utf-8")
