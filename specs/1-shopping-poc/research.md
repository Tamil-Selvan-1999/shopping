# research.md

## Decisions

- Decision: Use Next.js for frontend and FastAPI for backend.

  - Rationale: User specified these technologies; both are lightweight and fast for POC.
  - Alternatives considered: Single-server rendered backend or SPA with different frontend frameworks; rejected to honor stakeholder constraints.

- Decision: MongoDB as sole persistent store.

  - Rationale: Explicit requirement; motor async driver fits FastAPI.

- Decision: JWT bearer tokens for authentication.

  - Rationale: Stateless, easy to implement for APIs and POC; frontend stores token for session continuity.

- Decision: Minimal security posture for POC.
  - Rationale: Focus on demonstration; production hardening deferred to amendments.

## Open Questions (resolved)

- Q: Auth mechanism? → Resolved: JWT bearer (documented in spec)
- Q: Product creation admin control? → Resolved: Admin identified via `ADMIN_EMAIL` env var; creation restricted to that account.
