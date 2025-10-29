import psycopg2
import pandas as pd
import os
import json
import streamlit as st
from datetime import datetime

# --- Database connection setup ---

def get_connection():
    """Create and return a PostgreSQL connection using environment variables."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        sslmode="require"
    )
    return conn

# --- Database functions ---
def create_orders_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT NOW(),
            items TEXT,
            total NUMERIC,
            paid NUMERIC,
            change NUMERIC,
            payment_method TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_order(items, total, paid, change, payment_method):
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO orders (timestamp, items, total, paid, change, payment_method)
        VALUES (%s, %s, %s, %s, %s, %s);
    """, (timestamp, ", ".join(items), total, paid, change, payment_method))
    conn.commit()
    cur.close()
    conn.close()


def get_recent_orders(limit=10):
    conn = get_connection()
    df = pd.read_sql(f"SELECT * FROM orders ORDER BY timestamp DESC LIMIT {limit}", conn)
    conn.close()
    return df
