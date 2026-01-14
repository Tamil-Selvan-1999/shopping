---
description: "Task list for Shopping POC implementation"
---

# Tasks: Shopping POC

**Input**: Design documents from `/specs/1-shopping-poc/`  
**Prerequisites**: `plan.md`, `spec.md` (existing)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic developer setup

- [ ] T001 Create project structure and verify `src/frontend` and `src/backend` exist (src/frontend, src/backend)
- [ ] T002 [P] Initialize Python virtualenv and install backend dependencies in `src/backend/requirements.txt` (src/backend)
- [ ] T003 [P] Install frontend dependencies (`npm install`) and verify `next dev` runs (src/frontend)
- [ ] T004 [P] Configure linting and formatting: add `pyproject.toml`/`ruff`/`black` for backend and `eslint`/`prettier` for frontend (src/backend, src/frontend)
- [ ] T005 [P] Add environment template files: `src/backend/.env.example` and `src/frontend/.env.example` with required env vars (src/backend/.env.example, src/frontend/.env.example)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend infra that MUST be ready before implementing user stories

- [ ] T006 Setup MongoDB connectivity and health-check endpoint in `src/backend/app/db.py` and `src/backend/app/main.py` (src/backend/app/db.py, src/backend/app/main.py)
- [ ] T007 [P] Implement authentication helpers (password hashing, JWT creation/verification) in `src/backend/app/auth.py` (src/backend/app/auth.py)
- [ ] T008 [P] Setup API routing, CORS, and middleware structure in `src/backend/app/main.py` (src/backend/app/main.py)
- [ ] T009 [P] Define Pydantic schemas/models for Product, User, Order in `src/backend/app/schemas.py` (src/backend/app/schemas.py)
- [ ] T010 [P] Configure basic error handling and structured logging for backend in `src/backend/app/main.py` (src/backend/app/main.py)
- [ ] T011 [P] Add automated check/CI job draft to validate that frontend files exist only under `src/frontend` and backend files under `src/backend` (.github/workflows/ci-validate-boundaries.yml)

**Checkpoint**: Foundational phase complete — user story work may begin

---

## Phase 3: User Story 1 - Browse & Place Order (Priority: P1) 🎯 MVP

**Goal**: Implement product listing, cart, and order placement end-to-end

**Independent Test**: Using frontend, browse products, add to cart, place order; verify order record exists in MongoDB and `userId` is nullable for guest.

### Implementation

- [ ] T012 [P] [US1] Implement `GET /api/v1/products` endpoint in `src/backend/app/main.py` (src/backend/app/main.py)
- [ ] T013 [P] [US1] Implement `POST /api/v1/orders` endpoint and persistence logic in `src/backend/app/main.py` and `src/backend/app/db.py` (src/backend/app/main.py, src/backend/app/db.py)
- [ ] T014 [US1] Create frontend product listing page at `src/frontend/app/products/page.tsx` and wire API calls (src/frontend/app/products/page.tsx)
- [ ] T015 [US1] Implement frontend cart UI and checkout flow (client-side state) in `src/frontend/app/` (suggested files: `src/frontend/app/cart/page.tsx`, `src/frontend/app/checkout/page.tsx`)
- [ ] T016 [P] [US1] Add a simple integration test to `specs/1-shopping-poc/tests/integration/test_place_order.py` that posts an order and verifies DB record (specs/1-shopping-poc/tests/integration/test_place_order.py)
- [ ] T017 [US1] Update `specs/1-shopping-poc/quickstart.md` with demo steps for placing an order (specs/1-shopping-poc/quickstart.md)

**Checkpoint**: US1 should be independently demonstrable

---

## Phase 4: User Story 2 - Authentication (Priority: P2)

**Goal**: User registration and login with JWT tokens

**Independent Test**: Register a user and login; use token to access a protected endpoint.

- [ ] T018 [P] [US2] Implement `POST /api/v1/auth/register` and `POST /api/v1/auth/login` in `src/backend/app/main.py` (src/backend/app/main.py)
- [ ] T019 [P] [US2] Implement JWT creation/verification and password hashing in `src/backend/app/auth.py` (src/backend/app/auth.py)
- [ ] T020 [P] [US2] Implement frontend login/register pages and token storage at `src/frontend/app/login/page.tsx` and `src/frontend/app/register/page.tsx` (src/frontend/app/login/page.tsx)
- [ ] T021 [P] [US2] Ensure frontend attaches `Authorization: Bearer <token>` to protected API calls (src/frontend/app/\*)
- [ ] T022 [P] [US2] Add contract tests for auth endpoints in `specs/1-shopping-poc/tests/contract/test_auth.py` (specs/1-shopping-poc/tests/contract/test_auth.py)

---

## Phase 5: User Story 3 - Simple Product Management (Priority: P3)

**Goal**: Allow maintainers to create products (admin-protected)

**Independent Test**: Seed or create an admin user and POST a product; verify product appears in list.

- [ ] T023 [P] [US3] Implement protected `POST /api/v1/products` in `src/backend/app/main.py` (src/backend/app/main.py)
- [ ] T024 [P] [US3] Add admin seed script `src/backend/scripts/seed_admin.py` to create admin account and print JWT (src/backend/scripts/seed_admin.py)
- [ ] T025 [P] [US3] Add contract tests for product creation in `specs/1-shopping-poc/tests/contract/test_products.py` (specs/1-shopping-poc/tests/contract/test_products.py)
- [ ] T026 [P] [US3] (Optional) Minimal admin UI for product creation at `src/frontend/app/admin/page.tsx` (src/frontend/app/admin/page.tsx)

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, CI, formatting, and security hardening

- [ ] T027 [P] Documentation updates: finalize `specs/1-shopping-poc/*.md` and `src/*/README.md` (specs/1-shopping-poc/, src/frontend/README.md, src/backend/README.md)
- [ ] T028 [P] Add GitHub Action to validate frontend/backend separation and MongoDB-only persistence (`.github/workflows/validate-boundaries.yml`)
- [ ] T029 [P] Add pre-commit hooks and CI lint job (`.husky/` or `.github/workflows/lint.yml`, `pyproject.toml`) (repo root)
- [ ] T030 [P] Run smoke tests and integration tests in CI (workflows) (specs/1-shopping-poc/tests/)

---

## Dependencies & Execution Order

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Setup completion — blocks user-story work
- **User Stories (Phase 3+)**: Depend on Foundational phase completion

### Story Order & Dependencies

- **US1 (P1)**: Start after Foundational; independent from US2/US3
- **US2 (P2)**: Start after Foundational; independent but may be used by US3
- **US3 (P3)**: Start after Foundational; requires auth infra from US2 for admin checks

---

## Parallel Execution Examples

- Setup tasks `T002`, `T003`, `T004`, `T005` run in parallel across different developers
- Foundational tasks `T006`, `T007`, `T009`, `T010` can run in parallel
- Once foundational done, US1, US2 and US3 implementation tasks can proceed in parallel by separate engineers

Example parallel command for US1 contract + integration tests:

```bash
# run contract tests in parallel (example)
pytest specs/1-shopping-poc/tests/contract/ -q & pytest specs/1-shopping-poc/tests/integration/ -q
```

---

## Implementation Strategy

**MVP First (User Story 1 Only)**n

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Implement Phase 3: User Story 1 and validate end-to-end
4. Stop and demo the browse → add to cart → place order flow

**Incremental Delivery**

- After MVP, implement US2 (auth) then US3 (product management)
- Each story should remain independently testable and demoable

---

## Validation

All tasks above follow the required checklist format (checkbox + Task ID + optional `[P]` + optional `[USx]` label + description with file paths).
