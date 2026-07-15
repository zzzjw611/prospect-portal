# Representative Prompt Logs

## Prompt 1: Turn Requirements Into A Product Checklist

**Prompt**

Read the assignment requirements and convert them into a product delivery checklist. Separate what the applicant needs, what the internal attorney user needs, what the backend must support, and what documentation must be included for review.

**Agent Output Summary**

The agent mapped the assignment into two user surfaces: a public applicant form and an authenticated internal review dashboard. It also identified the required backend APIs, persistence, resume upload handling, email behavior, setup documentation, design notes, prompt logs, and attribution notes.

**My Review / Changes**

I confirmed the app should behave like two separate products on the same local domain: applicants should only see the submission flow, while internal users should access the dashboard through a protected route.

## Prompt 2: Design A Reviewer-Friendly MVP

**Prompt**

Design a local-first MVP architecture for this prospect portal that is realistic enough for the assignment but easy for a reviewer to run. Choose the simplest persistence, storage, auth, and email approach that still demonstrates the full workflow.

**Agent Output Summary**

The agent proposed a FastAPI + Next.js monorepo with SQLite, local filesystem resume storage, bearer-token internal auth, SMTP-compatible email, and a local outbox fallback when real email credentials are not configured.

**My Review / Changes**

I kept the implementation intentionally small and reviewable, then added `.env.example`, Docker Compose, a migration script, Swagger docs, and README instructions so the evaluator can run and inspect the system without external services.

## Prompt 3: Improve Trust, Feedback, And Edge Cases

**Prompt**

Review the app from a product engineer perspective and improve the parts that could confuse or weaken trust: invalid token behavior, resume upload validation, email confirmation expectations, status persistence, and dashboard feedback.

**Agent Output Summary**

The agent helped add backend-enforced token checks, frontend token verification before dashboard navigation, resume type and size validation, local email outbox documentation, status updates from `PENDING` to `REACHED_OUT`, resume download feedback, and live dashboard refresh.

**My Review / Changes**

I tested the confusing cases manually, especially invalid token login and missing confirmation emails. I revised the UX so invalid tokens are rejected before navigation and documented that local emails are stored in `backend/storage/outbox/emails.log` unless SMTP is configured.
