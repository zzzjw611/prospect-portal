# Representative Prompt Logs

## Prompt 1: Assignment Requirements

**Prompt**

Based on the assignment PDF, turn the requirements into a delivery checklist and map each item to the app feature or document we need to build.

**Agent Output Summary**

The agent identified the public applicant form, authenticated internal attorney dashboard, FastAPI API requirement, Next.js frontend requirement, persistence, email integration, design document, local setup instructions, prompt logs, attribution notes, and coding-agent usage writeup.

**My Review / Changes**

I confirmed that the product needed two surfaces: a public applicant form and an authenticated internal review workflow.

## Prompt 2: Repository Architecture

**Prompt**

Create a FastAPI + Next.js monorepo for a prospect intake portal with a public submission page, an internal review page, SQLite storage, resume uploads, and local email fallback.

**Agent Output Summary**

The agent scaffolded a monorepo with `backend/`, `frontend/`, and `docs/`, using SQLite, local resume storage, FastAPI routes, environment examples, and Next.js pages.

**My Review / Changes**

I kept the architecture local-first for reviewer convenience and later added Docker Compose, a migration command, and clearer production trade-off documentation.

## Prompt 3: FastAPI Lead APIs

**Prompt**

Implement the lead workflow API: create a lead with multipart resume upload, list leads for authenticated attorneys, update status, download resumes, and send the two required emails.

**Agent Output Summary**

The agent generated FastAPI endpoints for `POST /api/leads`, `GET /api/leads`, `PATCH /api/leads/{lead_id}`, and resume download.

**My Review / Changes**

I verified that internal endpoints enforce bearer-token auth on the backend, not only in the UI.

## Prompt 4: File Upload Safety

**Prompt**

Add backend validation for resume uploads and write tests for bad file types, invalid email addresses, and oversized files.

**Agent Output Summary**

The agent added resume extension validation, email validation, upload size checks, and tests for invalid files.

**My Review / Changes**

I added a configurable `MAX_RESUME_BYTES` setting so the local default is 10MB and production can change it through environment variables.

## Prompt 5: Internal UI

**Prompt**

Build an internal attorney dashboard that requires a token, filters leads by status, supports live refresh, downloads resumes, and marks leads as `REACHED_OUT`.

**Agent Output Summary**

The agent generated a login page, token verification flow, dashboard table, status filters, live polling, resume download, and `REACHED_OUT` updates.

**My Review / Changes**

I asked for the public and internal surfaces to be separated in the UI so applicants do not see an internal entry point.

## Prompt 6: Email Fallback

**Prompt**

The app says confirmation emails were sent, but I did not receive one locally. Diagnose the email behavior and explain what a reviewer can inspect.

**Agent Output Summary**

The agent found that SMTP was not configured and local emails were written to `backend/storage/outbox/emails.log`.

**My Review / Changes**

I kept the outbox fallback for local demos and documented how to configure SMTP for real delivery.

## Prompt 7: Agent Mistake Fix

**Prompt**

Invalid attorney tokens still appear to enter the internal dashboard. Find the issue and change the login flow so invalid tokens are rejected before navigation.

**Agent Output Summary**

The agent identified that the login page saved the token before backend validation.

**My Review / Changes**

I changed login to verify the token against the protected FastAPI endpoint before storing it and added dashboard logic to clear invalid stored tokens.
