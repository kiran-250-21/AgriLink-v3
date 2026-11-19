"""
Section 6: Database Architecture & Complete API Specification
"""

def get_content():
    return r"""# CHAPTER 7: DATABASE ARCHITECTURE & COMPLETE API SPECIFICATION

### 7.1 Mongoose Schemas, Relationships, Constraints, and Indexing

AgriLink employs MongoDB with Mongoose ODM to maintain a flexible yet rigorously validated document schema. The schema encompasses 11 interconnected collections designed for sub-millisecond lookups and atomic concurrency control.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               AGRILINK ENTITY RELATIONSHIP ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                      ┌──────────────┐                                            │
│                                      │     User     │                                            │
│                                      │ (Role: RBAC) │                                            │
│                                      └──────┬───────┘                                            │
│                 ┌───────────────────────────┼───────────────────────────┐                        │
│                 ▼                           ▼                           ▼                        │
│         ┌──────────────┐            ┌──────────────┐            ┌──────────────┐                 │
│         │   Harvest    │            │ BuyerRequire │            │   Vehicle    │                 │
│         │ (Farm Stock) │            │ (Buy Offers) │            │ (Transport)  │                 │
│         └──────┬───────┘            └──────────────┘            └──────┬───────┘                 │
│                 │                                                      │                         │
│                 │ Creates                                              │ Assigned                │
│                 ▼                                                      ▼                         │
│         ┌──────────────┐       Directs       ┌──────────────┐       Carried  │                   │
│         │    Order     ├────────────────────>│   Delivery   │<───────────────┘                   │
│         │ (Financials) │                     │  (Logistics) │                                    │
│         └──────┬───────┘                     └──────────────┘                                    │
│                 │                                                                                │
│                 ▼                                                                                │
│         ┌──────────────┐                                                                         │
│         │Recommendation│                                                                         │
│         │ (Snapshots)  │                                                                         │
│         └──────────────┘                                                                         │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Detailed Collection Specifications:

#### 1. `User` Collection (`backend/models/User.js`)
- **Purpose**: Unified account collection storing credentials and polymorphic profiles for all four roles.
- **Fields**:
  - `name`: String, required, trimmed.
  - `email`: String, required, unique, lowercase, indexed.
  - `phone`: String, required, trimmed.
  - `passwordHash`: String, required (hashed via bcrypt with 10 salt rounds).
  - `role`: String enum (`['FARMER', 'BUYER', 'DRIVER', 'ADMIN']`), required.
  - `status`: String enum (`['ACTIVE', 'SUSPENDED', 'INACTIVE']`), default `'ACTIVE'`.
  - `verificationStatus`: String enum (`['VERIFIED', 'UNVERIFIED', 'PENDING']`).
  - `farmerProfile`: Sub-document containing `farmName`, `farmLocation`, `village`, `district`, `state`, `pincode`, `farmSize` (acres), `primaryCrops`.
  - `buyerProfile`: Sub-document containing `businessName`, `businessType`, `businessLocation`, `gstNumber`, `preferredCrops`.
  - `driverProfile`: Sub-document containing `licenseNumber`, `vehicleId` (ObjectId ref `Vehicle`), `serviceAreas`.
- **Indexes**: Unique index on `email`.

#### 2. `Harvest` Collection (`backend/models/Harvest.js`)
- **Purpose**: Stores produce declared by farmers ready for market intelligence or sale.
- **Fields**:
  - `farmerId`: ObjectId ref `User`, required, indexed.
  - `cropName`: String, required, indexed (case-insensitive search).
  - `category`: String, default `'Spices'`.
  - `expectedQuantity`: Number, required, `min: 1`.
  - `availableQuantity`: Number, required, `min: 0` (guarded by atomic operations).
  - `unit`: String, default `'Kg'`.
  - `quality`: String enum (`['GRADE_A', 'GRADE_B', 'GRADE_C']`), default `'GRADE_A'`.
  - `farmLocation`: String, required.
  - `latitude`, `longitude`: Number (geocoded coordinates).
  - `status`: String enum (`['PLANNED', 'READY', 'AVAILABLE', 'PARTIALLY_SOLD', 'SOLD_OUT', 'CANCELLED']`), indexed.

#### 3. `Market` Collection (`backend/models/Market.js`)
- **Purpose**: Registry of official APMC regulated wholesale mandi yards.
- **Fields**:
  - `name`: String, required, unique, trimmed.
  - `location`: String, required.
  - `district`: String, default `'Guntur'`.
  - `latitude`, `longitude`: Number.
  - `supportedCrops`: Array of Strings.
  - `active`: Boolean, default `true`.

#### 4. `MarketPrice` Collection (`backend/models/MarketPrice.js`)
- **Purpose**: Daily wholesale commodity clearing prices recorded per mandi.
- **Fields**:
  - `marketId`: ObjectId ref `Market`, required, indexed.
  - `crop`: String, required, indexed.
  - `quality`: String enum (`['GRADE_A', 'GRADE_B', 'GRADE_C']`).
  - `pricePerUnit`: Number, required (Rupees per kg).
  - `source`: String, default `'APMC Official Feed'`.
  - `validFrom`, `validUntil`: Dates.
  - `updatedBy`: ObjectId ref `User`.

#### 5. `BuyerRequirement` Collection (`backend/models/BuyerRequirement.js`)
- **Purpose**: Institutional procurement buy offers published by food processing companies.
- **Fields**:
  - `buyerId`: ObjectId ref `User`, required, indexed.
  - `crop`: String, required, indexed.
  - `requiredQuantity`: Number, required.
  - `offeredPrice`: Number, required (Rupees per kg).
  - `quality`: String enum (`['GRADE_A', 'GRADE_B', 'GRADE_C']`).
  - `location`: String, required.
  - `validUntil`: Date, default 30 days from creation.
  - `status`: String enum (`['ACTIVE', 'FULFILLED', 'EXPIRED', 'CANCELLED']`), indexed.

#### 6. `Order` Collection (`backend/models/Order.js`)
- **Purpose**: Represents legally binding commercial trade agreements between farmers and mandis/buyers.
- **Fields**:
  - `farmerId`: ObjectId ref `User`, required, indexed.
  - `buyerId`: ObjectId ref `User`, optional (null for APMC direct orders).
  - `marketId`: ObjectId ref `Market`, optional.
  - `harvestId`: ObjectId ref `Harvest`, required.
  - `cropName`: String, required.
  - `quantity`: Number, required.
  - `agreedPricePerUnit`: Number, required.
  - `grossRevenue`: Number, required.
  - `estimatedLogisticsCost`: Number, required.
  - `estimatedNetRevenue`: Number, required.
  - `destinationType`: String enum (`['MARKET', 'BUYER']`), required.
  - `destinationName`: String, required.
  - `deliveryAddress`: String, required.
  - `orderStatus`: String enum (`['PENDING_BUYER_CONFIRMATION', 'BUYER_ACCEPTED', 'REJECTED', 'LOGISTICS_REQUIRED', 'DRIVER_ASSIGNED', 'IN_DELIVERY', 'DELIVERED', 'COMPLETED', 'CANCELLED']`), default `'PENDING_BUYER_CONFIRMATION'`, indexed.
  - `deliveryId`: ObjectId ref `Delivery`.

#### 7. `Delivery` Collection (`backend/models/Delivery.js`)
- **Purpose**: Physical haulage tracking and logistics milestone state machine.
- **Fields**:
  - `orderId`: ObjectId ref `Order`, required, indexed.
  - `farmerId`: ObjectId ref `User`, required, indexed.
  - `buyerId`: ObjectId ref `User`, optional.
  - `driverId`: ObjectId ref `User`, optional (assigned upon job acceptance), indexed.
  - `vehicleId`: ObjectId ref `Vehicle`.
  - `pickupLocation`, `dropoffLocation`: Strings, required.
  - `totalDistanceKm`: Number, required.
  - `estimatedCost`: Number, required.
  - `actualCost`: Number.
  - `status`: String enum (`['LOGISTICS_REQUIRED', 'DRIVER_ASSIGNED', 'PICKUP_SCHEDULED', 'PICKED_UP', 'IN_TRANSIT', 'DELIVERED', 'BUYER_CONFIRMED', 'COMPLETED']`), indexed.
  - `timeline`: Array of `{ status, timestamp, note }`.

#### 8. `Recommendation` Collection (`backend/models/Recommendation.js`)
- **Purpose**: Historical audit snapshots of market intelligence recommendations generated for farmers.
- **Fields**:
  - `harvestId`: ObjectId ref `Harvest`, required.
  - `farmerId`: ObjectId ref `User`, required.
  - `quantityAnalyzed`: Number, required.
  - `recommendedOption`: Object containing destination name, type, selling price, gross revenue, logistics cost, net revenue, distance.
  - `allOptions`: Array of ranked option objects.

#### 9. `AuditLog` Collection (`backend/models/AuditLog.js`)
- **Purpose**: Immutable security audit trail recording all critical platform operations.
- **Fields**:
  - `userId`: ObjectId ref `User`.
  - `userRole`: String.
  - `action`: String, required (e.g., `'BUYER_DIRECT_PURCHASE'`, `'DRIVER_ACCEPTED_JOB'`).
  - `targetResource`: String (e.g., `'Order:67be10c0...'`).
  - `details`: String.
  - `createdAt`: Date (auto timestamp).

#### 10. `Notification` Collection (`backend/models/Notification.js`)
- **Purpose**: In-app lifecycle alerts dispatched to specific users.
- **Fields**:
  - `recipientId`: ObjectId ref `User`, required, indexed.
  - `recipientRole`: String enum (`['FARMER', 'BUYER', 'DRIVER', 'ADMIN']`).
  - `title`, `message`: Strings, required.
  - `type`: String, default `'GENERAL'`.
  - `isRead`: Boolean, default `false`.

#### 11. `Vehicle` Collection (`backend/models/Vehicle.js`)
- **Purpose**: Commercial vehicles registered by logistics transporters.
- **Fields**:
  - `driverId`: ObjectId ref `User`, required.
  - `vehicleType`: String (e.g., `'Tata Ace (1 Ton)'`, `'Eicher 14ft (4 Tons)'`).
  - `registrationNumber`: String, required, unique, trimmed.
  - `maxCapacityKg`: Number, required.
  - `ratePerKmPerTon`: Number, default `12`.
  - `active`: Boolean, default `true`.

---

### 7.2 Realistic Document JSON Payloads

#### Sample 1: Completed Order Document (`Order.json`)
```json
{
  "_id": "67be10c5f10283c842e12b10",
  "farmerId": "67be10a4f10283c842e12a91",
  "buyerId": "67be10a4f10283c842e12a93",
  "harvestId": "67be10b0f10283c842e12a95",
  "cropName": "Chilli",
  "quantity": 5000,
  "agreedPricePerUnit": 205,
  "grossRevenue": 1025000,
  "estimatedLogisticsCost": 4100,
  "estimatedNetRevenue": 1020900,
  "destinationType": "BUYER",
  "destinationName": "Buyer: Godavari Agro Processing Ltd",
  "deliveryAddress": "Auto Nagar Industrial Area, Vijayawada",
  "orderStatus": "DRIVER_ASSIGNED",
  "deliveryId": "67be10c5f10283c842e12b12",
  "createdAt": "2026-10-27T10:15:30.120Z"
}
```

#### Sample 2: Active Delivery Document (`Delivery.json`)
```json
{
  "_id": "67be10c5f10283c842e12b12",
  "orderId": "67be10c5f10283c842e12b10",
  "farmerId": "67be10a4f10283c842e12a91",
  "buyerId": "67be10a4f10283c842e12a93",
  "driverId": "67be10a4f10283c842e12a94",
  "pickupLocation": "Pedakakani, Guntur",
  "dropoffLocation": "Auto Nagar Industrial Area, Vijayawada",
  "totalDistanceKm": 35,
  "estimatedCost": 4100,
  "status": "DRIVER_ASSIGNED",
  "timeline": [
    {
      "status": "LOGISTICS_REQUIRED",
      "timestamp": "2026-10-27T10:15:30.125Z",
      "note": "Buyer confirmed purchase. Awaiting driver assignment."
    },
    {
      "status": "DRIVER_ASSIGNED",
      "timestamp": "2026-10-27T10:18:45.310Z",
      "note": "Assigned to driver Arun Kumar (AP07TJ1234)"
    }
  ]
}
```

---

### 7.3 Master REST API Route Specification Table

Extracted directly from active backend route manifests (`backend/routes/*.js`):

| HTTP Method | API Endpoint | Responsibility & Business Purpose | Expected Input Payload / Query Params | Response Payload & Status Code | Error Status Codes | Actual Source File |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **POST** | `/api/auth/register` | Register a new user account with role-specific profile subdocument. | `{ name, email, phone, password, role, farmerProfile, ... }` | HTTP 201: Created User object + signed JWT bearer token. | 400 (Validation fail / Email exists) | `backend/routes/authRoutes.js` |
| **POST** | `/api/auth/login` | Authenticate existing user via email/password; return JWT. | `{ email, password }` | HTTP 200: User profile + signed JWT bearer token. | 400 (Missing fields), 401 (Invalid creds) | `backend/routes/authRoutes.js` |
| **GET** | `/api/auth/me` | Fetch authenticated user's active session profile. | Headers: `Authorization: Bearer <token>` | HTTP 200: User document without `passwordHash`. | 401 (Unauthorized), 403 (Suspended) | `backend/routes/authRoutes.js` |
| **POST** | `/api/harvests` | Farmer declares a new crop harvest with quantity and location. | Headers: JWT (FARMER)<br>`{ cropName, expectedQuantity, quality, farmLocation }` | HTTP 201: Newly persisted Harvest document with geocoded GPS. | 400 (Bad input), 403 (Non-Farmer) | `backend/routes/harvestRoutes.js` |
| **GET** | `/api/harvests/my` | Retrieve all harvests declared by the logged-in farmer. | Headers: JWT (FARMER) | HTTP 200: Array of Harvest documents sorted by date descending. | 401 (Unauthorized), 403 (Non-Farmer) | `backend/routes/harvestRoutes.js` |
| **GET** | `/api/harvests/available` | Browse active crop marketplace open for commercial purchase. | Headers: JWT (Authenticated) | HTTP 200: Array of Harvest documents with `status: AVAILABLE`. | 401 (Unauthorized) | `backend/routes/harvestRoutes.js` |
| **GET** | `/api/harvests/:id` | Retrieve specific harvest batch details. | URL Param: `:id` (Harvest ObjectId) | HTTP 200: Harvest document populated with farmer details. | 404 (Harvest not found) | `backend/routes/harvestRoutes.js` |
| **PUT** | `/api/harvests/:id` | Update harvest details or status. | URL Param: `:id`<br>`{ availableQuantity, status, ... }` | HTTP 200: Updated Harvest document. | 400 (Invalid update), 404 (Not found) | `backend/routes/harvestRoutes.js` |
| **POST** | `/api/recommendations/analyze` | Run Market Intelligence & Net Return Engine on harvest lot. | Headers: JWT<br>`{ harvestId, quantity }` | HTTP 200: `{ harvest, recommendedOption, allOptions: [ranked] }` | 400 (Missing harvestId), 404 (Not found) | `backend/routes/recommendationRoutes.js` |
| **POST** | `/api/orders` | Create sale order (Farmer selects Mandi/Buyer OR Buyer direct purchase). | Headers: JWT (FARMER/BUYER)<br>`{ harvestId, destinationType, quantity, agreedPricePerUnit }` | HTTP 201: Created Order and Delivery documents. | 400 (Stock check fail), 403 (Forbidden) | `backend/routes/orderRoutes.js` |
| **PUT** | `/api/orders/:id/respond` | Buyer accepts or rejects an incoming farmer sale request. | Headers: JWT (BUYER)<br>`{ action: 'ACCEPT' \| 'REJECT' }` | HTTP 200: Updated Order + newly spawned Delivery document. | 400 (Invalid status / stock gone), 403 | `backend/routes/orderRoutes.js` |
| **GET** | `/api/orders/my` | Fetch user's orders (Farmer sales, Buyer purchases, or Admin all). | Headers: JWT (Authenticated) | HTTP 200: Array of populated Order records. | 401 (Unauthorized) | `backend/routes/orderRoutes.js` |
| **GET** | `/api/deliveries/available` | Drivers browse unassigned freight jobs awaiting transport. | Headers: JWT (DRIVER/ADMIN) | HTTP 200: Array of Delivery jobs in `LOGISTICS_REQUIRED` status. | 403 (Non-Driver/Admin) | `backend/routes/deliveryRoutes.js` |
| **PUT** | `/api/deliveries/:id/accept` | Driver claims an unassigned shipment contract. | Headers: JWT (DRIVER)<br>URL Param: `:id` | HTTP 200: Delivery updated to `DRIVER_ASSIGNED` with driver info. | 400 (Already assigned), 404 (Not found) | `backend/routes/deliveryRoutes.js` |
| **PUT** | `/api/deliveries/:id/status` | Advance shipment milestone (`PICKED_UP`, `IN_TRANSIT`, `DELIVERED`). | Headers: JWT<br>`{ status, note }` | HTTP 200: Delivery with appended timeline event and updated state. | 400 (Invalid status transition) | `backend/routes/deliveryRoutes.js` |
| **GET** | `/api/deliveries/my` | Fetch active and historical shipments handled by logged-in user. | Headers: JWT (Authenticated) | HTTP 200: Array of populated Delivery records. | 401 (Unauthorized) | `backend/routes/deliveryRoutes.js` |
| **POST** | `/api/buyer/requirements` | Buyer publishes commercial procurement buy listing. | Headers: JWT (BUYER)<br>`{ crop, requiredQuantity, offeredPrice, location }` | HTTP 201: Newly persisted BuyerRequirement document. | 400 (Bad input), 403 (Non-Buyer) | `backend/routes/buyerRoutes.js` |
| **GET** | `/api/buyer/requirements/my` | Fetch all procurement offers posted by logged-in buyer. | Headers: JWT (BUYER) | HTTP 200: Array of active BuyerRequirement documents. | 403 (Non-Buyer) | `backend/routes/buyerRoutes.js` |
| **GET** | `/api/buyer/sale-requests` | Buyer views incoming sales intents submitted by farmers. | Headers: JWT (BUYER) | HTTP 200: Array of Orders in `PENDING_BUYER_CONFIRMATION`. | 403 (Non-Buyer) | `backend/routes/buyerRoutes.js` |
| **GET** | `/api/markets` | Fetch all registered APMC mandis. | Public Endpoint | HTTP 200: Array of active Market documents. | None (Public) | `backend/routes/marketRoutes.js` |
| **POST** | `/api/markets` | Admin registers a new APMC mandi hub. | Headers: JWT (ADMIN)<br>`{ name, location, latitude, longitude }` | HTTP 201: Created Market document. | 400 (Duplicate name), 403 (Non-Admin) | `backend/routes/marketRoutes.js` |
| **GET** | `/api/markets/prices` | Fetch daily clearing commodity prices. | Public Endpoint | HTTP 200: Array of MarketPrice documents. | None (Public) | `backend/routes/marketRoutes.js` |
| **POST** | `/api/markets/prices` | Admin updates official commodity rate for a mandi. | Headers: JWT (ADMIN)<br>`{ marketId, crop, pricePerUnit, quality }` | HTTP 201: Created / Updated MarketPrice document. | 400 (Bad input), 403 (Non-Admin) | `backend/routes/marketRoutes.js` |
| **GET** | `/api/notifications` | Fetch unread notifications for logged-in user. | Headers: JWT (Authenticated) | HTTP 200: Array of Notification documents. | 401 (Unauthorized) | `backend/routes/notificationRoutes.js` |
| **PUT** | `/api/notifications/:id/read` | Mark specific notification as read. | Headers: JWT<br>URL Param: `:id` | HTTP 200: Notification updated to `isRead: true`. | 404 (Not found) | `backend/routes/notificationRoutes.js` |
| **GET** | `/api/admin/users` | Admin fetches all platform user accounts. | Headers: JWT (ADMIN) | HTTP 200: Array of User documents. | 403 (Non-Admin) | `backend/routes/adminRoutes.js` |
| **PUT** | `/api/admin/users/:id/status`| Admin suspends or activates user account. | Headers: JWT (ADMIN)<br>`{ status: 'SUSPENDED' \| 'ACTIVE' }` | HTTP 200: Updated User document. | 400 (Invalid status), 403 (Non-Admin) | `backend/routes/adminRoutes.js` |
| **GET** | `/api/admin/analytics` | Admin fetches platform-wide aggregate telemetry metrics. | Headers: JWT (ADMIN) | HTTP 200: `{ totalUsers, harvests, orders, activeDeliveries }` | 403 (Non-Admin) | `backend/routes/adminRoutes.js` |
| **GET** | `/api/admin/audit-logs` | Admin inspects immutable security and transaction audit logs. | Headers: JWT (ADMIN) | HTTP 200: Array of AuditLog documents sorted by timestamp. | 403 (Non-Admin) | `backend/routes/adminRoutes.js` |
"""
