from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import EmailStr, TypeAdapter, ValidationError

from app.auth import require_internal_auth
from app.config import Settings, get_settings
from app.database import initialize_database
from app.email_service import EmailService
from app.repository import create_lead, get_lead_row, list_leads, update_lead_status
from app.schemas import Lead, LeadCreated, LeadStatusUpdate


ALLOWED_RESUME_EXTENSIONS = {".pdf", ".doc", ".docx"}
EMAIL_ADAPTER = TypeAdapter(EmailStr)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    initialize_database(settings)
    yield


app = FastAPI(title="Prospect Portal API", lifespan=lifespan)


settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/leads", response_model=LeadCreated, status_code=status.HTTP_201_CREATED)
async def submit_lead(
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    resume: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
) -> LeadCreated:
    clean_first_name = first_name.strip()
    clean_last_name = last_name.strip()
    clean_email = email.strip().lower()
    if not clean_first_name or not clean_last_name or not clean_email:
        raise HTTPException(status_code=400, detail="First name, last name, and email are required")
    try:
        clean_email = str(EMAIL_ADAPTER.validate_python(clean_email))
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail="Valid email is required") from exc

    original_filename = Path(resume.filename or "").name
    extension = Path(original_filename).suffix.lower()
    if extension not in ALLOWED_RESUME_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Resume must be a PDF, DOC, or DOCX file")

    resume_dir = settings.storage_dir / "resumes"
    resume_dir.mkdir(parents=True, exist_ok=True)
    stored_filename = f"{uuid4()}{extension}"
    stored_path = resume_dir / stored_filename

    contents = await resume.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Resume file cannot be empty")
    if len(contents) > settings.max_resume_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"Resume file must be {settings.max_resume_bytes} bytes or smaller",
        )
    stored_path.write_bytes(contents)

    lead = create_lead(
        settings=settings,
        first_name=clean_first_name,
        last_name=clean_last_name,
        email=clean_email,
        resume_filename=original_filename,
        resume_path=str(stored_path),
    )
    EmailService(settings).send_lead_emails(lead)
    return LeadCreated(
        id=lead.id,
        status=lead.status,
        message="Lead submitted successfully",
    )


@app.get("/api/leads", response_model=list[Lead], dependencies=[Depends(require_internal_auth)])
def get_leads(settings: Settings = Depends(get_settings)) -> list[Lead]:
    return list_leads(settings)


@app.patch(
    "/api/leads/{lead_id}",
    response_model=Lead,
    dependencies=[Depends(require_internal_auth)],
)
def patch_lead_status(
    lead_id: str,
    payload: LeadStatusUpdate,
    settings: Settings = Depends(get_settings),
) -> Lead:
    lead = update_lead_status(settings, lead_id, payload.status)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


@app.get("/api/leads/{lead_id}/resume", dependencies=[Depends(require_internal_auth)])
def download_resume(lead_id: str, settings: Settings = Depends(get_settings)) -> FileResponse:
    row = get_lead_row(settings, lead_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Lead not found")

    resume_path = Path(row["resume_path"])
    if not resume_path.exists():
        raise HTTPException(status_code=404, detail="Resume file not found")

    return FileResponse(
        resume_path,
        media_type="application/octet-stream",
        filename=row["resume_filename"],
    )
