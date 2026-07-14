# Coding-Agent Usage

I used ChatGPT/Codex as the main coding agent throughout this assignment. I delegated repository scaffolding, repetitive FastAPI route structure, Pydantic schema boilerplate, Next.js component wiring, test boilerplate, Docker/documentation drafts, and UI polish iterations. I personally reviewed and directed the data model, authentication behavior, resume validation, email fallback behavior, state transition flow, documentation scope, and final submission structure because those areas affect correctness, security, and evaluator clarity.

One subtle issue produced during iteration was that the internal login page initially stored any typed token and navigated to the dashboard before verifying it with the backend. The backend still protected the data, but the UX was misleading because an invalid token appeared to enter the internal page. I caught this while manually testing invalid credentials and fixed it by validating the token against the protected `GET /api/leads` endpoint before storing it. I also added dashboard logic to clear invalid stored tokens and redirect back to login.

All agent-assisted code was manually reviewed, run locally, tested with Pytest/build checks, and revised before submission.

