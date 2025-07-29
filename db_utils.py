import mysql.connector
import pandas as pd
import streamlit as st


def connect_db():
    return mysql.connector.connect(
        host=st.secrets["DB_HOST"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        database=st.secrets["DB_PORT"]

    )

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            track_id VARCHAR(50) PRIMARY KEY,
            track_name VARCHAR(255),
            artist_name VARCHAR(255),
            album_name VARCHAR(255),
            release_date DATE,
            duration_min FLOAT,
            popularity INT,
            spotify_url TEXT
        )
    ''')
    conn.commit()

def insert_track(conn, track):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT IGNORE INTO tracks (track_id, track_name, artist_name, album_name, release_date, duration_min, popularity, spotify_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
          track['track_id'], track['track_name'], track['artist_name'],
          track['album_name'], track['release_date'], track['duration_min'],
          track['popularity'], track['spotify_url']
      ))
    conn.commit()

def fetch_all_tracks(conn):
    return pd.read_sql("SELECT DISTINCT * FROM tracks", conn)

def truncate_table(conn):
    cursor=conn.cursor()
    cursor.execute("TRUNCATE TABLE tracks")
    conn.commit()
    cursor.close()