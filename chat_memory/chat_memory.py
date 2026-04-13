from config.db_config import get_connection
import os

host = os.getenv("SUPABASE_DB_HOST")
password = os.getenv("SUPABASE_DB_PASSWORD")


#=============================================SAVE MEMORY==================================================================================
def save_summary(user_id, summary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chat_memory (user_id, summary) VALUES (%s, %s)",
        (user_id, summary)
    )

    conn.commit()
    cursor.close()
    conn.close()


#========================================================LOAD MEMORY===============================================================
def get_recent_summaries(user_id, limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT summary FROM chat_memory
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT %s
        """,
        (user_id, limit)
    )

    
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return [row[0] for row in data]


#===============================REMOVE/TRIM OLD MEMORY===========================================================================

def trim_old_summaries(user_id, keep_limit=5):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        WITH ranked AS (
            SELECT id,
                   ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) as rn
            FROM chat_memory
            WHERE user_id = %s
        )
        DELETE FROM chat_memory
        WHERE id IN (
            SELECT id FROM ranked WHERE rn > %s
        )
        RETURNING id;
    """, (user_id, keep_limit))

    deleted_rows = cursor.fetchall()

    conn.commit()

    print(f"🧹 Deleted {len(deleted_rows)} old memories for user {user_id}")

    cursor.close()
    conn.close()
