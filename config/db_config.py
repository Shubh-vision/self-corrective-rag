import psycopg2
import socket
import streamlit as st


def get_connection():
    try:
        host = st.secrets["SUPABASE_DB_HOST"]

        print("Using host:", host)

        # Force IPv4
        ipv4 = socket.getaddrinfo(host, 5432, socket.AF_INET)[0][4][0]

        conn = psycopg2.connect(
            host=ipv4,
            database="postgres",
            user="postgres",
            password=st.secrets["SUPABASE_DB_PASSWORD"],  # 🔐 move to secrets
            port=5432,
            sslmode="require"
        )

        print("✅ Connected")
        return conn

    except Exception as e:
        print("❌ Error:", e)
        return None