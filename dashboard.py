import streamlit as st
import redis
import time
import pandas as pd

# Redis connection
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

st.set_page_config(page_title="Streaming Analytics Dashboard", layout="wide")

st.title("📊 Real-time Content Engagement Dashboard")

refresh = st.slider("Refresh interval (seconds)", 2, 10, 5)

placeholder = st.empty()

while True:
    data = []

    for key in r.scan_iter("metrics:*"):
        content_id = key.split(":")[1]
        metrics = r.hgetall(key)

        row = {"content_id": content_id}
        row.update(metrics)
        data.append(row)

    if data:
        df = pd.DataFrame(data).fillna(0)

        for col in df.columns:
            if col != "content_id":
                df[col] = df[col].astype(int)

        with placeholder.container():
            st.subheader("📌 Aggregated Metrics")
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Engagement per Content")
            st.bar_chart(df.set_index("content_id"))

    else:
        st.warning("No metrics available yet...")

    time.sleep(refresh)