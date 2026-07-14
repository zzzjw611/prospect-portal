# Prospect Portal

A full-stack lead intake application for prospects and attorneys.

## Stack

- Backend: FastAPI, SQLite, SMTP email integration
- Frontend: Next.js, React, TypeScript
- Storage: SQLite for lead data, local filesystem for uploaded resumes

## Local Setup

### 1. Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

The API will run at `http://localhost:8000`.

For local testing, email messages are written to `backend/storage/outbox/emails.log` unless SMTP is configured.

Interactive API docs are available at `http://127.0.0.1:8000/docs`.

To seed local demo data:

```bash
cd backend
source .venv/bin/activate
python scripts/seed_demo.py --reset
```

The `--reset` flag deletes the local SQLite database and storage directory before creating demo leads. Omit it if you want to keep existing local data.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The web app will run at `http://localhost:3000`.

Public applicant form:

```text
http://localhost:3000
```

Internal attorney login:

```text
http://localhost:3000/internal/login
```

The public applicant page does not link to the internal dashboard. Internal routes are separated by URL and protected by backend bearer-token checks.

### Demo Credentials

Internal dashboard token:

```text
dev-attorney-token
```

Use it on the internal login page at `http://localhost:3000/internal/login`.

## Main Workflows

1. Prospect opens the public form and submits name, email, and resume.
2. Backend stores the lead and resume.
3. Backend sends confirmation/notification emails, or writes them to the dev outbox.
4. Attorney logs into the internal dashboard.
5. Attorney reviews and filters leads, downloads resumes, and marks leads as `REACHED_OUT`.
6. The dashboard polls for live updates every 5 seconds while live updates are enabled.

## Local Email Behavior

The backend supports SMTP through environment variables. Without SMTP settings, the application uses a development outbox:

```text
backend/storage/outbox/emails.log
```

This lets reviewers verify confirmation and attorney notification emails without external credentials. Configure `SMTP_HOST`, `SMTP_USERNAME`, `SMTP_PASSWORD`, and `SMTP_FROM_EMAIL` in `backend/.env` to send real email.

## API Summary

- `POST /api/leads` - create a public lead with multipart form data.
- `GET /api/leads` - list leads, requires bearer token.
- `PATCH /api/leads/{lead_id}` - update lead status, requires bearer token.
- `GET /api/leads/{lead_id}/resume` - download resume, requires bearer token.
- `GET /health` - health check.

Resume uploads accept `.pdf`, `.doc`, and `.docx` files up to `MAX_RESUME_BYTES` bytes. The default is 10MB.

## Verification

```bash
backend/.venv/bin/python -m pytest
cd frontend && npm run build
cd frontend && npm audit --omit=dev
```

## Assignment Documents

- [System design](docs/SYSTEM_DESIGN.md)
- [Coding-agent usage](docs/AGENT_USAGE.md)
- [Attribution notes](NOTES.md)
