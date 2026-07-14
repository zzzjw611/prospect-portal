from pathlib import Path

from fastapi.testclient import TestClient

from app.config import get_settings
from app.database import initialize_database
from app.main import app


def test_create_and_update_lead(tmp_path: Path) -> None:
    settings = get_settings()
    settings.database_path = tmp_path / "test.db"
    settings.storage_dir = tmp_path / "storage"
    settings.internal_api_token = "test-token"
    initialize_database(settings)

    client = TestClient(app)
    response = client.post(
        "/api/leads",
        data={
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ADA@EXAMPLE.COM",
        },
        files={"resume": ("resume.pdf", b"pdf content", "application/pdf")},
    )

    assert response.status_code == 201
    lead_id = response.json()["id"]

    unauthorized = client.get("/api/leads")
    assert unauthorized.status_code == 401

    leads = client.get(
        "/api/leads",
        headers={"Authorization": "Bearer test-token"},
    )
    assert leads.status_code == 200
    assert leads.json()[0]["email"] == "ada@example.com"
    assert leads.json()[0]["status"] == "PENDING"

    updated = client.patch(
        f"/api/leads/{lead_id}",
        json={"status": "REACHED_OUT"},
        headers={"Authorization": "Bearer test-token"},
    )
    assert updated.status_code == 200
    assert updated.json()["status"] == "REACHED_OUT"

    resume = client.get(
        f"/api/leads/{lead_id}/resume",
        headers={"Authorization": "Bearer test-token"},
    )
    assert resume.status_code == 200
    assert resume.content == b"pdf content"


def test_invalid_email_is_rejected_before_create(tmp_path: Path) -> None:
    settings = get_settings()
    settings.database_path = tmp_path / "test.db"
    settings.storage_dir = tmp_path / "storage"
    initialize_database(settings)

    client = TestClient(app)
    response = client.post(
        "/api/leads",
        data={
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "not-an-email",
        },
        files={"resume": ("resume.pdf", b"pdf content", "application/pdf")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Valid email is required"


def test_invalid_resume_type_is_rejected(tmp_path: Path) -> None:
    settings = get_settings()
    settings.database_path = tmp_path / "test.db"
    settings.storage_dir = tmp_path / "storage"
    initialize_database(settings)

    client = TestClient(app)
    response = client.post(
        "/api/leads",
        data={
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@example.com",
        },
        files={"resume": ("resume.txt", b"text content", "text/plain")},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Resume must be a PDF, DOC, or DOCX file"


def test_oversized_resume_is_rejected(tmp_path: Path) -> None:
    settings = get_settings()
    settings.database_path = tmp_path / "test.db"
    settings.storage_dir = tmp_path / "storage"
    settings.max_resume_bytes = 4
    initialize_database(settings)

    client = TestClient(app)
    response = client.post(
        "/api/leads",
        data={
            "first_name": "Ada",
            "last_name": "Lovelace",
            "email": "ada@example.com",
        },
        files={"resume": ("resume.pdf", b"12345", "application/pdf")},
    )

    assert response.status_code == 413
    assert response.json()["detail"] == "Resume file must be 4 bytes or smaller"
