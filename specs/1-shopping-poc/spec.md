# Feature Specification: Shopping POC

**Feature Branch**: `1-shopping-poc`
**Created**: 2026-01-14
**Status**: Draft
**Input**: User description: "Create a proof-of-concept e-commerce shopping application using a Next.js frontend and a Python FastAPI backend with MongoDB as the database. The frontend and backend must be clearly separated, with frontend code in src/frontend and backend code in src/backend. The frontend should focus only on UI and basic client-side state, while all business logic, APIs, authentication, and data access live in the backend. Keep the scope intentionally small and simple, favoring clarity and minimal implementation over scalability or optimization."

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Browse & Place Order (Priority: P1)

A shopper can view a list of products, inspect a product detail, add items to a cart, review the cart, and place an order (POC: no external payment integration; order is recorded as "placed").

**Why this priority**: Demonstrates the core value of an e-commerce flow in minimum scope.

**Independent Test**: Use the UI to search/browse, add an item to the cart, complete the order flow; verify backend order record exists and cart is emptied.

**Acceptance Scenarios**:

1. **Given** product(s) exist, **When** a user opens the product list page, **Then** they see product names, images (if any), short descriptions, price, and an "Add to cart" button for each product.
2. **Given** items in cart, **When** user visits cart and clicks "Place order", **Then** backend creates an order record with items, quantities, total price, user reference (if logged in), and returns success.

---

### User Story 2 - Authentication (Priority: P2)

A shopper can create an account and sign in. The backend enforces authentication; the frontend only stores tokens for session continuity.

**Why this priority**: Authentication is required for account tracking and order history but is secondary to demonstrating placing an order.

**Independent Test**: Create account via frontend form → backend returns success and a JWT bearer token → use token to fetch user-specific endpoints (e.g., order history).

**Acceptance Scenarios**:

1. **Given** a new user, **When** they submit the registration form, **Then** backend creates the user and returns a JWT bearer token or directs user to login.
2. **Given** valid credentials, **When** user logs in, **Then** backend returns a JWT bearer token and protected endpoints succeed using that token.

---

### User Story 3 - Simple Product Management (Priority: P3)

A maintainer may add or update product entries via backend API (UI optional for POC). This supports demonstrating product CRUD without a full admin UI.

**Why this priority**: Supports testing product lifecycle and makes it easy to create demo data.

**Independent Test**: Use a backend-only contract test or minimal admin UI to create a product, then verify it appears in product list.

**Acceptance Scenarios**:

1. **Given** authenticated maintainer credentials, **When** they POST a valid product payload to the API, **Then** the product is persisted and appears in product list responses.

---

### Edge Cases

- Adding more items than available inventory: POC may allow unlimited inventory unless explicitly modeled as limited.
- Network failure during order placement: order request must fail safely and not leave partial data; idempotency is encouraged but optional for POC.
- Malformed API requests: backend must return appropriate 4xx responses with clear error messages.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST return a list of products via a backend API endpoint; frontend MUST display that list.
- **FR-002**: System MUST allow adding items to a cart on the frontend; the cart view MUST be able to submit an order request to the backend.
- **FR-003**: Backend MUST create an order record when the frontend places an order; the record MUST include items, quantities, total amount, timestamp, and `userId` (nullable to allow guest checkout). When a user is authenticated, `userId` SHOULD reference that user.
- **FR-004**: Backend MUST implement authentication endpoints (register, login, logout) and issue JWT bearer tokens (sent in `Authorization: Bearer <token>`). The frontend MUST store tokens for session continuity but MUST NOT perform authoritative validation or authorization decisions.
- **FR-005**: Backend MUST expose simple, versioned REST APIs (e.g., `/api/v1/products`, `/api/v1/cart`, `/api/v1/orders`, `/api/v1/auth`).
- **FR-006**: MongoDB MUST be used as the sole persistent store; backend MUST persist products, users, and orders in MongoDB.
- **FR-007**: Backend MUST validate and sanitize inputs for all public endpoints and return appropriate error codes for invalid requests.
- **FR-008**: The frontend MUST not contain business logic that alters persistent state outside via the backend APIs.

