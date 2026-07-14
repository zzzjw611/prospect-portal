from datetime import UTC, datetime
import sqlite3
from uuid import uuid4

from app.database import get_connection
from app.schemas import Lead, LeadStatus
from app.config import Settings


def _row_to_lead(row: sqlite3.Row) -> Lead:
    return Lead(
        id=row["id"],
        first_name=row["first_name"],
        last_name=row["last_name"],
        email=row["email"],
        resume_filename=row["resume_filename"],
        status=row["status"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def create_lead(
    settings: Settings,
    first_name: str,
    last_name: str,
    email: str,
    resume_filename: str,
    resume_path: str,
) -> Lead:
    now = datetime.now(UTC).isoformat()
    lead_id = str(uuid4())
    with get_connection(settings.database_path) as connection:
        connection.execute(
            """
            INSERT INTO leads (
                id, first_name, last_name, email, resume_filename,
                resume_path, status, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                lead_id,
                first_name,
                last_name,
                email,
                resume_filename,
                resume_path,
                LeadStatus.pending.value,
                now,
                now,
            ),
        )
        row = connection.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    return _row_to_lead(row)


def list_leads(settings: Settings) -> list[Lead]:
    with get_connection(settings.database_path) as connection:
        rows = connection.execute(
            "SELECT * FROM leads ORDER BY created_at DESC"
        ).fetchall()
    return [_row_to_lead(row) for row in rows]


def get_lead_row(settings: Settings, lead_id: str) -> sqlite3.Row | None:
    with get_connection(settings.database_path) as connection:
        return connection.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()


def update_lead_status(settings: Settings, lead_id: str, status: LeadStatus) -> Lead | None:
    now = datetime.now(UTC).isoformat()
    with get_connection(settings.database_path) as connection:
        connection.execute(
            "UPDATE leads SET status = ?, updated_at = ? WHERE id = ?",
            (status.value, now, lead_id),
        )
        row = connection.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
    if row is None:
        return None
    return _row_to_lead(row)

