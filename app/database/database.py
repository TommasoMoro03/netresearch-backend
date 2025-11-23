import sqlite3
import json
from typing import Optional, Dict, Any
from contextlib import contextmanager
import os


class Database:
    """SQLite database manager for the application."""

    def __init__(self, db_path: str = "netresearch.db"):
        """Initialize database connection."""
        # Use absolute path relative to backend directory
        backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.db_path = os.path.join(backend_dir, db_path)
        self._init_db()

    def _init_db(self):
        """Initialize database tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create user table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    cv_transcribed TEXT
                )
            """)

            # Create run table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS run (
                    id TEXT PRIMARY KEY,
                    query TEXT NOT NULL,
                    graph_data TEXT
                )
            """)

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    # User operations
    def get_user(self) -> Optional[dict]:
        """Get the user (there should only be one)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM user LIMIT 1")
            row = cursor.fetchone()
            if row:
                return {
                    "id": row["id"],
                    "name": row["name"],
                    "cv_transcribed": row["cv_transcribed"]
                }
            return None

    def create_user(self, name: str, cv_transcribed: str) -> int:
        """Create a new user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (name, cv_transcribed) VALUES (?, ?)",
                (name, cv_transcribed)
            )
            conn.commit()
            return cursor.lastrowid

    def update_user_cv(self, cv_transcribed: str) -> None:
        """Update the CV of the existing user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user SET cv_transcribed = ? WHERE id = (SELECT id FROM user LIMIT 1)",
                (cv_transcribed,)
            )
            conn.commit()

    def update_user_name(self, name: str) -> None:
        """Update the name of the existing user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user SET name = ? WHERE id = (SELECT id FROM user LIMIT 1)",
                (name,)
            )
            conn.commit()

    # Run operations
    def create_run(self, run_id: str, query: str, graph_data: Optional[Dict[str, Any]] = None) -> None:
        """Create a new run."""
        # Serialize graph_data to JSON if provided
        graph_data_json = json.dumps(graph_data) if graph_data else None

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO run (id, query, graph_data) VALUES (?, ?, ?)",
                (run_id, query, graph_data_json)
            )
            conn.commit()

    def get_run(self, run_id: str) -> Optional[dict]:
        """Get a run by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM run WHERE id = ?", (run_id,))
            row = cursor.fetchone()
            if row:
                # Deserialize graph_data from JSON if present
                graph_data = json.loads(row["graph_data"]) if row["graph_data"] else None
                return {
                    "id": row["id"],
                    "query": row["query"],
                    "graph_data": graph_data
                }
            return None

    def update_run_graph(self, run_id: str, graph_data: Dict[str, Any]) -> None:
        """Update the graph data for a run."""
        # Serialize graph_data to JSON
        graph_data_json = json.dumps(graph_data)

        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE run SET graph_data = ? WHERE id = ?",
                (graph_data_json, run_id)
            )
            conn.commit()

    def list_runs(self) -> list[dict]:
        """List all runs."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM run")
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "query": row["query"],
                    "graph_data": json.loads(row["graph_data"]) if row["graph_data"] else None
                }
                for row in rows
            ][::-1]


# Global database instance
db = Database()
