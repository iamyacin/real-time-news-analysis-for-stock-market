"""Streamlit dashboard for the restored PFE project.

Run with:
    streamlit run dashboard/app.py
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import config  # noqa: E402

st.set_page_config(page_title="Stock News Analyzer", page_icon="📈", layout="wide")

SENTIMENTS = ["Positive", "Neutral", "Negative"]
COLORS = {"Positive": "#2eb85c", "Neutral": "#8a93a2", "Negative": "#e55353"}


@st.cache_resource
def get_collection():
    client = MongoClient(config.MONGO_URI, serverSelectionTimeoutMS=3000)
    return client[config.MONGO_DB][config.MONGO_COLLECTION]


def _source_name(value) -> str:
    if isinstance(value, dict):
        return value.get("name") or value.get("id") or "Unknown"
    return str(value or "Unknown")


def _sentiment(row) -> str:
    value = row.get("prediction") if isinstance(row, dict) else row.get("prediction")
    if isinstance(value, (int, float)):
        return {-1: "Negative", 0: "Neutral", 1: "Positive"}.get(int(value), "Neutral")
    value = str(value or row.get("polarity") or "Neutral")
    return value if value in SENTIMENTS else "Neutral"


def _parse_date(value):
    if isinstance(value, datetime):
        return value
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


@st.cache_data(ttl=15)
def load_news() -> pd.DataFrame:
    docs = list(get_collection().find({}).sort("publishedAt", -1))
    if not docs:
        return pd.DataFrame()
    rows = []
    for doc in docs:
        published = _parse_date(doc.get("publishedAt")) or _parse_date(doc.get("collected_at"))
        rows.append(
            {
                "id": str(doc.get("_id")),
                "title": doc.get("title") or (doc.get("text") or "")[:120],
                "text": doc.get("text") or doc.get("description") or "",
                "source": _source_name(doc.get("source")),
                "ticker": doc.get("ticker") or ((doc.get("tickers") or [None])[0]),
                "sentiment": _sentiment(doc),
                "published_at": published,
                "date": published.date() if published else None,
                "url": doc.get("url"),
                "is_business": doc.get("is_business"),
                "source_type": doc.get("source_type", "newsapi"),
            }
        )
    frame = pd.DataFrame(rows)
    frame["ticker"] = frame["ticker"].fillna("—").astype(str)
    return frame


def _news_table(frame: pd.DataFrame, max_rows: int = 50) -> None:
    if frame.empty:
        st.info("No news found. Run `make seed` to load the demo fixtures.")
        return
    display = frame.head(max_rows).copy()
    display["published_at"] = display["published_at"].apply(
        lambda value: value.strftime("%Y-%m-%d %H:%M") if value else ""
    )
    columns = ["published_at", "ticker", "sentiment", "source", "title"]
    st.dataframe(
        display[columns],
        use_container_width=True,
        hide_index=True,
        column_config={
            "published_at": st.column_config.TextColumn("Published"),
            "ticker": st.column_config.TextColumn("Ticker"),
            "sentiment": st.column_config.TextColumn("Sentiment"),
            "source": st.column_config.TextColumn("Source"),
            "title": st.column_config.TextColumn("Headline", width="large"),
        },
    )
    links = [f"- [{row.title}]({row.url})" for row in display.head(10).itertuples() if row.url]
    if links:
        with st.expander("Open headlines"):
            st.markdown("\n".join(links))


def overview(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.info("No data yet. Start the stack with `docker compose up` or run `make seed`.")
        return

    counts = frame["sentiment"].value_counts().reindex(SENTIMENTS, fill_value=0)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Articles", len(frame))
    col2.metric("Positive", int(counts["Positive"]))
    col3.metric("Neutral", int(counts["Neutral"]))
    col4.metric("Negative", int(counts["Negative"]))

    left, right = st.columns(2)
    with left:
        chart = px.bar(
            x=SENTIMENTS,
            y=[int(counts[s]) for s in SENTIMENTS],
            color=SENTIMENTS,
            color_discrete_map=COLORS,
            labels={"x": "Sentiment", "y": "Articles"},
            title="Sentiment distribution",
        )
        chart.update_layout(showlegend=False, height=340, margin=dict(t=50, b=10))
        st.plotly_chart(chart, use_container_width=True)
    with right:
        top = frame["ticker"].value_counts().head(12).sort_values()
        chart = px.bar(
            x=top.values,
            y=top.index,
            orientation="h",
            title="Most covered tickers",
            labels={"x": "Articles", "y": "Ticker"},
        )
        chart.update_layout(height=340, margin=dict(t=50, b=10))
        st.plotly_chart(chart, use_container_width=True)

    st.subheader("Latest headlines")
    _news_table(frame)


def ticker_explorer(frame: pd.DataFrame) -> None:
    if frame.empty:
        st.info("No data yet.")
        return
    tickers = sorted(frame["ticker"].unique())
    selected = st.selectbox("Ticker", tickers, index=0)
    subset = frame[frame["ticker"] == selected].copy()
    sentiment = st.multiselect("Sentiment", SENTIMENTS, default=SENTIMENTS)
    subset = subset[subset["sentiment"].isin(sentiment)]
    if subset.empty:
        st.warning("No records for this filter.")
        return

    counts = subset["sentiment"].value_counts().reindex(SENTIMENTS, fill_value=0)
    cols = st.columns(3)
    for col, label in zip(cols, SENTIMENTS):
        col.metric(label, int(counts[label]))

    daily = (
        subset.dropna(subset=["date"])
        .groupby(["date", "sentiment"])
        .size()
        .reset_index(name="count")
    )
    if not daily.empty:
        chart = px.line(
            daily,
            x="date",
            y="count",
            color="sentiment",
            markers=True,
            color_discrete_map=COLORS,
            title=f"Sentiment over time — {selected}",
        )
        chart.update_layout(height=360)
        st.plotly_chart(chart, use_container_width=True)

    st.subheader(f"Headlines for {selected}")
    _news_table(subset, max_rows=100)


def analyzer() -> None:
    st.write(
        "Paste a headline or article excerpt. The service returns the business-news "
        "prediction and the polarity score."
    )
    text = st.text_area(
        "Text",
        height=140,
        placeholder="Apple beats earnings expectations as services revenue hits a record...",
    )
    if st.button("Analyze", type="primary"):
        if not text.strip():
            st.warning("Enter some text first.")
            return
        try:
            response = requests.post(
                f"{config.SERVICE_URL.rstrip('/')}/analyze",
                json={"text": text},
                timeout=120,
            )
            response.raise_for_status()
            result = response.json()
            col1, col2, col3 = st.columns(3)
            col1.metric("Business news", "Yes" if result["is_business"] else "No")
            col2.metric("Polarity", result["polarity_label"])
            col3.metric("Backend", result["backend"])
            st.json(result)
        except Exception as exc:  # noqa: BLE001
            st.error(f"Prediction service unavailable: {exc}")


def main() -> None:
    st.title("📈 Stock News Analyzer")
    st.caption("PFE 2020 restoration — financial news classification and sentiment analysis")

    try:
        frame = load_news()
        collection = get_collection()
        mongo_ok = True
    except Exception as exc:  # noqa: BLE001
        st.error(f"MongoDB unavailable at `{config.MONGO_URI}`: {exc}")
        st.code("docker compose up -d mongo\nmake seed")
        return

    with st.sidebar:
        st.header("Filters")
        st.caption(f"MongoDB: `{config.MONGO_DB}.{config.MONGO_COLLECTION}`")
        if not frame.empty:
            tickers = st.multiselect("Tickers", sorted(frame["ticker"].unique()))
            sentiments = st.multiselect("Sentiment", SENTIMENTS, default=SENTIMENTS)
            dates = frame["date"].dropna()
            if not dates.empty:
                selected_dates = st.date_input(
                    "Date range",
                    value=(dates.min(), dates.max()),
                    min_value=dates.min(),
                    max_value=dates.max(),
                )
                if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
                    start, end = selected_dates
                else:
                    start = end = None
            else:
                start = end = None
            filtered = frame.copy()
            if tickers:
                filtered = filtered[filtered["ticker"].isin(tickers)]
            filtered = filtered[filtered["sentiment"].isin(sentiments)]
            if start and end:
                filtered = filtered[
                    filtered["date"].isna()
                    | ((filtered["date"] >= start) & (filtered["date"] <= end))
                ]
        else:
            filtered = frame
        if st.button("Refresh data"):
            load_news.clear()
            st.rerun()
        st.divider()
        st.caption(f"Prediction service: `{config.SERVICE_URL}`")

    tab_overview, tab_ticker, tab_analyze, tab_data = st.tabs(
        ["Overview", "Ticker explorer", "Analyze text", "Data"]
    )
    with tab_overview:
        overview(filtered)
    with tab_ticker:
        ticker_explorer(filtered)
    with tab_analyze:
        analyzer()
    with tab_data:
        st.subheader("Raw records")
        st.dataframe(filtered, use_container_width=True, hide_index=True)
        if not filtered.empty:
            csv = filtered.drop(columns=["id"]).to_csv(index=False).encode("utf-8")
            st.download_button("Download CSV", csv, "stock_news.csv", "text/csv")


if __name__ == "__main__":
    main()