### Key Entities

- **Product**: id, name, description, price, imageUrl (optional), available (boolean)
- **User**: id, email, passwordHash, createdAt
- **Cart** (frontend concept): list of product ids + quantities; persisted on the frontend session only for POC (optional server cart endpoint allowed)
- **Order**: id, userId (nullable for guest), items (productId, quantity, priceAtPurchase), totalAmount, createdAt

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: A demo user can complete the browse → add to cart → place order flow end-to-end in under 2 minutes.
- **SC-002**: Backend exposes the documented API endpoints and returns correct status codes for happy path and key error cases (tested by contract tests).
- **SC-003**: On the demo environment, at least 90% of scripted acceptance tests for the primary flow (US1) pass.
- **SC-004**: No frontend files outside `src/frontend` contain server-side logic or data access code (enforceable by repository check or CI linting rule).

## Assumptions

- This is a POC: no external payment provider integration is required; orders are recorded as "placed" without payment processing.
- Inventory is optional; initial implementation may assume unlimited stock unless explicitly modelled.
- Authentication may use simple token-based sessions; implementation detail is left to the backend team, but authorization decisions must be enforced server-side.
- Minimal UI: product list, product detail, cart, checkout, login/register screens are sufficient for demo purposes.
- The user requested Next.js + FastAPI + MongoDB; this spec assumes those technologies as project constraints.

## Clarifications

### Session 2026-01-14

- Q: Which authentication mechanism should the POC use? → A: JWT bearer tokens (Authorization: Bearer <token>)
- Q: Should guest checkout be allowed? → A: Yes — guest checkout allowed (orders may be placed without authentication; `userId` stored as null).

## Admin Provisioning (required)

- Seed script: A seed script exists at `src/backend/scripts/seed_admin.py` that creates an initial admin account when run locally. The script MUST accept or read environment variables for admin email and password, and should print an admin JWT after creation for quick testing.
- Required env vars (backend):
  - `ADMIN_EMAIL` — the email to create for the admin account (default: `admin@example.com` when not provided).
  - `ADMIN_PASSWORD` — plaintext password for the seeded admin (must be provided for CI or set in dev only).
  - `JWT_SECRET` — secret used to sign JWT tokens (mandatory for running the app).
- Admin role: The `User` entity includes a boolean `isAdmin` flag. Admin-only endpoints (e.g., `POST /api/v1/products`) validate `isAdmin` server-side.
- JWT lifetime: The seed script prints a long-lived demo JWT (e.g., 30d) for local demos; production deployments MUST use shorter secrets/expirations and secure secret management.

Acceptance criteria for admin provisioning:

1. Running `python src/backend/scripts/seed_admin.py` with `ADMIN_EMAIL` and `ADMIN_PASSWORD` set creates a user with `isAdmin: true` in MongoDB and prints a JWT.
2. The backend enforces `isAdmin` checks for admin-only endpoints; contract tests verify admin-required endpoints return `403` for non-admin tokens.

## UI & Client-State Scope (Clarification)

- Required UI screens: Product List, Product Detail, Cart, Checkout, Login, Register.
- Client-side state for POC: cart (stored in browser `localStorage`) and JWT token for session continuity only. The frontend MUST NOT persist order data or business rules.
- Performance/UX boundary: primary flow (browse → add to cart → place order) should complete in under 2 minutes on a local dev machine; pages should render within 2s on typical dev hardware.

## Acceptance Tests (examples)

- Contract test: `GET /api/v1/products` returns `200` and a JSON array of products.
- Integration test: Place order flow - create demo product, add to cart, POST `/api/v1/orders` → verify order in DB.
- UI smoke: load product list page, add item to cart, proceed to checkout, and receive success message.

## Deliverables

- Minimal Next.js app under `src/frontend` implementing the UI and client-side cart.
- Minimal FastAPI app under `src/backend` implementing the REST APIs, auth, and MongoDB persistence.
- Contract tests for core endpoints and a small integration test for placing an order.

---
