# Prospect Portal

## Overview

Prospect Portal is a full-stack lead management application with two separate surfaces:

- Public applicant form: `http://localhost:3000`
- Internal attorney dashboard: `http://localhost:3000/internal/login`

Prospects submit contact information and a resume/CV. Attorneys authenticate with an internal token, review submitted leads, download resumes, and update lead status from `PENDING` to `REACHED_OUT`.

## Features

- Public lead form with first name, last name, email, and resume/CV upload.
- FastAPI backend APIs for creating, listing, updating, and downloading lead resources.
- Internal UI protected by backend bearer-token authentication.
- SQLite persistence for local review.
- Local filesystem resume storage.
- SMTP email integration with local outbox fallback.
- Live dashboard polling, filters, resume download feedback, and status updates.
- Docker Compose support for local full-stack startup.

## Tech Stack

- Frontend: Next.js, React, TypeScript
- Backend: FastAPI, Pydantic
- Database: SQLite
- Storage: Local filesystem for uploaded resumes
- Email: SMTP or local development outbox
- Tests: Pytest, FastAPI TestClient

## Architecture

The frontend and backend are separate applications in one monorepo:

```text
frontend/  Next.js public and internal UI
backend/   FastAPI APIs, persistence, uploads, auth, email
docs/      Design, prompt logs, and coding-agent usage
```

The public applicant page does not link to the internal dashboard. Internal routes are separated by URL and protected by backend bearer-token checks.

## Prerequisites

- Python 3.12+
- Node.js 22+
- npm
- Docker Desktop, optional for Docker Compose

## Environment Variables

Copy examples before running locally:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env.local
```

Important variables:

```text
INTERNAL_API_TOKEN=dev-attorney-token
ATTORNEY_EMAIL=attorney@example.com
CORS_ORIGINS=http://localhost:3000
MAX_RESUME_BYTES=10485760
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

SMTP is optional:

```text
SMTP_HOST=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=no-reply@example.com
SMTP_USE_TLS=true
```

If SMTP is not configured, emails are written to:

```text
backend/storage/outbox/emails.log
```

## Local Development

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/migrate.py
uvicorn app.main:app --reload --port 8000
```

The API runs at:

```text
http://localhost:8000
```

### Frontend

In a second terminal:

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

The web app runs at:

```text
http://localhost:3000
```

## Running with Docker

From the repository root:

```bash
docker compose up --build
```

Then open:

```text
Public applicant form: http://localhost:3000
Internal login:        http://localhost:3000/internal/login
FastAPI Swagger:       http://localhost:8000/docs
```

To run the migration inside Docker:

```bash
docker compose run --rm backend python scripts/migrate.py
```

## Database Migration

The local schema is initialized by:

```bash
cd backend
source .venv/bin/activate
python scripts/migrate.py
```

This creates the SQLite `leads` table if it does not already exist. For production, this should be replaced with versioned migrations such as Alembic.

## Test Accounts

Internal attorney token:

```text
dev-attorney-token
```

The login page includes a testing tip and copy button for local review.

## API Documentation

Swagger UI:

```text
http://localhost:8000/docs
```

API summary:

- `POST /api/leads` - create a public lead with multipart form data.
- `GET /api/leads` - list leads, requires bearer token.
- `PATCH /api/leads/{lead_id}` - update lead status, requires bearer token.
- `GET /api/leads/{lead_id}/resume` - download resume, requires bearer token.
- `GET /health` - health check.

Resume uploads accept `.pdf`, `.doc`, and `.docx` files up to `MAX_RESUME_BYTES` bytes. The default is 10MB.

## Running Tests

```bash
backend/.venv/bin/python -m pytest
cd frontend && npm run build
cd frontend && npm audit --omit=dev
```

## Demo Data

To reset local data and seed two demo leads:

```bash
cd backend
source .venv/bin/activate
python scripts/seed_demo.py --reset
```

The `--reset` flag deletes the local SQLite database and storage directory before creating demo leads. Omit it if you want to keep existing local data.

## Main Workflow

1. Prospect opens the public form and submits name, email, and resume.
2. Backend stores the lead and resume.
3. Backend sends confirmation/notification emails, or writes them to the dev outbox.
4. Attorney logs into the internal dashboard.
5. Attorney reviews and filters leads, downloads resumes, and marks leads as `REACHED_OUT`.
6. The dashboard polls for live updates every 5 seconds while live updates are enabled.

## Known Limitations

- SQLite and local filesystem storage are used for local review; production should use Postgres and object storage.
- Demo auth uses a single configured bearer token; production should use SSO or server-managed sessions.
- Email delivery writes to a local outbox unless SMTP is configured.
- Migration support initializes the current schema but is not a full versioned migration history.

## Assignment Documents

- [System design](docs/DESIGN.md)
- [Coding-agent usage](docs/AGENT_USAGE.md)
- [Representative prompt logs](docs/PROMPT_LOGS.md)
- [Attribution notes](NOTES.md)
