import streamlit as st
import pandas as pd
from pathlib import Path

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Startup Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    possible_paths = [

        Path("startup_data.csv"),

        Path("data/startup_data.csv"),

        Path("dataset/startup_data.csv"),

        Path("Data/startup_data.csv")

    ]

    for path in possible_paths:

        if path.exists():

            st.success(f"Loaded data from: {path}")

            return pd.read_csv(path)

    raise FileNotFoundError(
        """
        startup_data.csv not found.

        Checked:
        - startup_data.csv
        - data/startup_data.csv
        - dataset/startup_data.csv
        - Data/startup_data.csv
        """
    )

# ==========================================================
# LOAD DATASET
# ==========================================================

try:

    df = load_data()

except Exception as e:

    st.error(f"Error Loading Dataset: {e}")

    st.stop()

# ==========================================================
# DASHBOARD
# ==========================================================

st.title("🚀 Startup Intelligence Platform")

st.write("Dataset Preview")

st.dataframe(
    df.head(),
    use_container_width=True
)

# ==========================================================
# KPIs
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Startups",
    len(df)
)

if "Funding Amount (M USD)" in df.columns:

    c2.metric(
        "Funding",
        f"${df['Funding Amount (M USD)'].sum():,.0f}M"
    )

if "Revenue (M USD)" in df.columns:

    c3.metric(
        "Revenue",
        f"${df['Revenue (M USD)'].sum():,.0f}M"
    )

if "Valuation (M USD)" in df.columns:

    c4.metric(
        "Valuation",
        f"${df['Valuation (M USD)'].sum():,.0f}M"
    )

st.divider()

st.subheader("Columns Found")

st.write(df.columns.tolist())
