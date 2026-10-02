import os

import psycopg2
import psycopg2.extras

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "user": os.getenv("POSTGRES_USER", "postgres_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres_password"),
    "dbname": os.getenv("POSTGRES_DB", "postgres_db"),
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_recent_frauds(limit=10):
    query = """
        SELECT transaction_id, score, fraud_flag
        FROM scores
        WHERE fraud_flag = 1
        ORDER BY id DESC
        LIMIT %s;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, (limit,))
            return [dict(row) for row in cur.fetchall()]


def fetch_recent_scores(limit=100):
    query = """
        SELECT score
        FROM scores
        ORDER BY id DESC
        LIMIT %s;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, (limit,))
            return [row[0] for row in cur.fetchall()]
