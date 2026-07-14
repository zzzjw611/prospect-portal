# System Design

## Goal

The application supports public lead intake and an authenticated internal workflow for attorneys to review and update submitted leads.

## Architecture

The system is split into two applications:

- `backend`: FastAPI service responsible for lead APIs, persistence, upload handling, auth checks, and email delivery.
- `frontend`: Next.js app responsible for the public intake form and the internal attorney dashboard.

The frontend talks to the backend over HTTP. Public lead creation does not require authentication. Internal lead reads, resume downloads, and status updates require an attorney bearer token.

## Data Model

`leads`

| Field | Purpose |
| --- | --- |
| `id` | UUID primary identifier |
| `first_name` | Prospect first name |
| `last_name` | Prospect last name |
| `email` | Prospect email |
| `resume_filename` | Original uploaded resume filename |
| `resume_path` | Server-side stored file path |
| `status` | `PENDING` or `REACHED_OUT` |
| `created_at` | Submission timestamp |
| `updated_at` | Last update timestamp |

Uploaded resumes are stored on disk under `backend/storage/resumes`. Lead metadata is stored in SQLite.

## API Design

- `POST /api/leads`
  - Public endpoint.
- Accepts multipart form data: `first_name`, `last_name`, `email`, `resume`.
- Validates required fields, email format, resume extension, non-empty uploads, and maximum resume size.
- Creates a lead in `PENDING` state.
- Sends confirmation email to the prospect and notification email to the attorney.

- `GET /api/leads`
  - Internal endpoint.
  - Requires `Authorization: Bearer <token>`.
  - Returns all submitted leads.
  - Used by the dashboard for manual refresh and 5-second live polling.

- `PATCH /api/leads/{lead_id}`
  - Internal endpoint.
  - Requires bearer token.
  - Allows an attorney to change status to `PENDING` or `REACHED_OUT`.

- `GET /api/leads/{lead_id}/resume`
  - Internal endpoint.
  - Requires bearer token.
  - Returns the uploaded resume file.

## Authentication

The assignment asks for an auth-guarded internal UI. This implementation uses a configured internal bearer token for the demo. The frontend stores the token in browser local storage and sends it to the backend for internal API calls.

For production, this should be replaced with SSO or passwordless login, server-managed HTTP-only sessions, short-lived access tokens, role-based permissions, and audit logging.

## Email

The backend integrates with SMTP using environment variables. If SMTP is not configured, it writes email payloads to `backend/storage/outbox/emails.log`. This gives reviewers a complete local E2E workflow without needing external credentials.

Production deployments should use a transactional email provider such as SendGrid, Postmark, Mailgun, or AWS SES, with retry handling and delivery monitoring.

## Storage Choices

SQLite and local file storage were chosen for fast local review and simple setup. In production, the database would move to Postgres and uploaded resumes would move to object storage such as S3 or GCS with encrypted buckets and signed download URLs.

## Reliability And Security Notes

- Resume uploads are limited by accepted extensions and a configurable size limit. The local default is 10MB.
- Internal endpoints require auth.
- CORS is configured through environment variables.
- Production should add malware scanning, file size limits at the reverse proxy, rate limiting, audit logs, backup policies, and stricter secrets management.

## Demo And Review Support

The backend includes `scripts/seed_demo.py` so reviewers can quickly create local sample leads. Running it with `--reset` clears local SQLite/file storage and creates a fresh demo dataset for screen recordings.
