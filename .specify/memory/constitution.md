<!--
Sync Impact Report
- Version change: TEMPLATE -> 1.0.0
- Modified principles:
	- (new) Separation of Frontend and Backend (added explicit directory & responsibility rules)
	- (new) Backend-First Business Logic & Auth
	- (new) MongoDB as Sole Persistent Store
	- (new) Simplicity Over Scalability (POC Principle)
	- (new) Versioned REST APIs & Clear Contracts
- Added sections: Constraints & Technical Boundaries; Development Workflow & Quality Gates
- Removed sections: none
- Templates requiring review: .specify/templates/plan-template.md (⚠ pending), .specify/templates/spec-template.md (⚠ pending), .specify/templates/tasks-template.md (⚠ pending)
- Commands folder (.specify/templates/commands) not present — manual check recommended (⚠ pending)
- Follow-up TODOs:
	- TODO(RATIFICATION_DATE): confirm official ratification approver(s) if not the author
	- Verify templates flagged above and update gates that reference constitution checks
	- Add automated CI check to validate `src/frontend` vs `src/backend` boundaries
-->

# Shopping POC Constitution

## Core Principles

### Separation of Frontend and Backend (NON-NEGOTIABLE)

The codebase MUST maintain a strict separation: all frontend sources live only under `src/frontend` and all backend sources live only under `src/backend`. The frontend is limited to UI rendering, client-side state, and presentation logic. All business logic, authentication, authorization, data validation, and data access MUST reside in the backend. This rule is testable by reviewing file locations and by ensuring no server-side responsibilities are implemented in `src/frontend`.

### Backend-First Business Logic & Authentication (NON-NEGOTIABLE)

All business rules, security checks, input validation, and authentication flows MUST be implemented in the backend. The backend is the single source of truth for authorization decisions and MUST expose versioned REST APIs that enforce those rules. The frontend MAY store authentication tokens for session continuity but MUST NOT perform authoritative validation or authorization decisions.

### MongoDB as Sole Persistent Store (NON-NEGOTIABLE)

MongoDB is the only permitted persistent database for this proof‑of‑concept. No additional persistent datastores or long-term file storage mechanisms are allowed without an explicit constitution amendment. Database schema and migration changes MUST be tracked and documented in the backend repository area.

### Simplicity Over Scalability (POC Principle)

This project is a proof‑of‑concept: prefer straightforward, minimal implementations that demonstrate intent and correctness. Avoid premature optimization, distributed complexity, or multi-datastore designs. Design decisions SHOULD favor clarity, observability, and fast iteration over high-scale architectural patterns.

### Versioned REST APIs & Clear Contracts (NON-NEGOTIABLE)

The backend MUST expose simple, versioned REST endpoints (e.g., `/api/v1/...`) with clear request/response contracts. API versions are part of the public contract and breaking changes MUST follow the Governance section (version bump rules). Contracts MUST be documented and include example requests, responses, and error conditions.

## Constraints & Technical Boundaries

Project layout and responsibilities:

- `src/frontend`: contains the Next.js application and all UI code. Responsibilities: rendering, routing, presentation state, form input handling, and calling backend APIs.
- `src/backend`: contains the Python FastAPI application. Responsibilities: business logic, authentication, authorization, data validation, persistence (MongoDB), and exposing versioned REST APIs.

Technical constraints (high level):

- Backend technology: Python + FastAPI. Frontend technology: Next.js (React).
- Persistence: MongoDB only. No additional DBs allowed without amendment.
- Network: All client operations that require data or logic MUST call the backend APIs; no business logic may be embedded in the frontend.
- Authentication: Implemented and enforced by backend; frontend only carries tokens for session continuity.

### Embedded Repositories / Submodules

Embedded git repositories (gitlinks/submodules) under `src/frontend` or `src/backend` are disallowed by default. An embedded repository hides file contents from a plain clone of the parent repo and can break constitution checks and CI validation that assumes a single coherent repository. If a sub-repository is required, it MUST be added explicitly as a documented Git submodule and the PR should include instructions for cloning (`git submodule update --init --recursive`) and rationale for why a submodule is necessary. Prefer copying or integrating the code under the appropriate `src/` directory for POC-level work.

These boundaries are non-negotiable for the POC and are intended to keep scope small and responsibilities clear.

## Development Workflow & Quality Gates

- Every code change that affects system behavior MUST be introduced via a pull request and reference the relevant spec or plan.
- PRs MUST include a short note confirming which constitution principles the change impacts (e.g., "Impacts: Separation of Frontend and Backend").
- Minimal testing expectations:
  - Backend: unit tests for business logic and minimal contract tests for each API (happy path + key error cases).
  - Frontend: smoke/UI integration tests as needed to exercise critical flows.
- Linting and formatting tools SHOULD be used per-language (e.g., ESLint/Prettier for frontend, black/ruff for backend).
- Any deviation from the constitution (e.g., adding a new datastore) MUST be proposed as a formal amendment in a PR and include a migration and rollback plan.

## Governance

Amendments, versioning, and compliance:

- Amendments: Changes to this constitution MUST be proposed through a repository PR that sets out the rationale, migration implications, and a testing/rollback plan. Approval requires at least one maintainer review plus one additional reviewer (or a maintainers majority if more than two maintainers exist).
- Versioning: This constitution follows semantic versioning for governance text only. MINOR bumps are for added principles or material expansions. PATCH bumps are for clarifications, wording, or typo fixes. MAJOR bumps are reserved for redefinitions that break prior guarantees.
- Compliance review: PRs that materially change system structure or cross the frontend/backend boundary MUST include an explicit constitution compliance checklist and be approved by reviewers who confirm the checklist passes.

**Version**: 1.0.0 | **Ratified**: 2026-01-14 | **Last Amended**: 2026-01-14
