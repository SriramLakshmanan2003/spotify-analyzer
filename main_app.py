import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_utils import connect_db, create_table, insert_track,truncate_table
from spotify_utils import extract_track_data
from data_operations import get_min_max_avg, detect_duplicates, detect_outliers
import numpy as np

st.title("🎵 Spotify Track Analyzer")

urls = st.text_area("Enter 2-10 Spotify track URLs (one per line):")
submit = st.button("Analyze Tracks")

if submit:
    url_list = [u.strip() for u in urls.strip().splitlines() if u.strip()]
    if len(url_list) < 2 or len(url_list) > 10:
        st.warning("Please enter between 2 and 10 Spotify track URLs.")
    else:
        conn = connect_db()
        create_table(conn)

        df_input = pd.DataFrame()

        for url in url_list:
            try:
                data = extract_track_data(url)
                insert_track(conn, data)
                df_input = pd.concat([df_input, pd.DataFrame([data])], ignore_index=True)
            except Exception as e:
                st.error(f"Error processing {url}: {e}")

        if not df_input.empty:
            conn= connect_db()
            st.subheader("🎧 Track Data (Current Session)")
            st.dataframe(df_input)
           

            st.subheader("🎨 Track Duration vs Popularity")

            labels = df_input['track_name']
            duration = df_input['duration_min']
            popularity = df_input['popularity']

            x = np.arange(len(labels))  # Label locations
            width = 0.35  # Width of the bars

            fig, ax = plt.subplots(figsize=(10, 5))
            bars1 = ax.bar(x - width/2, duration, width, label='Duration (min)', color='blue')
            bars2 = ax.bar(x + width/2, popularity, width, label='Popularity', color='deeppink')

            ax.set_ylabel('Values')
            ax.set_title('Track Duration and Popularity')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.legend()

            fig.tight_layout()
            st.pyplot(fig)

            st.subheader("📊 Track Duration and Popularity Statistics")
            stats = get_min_max_avg(df_input)
            st.metric("Minimum Duration (min)", f"{stats['min_duration']:.2f}")
            st.metric("Maximum Duration (min)", f"{stats['max_duration']:.2f}")
            st.metric("Average Duration (min)", f"{stats['avg_duration']:.2f}")

            dupes = detect_duplicates(df_input)
            if not dupes.empty:
                st.subheader("🚨 Duplicate Songs Detected")
                st.dataframe(dupes)

            outliers = detect_outliers(df_input)
            if not outliers.empty:
                st.subheader("⚠️ Outlier Songs by Duration")
                st.dataframe(outliers)
            truncate_table(conn)
