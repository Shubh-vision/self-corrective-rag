import psycopg2
import socket


def get_connection():
    host = "db.fsjhbqnzefptdzbkrjck.supabase.co"

    # Force IPv4 resolution
    ipv4 = socket.getaddrinfo(host, 5432, socket.AF_INET)[0][4][0]



    conn =  psycopg2.connect(
        host=ipv4,
        database="postgres",
        user="postgres",
        password="Shubham9746",
        port="5432",
        sslmode="require"
        )
    return conn

print("✅ Connected to CLOUD PostgreSQL")