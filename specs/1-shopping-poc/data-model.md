# Data Model

## Entities

- Product

  - Fields: `id` (string), `name` (string), `description` (string, optional), `price` (float), `imageUrl` (string, optional), `available` (bool)
  - Validation: `name` non-empty, `price` >= 0

- User

  - Fields: `id` (string), `email` (string, unique), `passwordHash` (string), `createdAt` (datetime)
  - Validation: `email` must be valid email

- Order
  - Fields: `id` (string), `userId` (string or null), `items` (list of {productId, quantity, price}), `totalAmount` (float), `createdAt` (datetime)
  - Validation: `quantity` >= 1, `price` >= 0

## Relationships

- Order -> User: optional many-to-one (orders may be placed by guests)
- Order -> Product: order items reference products by `productId`; prices are copied at purchase time

## State Transitions (POC)

- Product: created -> available/unavailable toggles
- Order: created (placed). No further fulfillment states modeled in POC.
