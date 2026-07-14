from argparse import ArgumentParser
from pathlib import Path
import shutil

from app.config import get_settings
from app.database import initialize_database
from app.repository import create_lead, update_lead_status
from app.schemas import LeadStatus


DEMO_LEADS = [
    {
        "first_name": "Maya",
        "last_name": "Chen",
        "email": "maya.chen@example.com",
        "status": LeadStatus.pending,
    },
    {
        "first_name": "Jordan",
        "last_name": "Lee",
        "email": "jordan.lee@example.com",
        "status": LeadStatus.reached_out,
    },
]


def reset_storage() -> None:
    settings = get_settings()
    if settings.database_path.exists():
        settings.database_path.unlink()
    if settings.storage_dir.exists():
        shutil.rmtree(settings.storage_dir)


def seed_demo_data() -> None:
    settings = get_settings()
    initialize_database(settings)
    resume_dir = settings.storage_dir / "resumes"
    resume_dir.mkdir(parents=True, exist_ok=True)

    for index, demo_lead in enumerate(DEMO_LEADS, start=1):
        resume_path = resume_dir / f"demo-resume-{index}.pdf"
        resume_path.write_text(
            f"Demo resume for {demo_lead['first_name']} {demo_lead['last_name']}\n",
            encoding="utf-8",
        )
        lead = create_lead(
            settings=settings,
            first_name=demo_lead["first_name"],
            last_name=demo_lead["last_name"],
            email=demo_lead["email"],
            resume_filename=resume_path.name,
            resume_path=str(resume_path),
        )
        if demo_lead["status"] == LeadStatus.reached_out:
            update_lead_status(settings, lead.id, LeadStatus.reached_out)


def main() -> None:
    parser = ArgumentParser(description="Seed local demo leads.")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Delete the local SQLite database and storage directory before seeding.",
    )
    args = parser.parse_args()

    if args.reset:
        reset_storage()
    seed_demo_data()
    print("Seeded demo leads.")


if __name__ == "__main__":
    main()

