import os

import psycopg2

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "postgres"),
    "port": os.getenv("POSTGRES_PORT", "5432"),
    "user": os.getenv("POSTGRES_USER", "postgres_user"),
    "password": os.getenv("POSTGRES_PASSWORD", "postgres_password"),
    "dbname": os.getenv("POSTGRES_DB", "postgres_db"),
}

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS scores (
    id BIGSERIAL PRIMARY KEY,
    transaction_id TEXT UNIQUE NOT NULL,
    score DOUBLE PRECISION NOT NULL,
    fraud_flag INTEGER NOT NULL
);
"""

INSERT = """
INSERT INTO scores (transaction_id, score, fraud_flag)
VALUES (%(transaction_id)s, %(score)s, %(fraud_flag)s)
ON CONFLICT (transaction_id) DO UPDATE
SET score = EXCLUDED.score,
    fraud_flag = EXCLUDED.fraud_flag;
"""


def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    return conn


def init_table(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE)


def insert_score(conn, record):
    with conn.cursor() as cur:
        cur.execute(INSERT, record)
