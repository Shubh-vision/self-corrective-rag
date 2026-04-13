import psycopg2


def get_connection():
    return psycopg2.connect(
        host="db.fsjhbqnzefptdzbkrjck.supabase.co",
        database="postgres",
        user="postgres",
        password="Shubham9746",
        port="5432")

print("✅ Connected to CLOUD PostgreSQL")