import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Literal, cast

from wechat_chatbot.domain import ChatMessage


class HistoryStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(path)) as connection, connection:
            connection.execute(
                """CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )"""
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS messages_user_id ON messages(user_id, id)"
            )

    def recent(self, user_id: str, limit: int = 20) -> list[ChatMessage]:
        with closing(sqlite3.connect(self.path)) as connection:
            rows = connection.execute(
                "SELECT role, content FROM messages WHERE user_id = ? ORDER BY id DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        return [
            ChatMessage(role=cast(Literal["user", "assistant"], role), content=content)
            for role, content in reversed(rows)
        ]

    def save_exchange(self, user_id: str, text: str, answer: str) -> None:
        with closing(sqlite3.connect(self.path)) as connection, connection:
            connection.executemany(
                "INSERT INTO messages (user_id, role, content) VALUES (?, ?, ?)",
                [(user_id, "user", text), (user_id, "assistant", answer)],
            )
