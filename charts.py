"""
=========================================================
CHART UTILITIES
Startup Intelligence Platform
Reusable Plotly Visualizations
=========================================================
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# THEME
# ==========================================================

PLOTLY_TEMPLATE = "plotly_white"

COLOR_SEQUENCE = px.colors.qualitative.Set2

# ==========================================================
# KPI BAR CHART
# ==========================================================

def bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    color=None
):

    fig = px.bar(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        template=PLOTLY_TEMPLATE,
        color_discrete_sequence=COLOR_SEQUENCE
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# PIE CHART
# ==========================================================

def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str
):

    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.4
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# TREEMAP
# ==========================================================

def treemap_chart(
    df: pd.DataFrame,
    path,
    values,
    color,
    title
):

    fig = px.treemap(
        df,
        path=path,
        values=values,
        color=color,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=600
    )

    return fig

# ==========================================================
# SCATTER CHART
# ==========================================================

def scatter_chart(
    df,
    x,
    y,
    size,
    color,
    title,
    hover_name=None
):

    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size,
        color=color,
        hover_name=hover_name,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=600
    )

    return fig

# ==========================================================
# HISTOGRAM
# ==========================================================

def histogram_chart(
    df,
    column,
    title,
    bins=30
):

    fig = px.histogram(
        df,
        x=column,
        nbins=bins,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# BOX PLOT
# ==========================================================

def box_chart(
    df,
    x,
    y,
    color,
    title
):

    fig = px.box(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# LINE CHART
# ==========================================================

def line_chart(
    df,
    x,
    y,
    title,
    color=None
):

    fig = px.line(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# AREA CHART
# ==========================================================

def area_chart(
    df,
    x,
    y,
    color,
    title
):

    fig = px.area(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# SUNBURST
# ==========================================================

def sunburst_chart(
    df,
    path,
    values,
    title
):

    fig = px.sunburst(
        df,
        path=path,
        values=values,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=650
    )

    return fig

# ==========================================================
# CORRELATION HEATMAP
# ==========================================================

def correlation_heatmap(
    corr_matrix,
    title="Correlation Matrix"
):

    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Blues",
        title=title
    )

    fig.update_layout(
        height=650
    )

    return fig

# ==========================================================
# RADAR CHART
# ==========================================================

def radar_chart(
    df,
    category_col,
    metrics,
    title
):

    fig = go.Figure()

    for _, row in df.iterrows():

        fig.add_trace(
            go.Scatterpolar(
                r=[row[m] for m in metrics],
                theta=metrics,
                fill="toself",
                name=row[category_col]
            )
        )

    fig.update_layout(
        title=title,
        polar=dict(
            radialaxis=dict(
                visible=True
            )
        ),
        showlegend=True,
        height=700
    )

    return fig

# ==========================================================
# GAUGE CHART
# ==========================================================

def gauge_chart(
    value,
    title
):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title},
            gauge={
                "axis": {
                    "range": [0, 100]
                }
            }
        )
    )

    fig.update_layout(
        height=400
    )

    return fig

# ==========================================================
# FUNNEL CHART
# ==========================================================

def funnel_chart(
    labels,
    values,
    title
):

    fig = go.Figure(
        go.Funnel(
            y=labels,
            x=values
        )
    )

    fig.update_layout(
        title=title,
        height=500
    )

    return fig

# ==========================================================
# WATERFALL CHART
# ==========================================================

def waterfall_chart(
    labels,
    values,
    title
):

    fig = go.Figure(
        go.Waterfall(
            x=labels,
            y=values
        )
    )

    fig.update_layout(
        title=title,
        height=500
    )

    return fig

# ==========================================================
# LEADERBOARD BAR
# ==========================================================

def leaderboard_chart(
    df,
    category,
    value,
    title
):

    top_df = df.sort_values(
        value,
        ascending=False
    )

    fig = px.bar(
        top_df,
        x=category,
        y=value,
        color=value,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=600
    )

    return fig

# ==========================================================
# EXECUTIVE SCORECARD
# ==========================================================

def scorecard_chart(
    df,
    category,
    score,
    title
):

    fig = px.bar(
        df.sort_values(
            score,
            ascending=False
        ),
        x=category,
        y=score,
        color=score,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=600
    )

    return fig

# ==========================================================
# TOP-N CHART
# ==========================================================

def top_n_chart(
    df,
    category,
    value,
    n=10,
    title="Top Records"
):

    temp = (
        df.sort_values(
            value,
            ascending=False
        )
        .head(n)
    )

    fig = px.bar(
        temp,
        x=category,
        y=value,
        color=value,
        title=title,
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        height=500
    )

    return fig

# ==========================================================
# EXPORT STYLE
# ==========================================================

def apply_enterprise_theme(fig):

    fig.update_layout(

        template=PLOTLY_TEMPLATE,

        title_font_size=22,

        font=dict(
            family="Inter"
        ),

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        paper_bgcolor="white",

        plot_bgcolor="white"
    )

    return fig
