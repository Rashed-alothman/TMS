# models/database.py
# Handles all database setup and model definitions.
# This is the single source of truth for your data structure.

from datetime import datetime
from typing import Optional
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Mapped, mapped_column

# Create the db instance here — import it everywhere else
db = SQLAlchemy()


class Task(db.Model):
    __tablename__ = "tasks"

    id: Mapped[str] = mapped_column(
        String(8), primary_key=True, default=lambda: str(uuid4())[:8]
    )
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[Optional[datetime]] = mapped_column(db.DateTime, nullable=True)
    completed: Mapped[bool] = mapped_column(db.Boolean, default=False)
    priority: Mapped[str] = mapped_column(String(10), default="low")
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        due_date_str = (
            self.due_date.strftime("%Y-%m-%d %H:%M:%S") if self.due_date else "None"
        )
        return f"Task(id={self.id}, description={self.description}, due_date={due_date_str}, completed={self.completed})"

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "Due Date": self.due_date.strftime("%Y-%m-%d %H:%M:%S")
            if self.due_date
            else None,
            "completed": self.completed,
            "priority": self.priority,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
