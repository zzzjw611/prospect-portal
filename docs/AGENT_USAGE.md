# Coding-Agent Usage

## Short Writeup

I used a coding agent to scaffold and implement the full-stack assignment. I delegated repetitive project setup, boilerplate API structure, form/dashboard UI wiring, documentation drafts, and local testing commands. I kept the product and architecture decisions human-directed: FastAPI backend, Next.js frontend, SQLite for local review, filesystem resume storage, SMTP-compatible email, and a simple token guard for the internal dashboard.

One place agent-generated code can easily be subtly wrong is authentication. A first pass may only hide the internal UI in the browser while leaving backend lead endpoints open. I caught this by checking the API surface and made the backend enforce `Authorization: Bearer <token>` on all internal endpoints, so the data is protected even if someone bypasses the frontend.

## Representative Prompt Logs

- "Read the assignment PDF and summarize the requirements."
- "Build the required FastAPI and Next.js project end to end."
- "Add local setup documentation, a design document, and coding-agent usage notes."

## Attribution

See `NOTES.md` for a concise attribution split between agent-assisted implementation and human-directed choices.

