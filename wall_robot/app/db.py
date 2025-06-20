import sqlite3
from sqlite3 import Connection
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "wall_robot.db"

def get_connection() -> Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trajectories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        wall_width REAL NOT NULL,
        wall_height REAL NOT NULL,
        obstacles TEXT NOT NULL,
        trajectory TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON trajectories (timestamp)")
    conn.commit()
    conn.close()
