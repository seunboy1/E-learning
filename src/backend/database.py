# database.py

import sqlite3
from flask import g


class Database:
    def __init__(self, database_name="test_questions.db"):
        self.database_name = database_name

    def init_db(self):
        """Initialize the database and create the TestQuestions table."""
        with self.get_db() as db:
            cursor = db.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS TestQuestions (
                    id TEXT PRIMARY KEY,
                    test_question TEXT NOT NULL,
                    test_answer TEXT NOT NULL
                )
            """
            )
            db.commit()

    def get_db(self):
        """Get a database connection, maintaining a persistent connection for the duration of a request."""
        if "db" not in g:
            g.db = sqlite3.connect(self.database_name)
            g.db.row_factory = sqlite3.Row
        return g.db

    def close_db(self):
        """Close the database connection."""
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def save_test_question(self, id, question, answer):
        """Save a test question and answer in the database."""
        db = self.get_db()
        cursor = db.cursor()

        # Insert test question and answer into the table
        cursor.execute(
            """
            INSERT INTO TestQuestions (id, test_question, test_answer)
            VALUES (?, ?, ?)
        """,
            (id, question, answer),
        )

        # Commit the transaction
        db.commit()

        # Return the inserted test question ID
        return id

    def get_test_answer(self, test_question_id):
        """Retrieve the test answer by test_question_id."""
        db = self.get_db()
        cursor = db.cursor()

        # Execute the query to fetch the test answer
        cursor.execute(
            "SELECT test_answer FROM TestQuestions WHERE id = ?", (test_question_id,)
        )
        result = cursor.fetchone()

        # Return the test_answer, or None if not found
        if result:
            return result["test_answer"]  # Fetch as dict if using `row_factory`
        return None

    def get_test_question(self, test_question_id):
        """Retrieve the test question by test_question_id."""
        db = self.get_db()
        cursor = db.cursor()

        # Execute the query to fetch the test answer
        cursor.execute(
            "SELECT test_question FROM TestQuestions WHERE id = ?", (test_question_id,)
        )
        result = cursor.fetchone()

        # Return the test_answer, or None if not found
        if result:
            return result["test_question"]  # Fetch as dict if using `row_factory`
        return None
