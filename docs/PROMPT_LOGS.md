# Representative Prompt Logs

## Prompt 1: Assignment Requirements

**Prompt**

Read the assignment PDF and summarize the requirements.

**Agent Output Summary**

The agent identified the public lead form, internal attorney dashboard, FastAPI API requirement, Next.js frontend requirement, persistence, email integration, design doc, local setup doc, and coding-agent usage submission.

**My Review / Changes**

I confirmed that the product needed two surfaces: a public applicant form and an authenticated internal review workflow.

## Prompt 2: Repository Architecture

**Prompt**

Build the required FastAPI and Next.js project end to end.

**Agent Output Summary**

The agent scaffolded a monorepo with `backend/`, `frontend/`, and `docs/`, using SQLite, local resume storage, FastAPI routes, and Next.js pages.

**My Review / Changes**

I kept the architecture local-first for reviewer convenience and later added Docker Compose, a migration command, and clearer production trade-off documentation.

## Prompt 3: FastAPI Lead APIs

**Prompt**

Implement lead creation, listing, status update, resume upload/download, auth, and email integration.

**Agent Output Summary**

The agent generated FastAPI endpoints for `POST /api/leads`, `GET /api/leads`, `PATCH /api/leads/{lead_id}`, and resume download.

**My Review / Changes**

I verified that internal endpoints enforce bearer-token auth on the backend, not only in the UI.

## Prompt 4: File Upload Safety

**Prompt**

Improve upload handling and tests.

**Agent Output Summary**

The agent added resume extension validation, email validation, upload size checks, and tests for invalid files.

**My Review / Changes**

I added a configurable `MAX_RESUME_BYTES` setting so the local default is 10MB and production can change it through environment variables.

## Prompt 5: Internal UI

**Prompt**

Build an authenticated internal dashboard for attorneys to review leads.

**Agent Output Summary**

The agent generated a login page, token verification flow, dashboard table, status filters, live polling, resume download, and `REACHED_OUT` updates.

**My Review / Changes**

I asked for the public and internal surfaces to be separated in the UI so applicants do not see an internal entry point.

## Prompt 6: Email Fallback

**Prompt**

Explain why confirmation email is not arriving locally.

**Agent Output Summary**

The agent found that SMTP was not configured and local emails were written to `backend/storage/outbox/emails.log`.

**My Review / Changes**

I kept the outbox fallback for local demos and documented how to configure SMTP for real delivery.

## Prompt 7: Agent Mistake Fix

**Prompt**

Why does an invalid token still enter the dashboard?

**Agent Output Summary**

The agent identified that the login page saved the token before backend validation.

**My Review / Changes**

I changed login to verify the token against the protected FastAPI endpoint before storing it and added dashboard logic to clear invalid stored tokens.

