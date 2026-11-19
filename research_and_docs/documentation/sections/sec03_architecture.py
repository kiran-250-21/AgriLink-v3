"""
Section 3: System Architecture, Component Interactions & Data Flow
"""

def get_content():
    return """# CHAPTER 4: SYSTEM ARCHITECTURE, COMPONENT INTERACTIONS & DATA FLOW

### 4.1 End-to-End Layered System Architecture

AgriLink implements a distributed, decoupled multi-tier architectural pattern. This design strictly segregates concerns between client-side state rendering, stateless RESTful API routing, business domain logic, spatial computational services, and persistent document storage.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                AGRILINK 5-TIER LAYERED ARCHITECTURE                              │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. PRESENTATION TIER (CLIENT SPA)                                                                │
│    • React 19 / 18 Component Tree (Farmer, Buyer, Driver, Admin Workspaces)                     │
│    • Client-Side Routing (<BrowserRouter>, <Routes>, <ProtectedRoute>)                           │
│    • Centralized Context Store (AuthContext, LocalStorage Session Synchronization)               │
│    • Axios HTTP Client with Bearer Token Request Interceptors                                    │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                          │  HTTPS / JSON Payload                                 │
│                                          ▼                                                       │
│ 2. API GATEWAY & ROUTING TIER                                                                    │
│    • Reverse Proxy & Static Host (Vite / Render Platform Edge)                                   │
│    • Express Application Server (`backend/server.js`)                                            │
│    • Global Middleware Pipeline (CORS, Express JSON Body Parser, UrlEncoded Parser)              │
│    • Centralized Exception Router & Custom Error Handler (`notFound`, `errorHandler`)            │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                          │  Route Dispatching                                    │
│                                          ▼                                                       │
│ 3. SECURITY & AUTHORIZATION TIER                                                                 │
│    • Authentication Guard (`backend/middleware/auth.js` -> `protect` via JWT verification)       │
│    • Role-Based Access Control (`backend/middleware/role.js` -> `requireRole('FARMER', etc)`)   │
│    • User Account Status Validation (`req.user.status !== 'SUSPENDED'`)                         │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                          │  Sanitized Controller Context                         │
│                                          ▼                                                       │
│ 4. CONTROLLER & BUSINESS LOGIC TIER                                                              │
│    • Request Handlers: `authController`, `harvestController`, `orderController`, etc.           │
│    • Atomic Transaction Locks & State Machine Orchestrators                                      │
│    • Computational Service Dispatchers:                                                          │
│      - `recommendationService.js` (Spatial filtering, Mandi price & Buyer requirement joining)   │
│      - `calculations.js` (Haversine distance, AP coordinate registry, Levenshtein typo engine)   │
│      - `notificationService.js` (Lifecycle alerts & in-app message publishing)                   │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                          │  ODM Queries & Atomic Mutations                       │
│                                          ▼                                                       │
│ 5. DATA PERSISTENCE & AUDIT TIER                                                                 │
│    • Mongoose ODM Schema Layer (Type validation, Enums, Default values, Lifecycle Hooks)         │
│    • MongoDB Document Collections (11 collections: Users, Harvests, Orders, Deliveries, etc.)    │
│    • Document-Level Concurrency Guards (`$inc`, `$set`, Conditional Matching `$gte`)             │
│    • Immutable Security Audit Log Collection (`AuditLog.js`)                                     │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 4.2 Comprehensive System Architecture Diagram

```
                 CLIENT DEVICES (SMARTPHONES, TABLETS, DESKTOP BROWSERS)
               🌾 Farmer        🏢 Buyer         🚛 Driver        🛡️ Admin
                   │                │                │                │
                   └────────────────┼────────────────┼────────────────┘
                                    │
                          HTTPS / Bearer JWT Token
                                    │
                                    ▼
                ┌───────────────────────────────────────┐
                │        EXPRESS.JS REST API SERVER     │
                │         (PORT 5000 / server.js)       │
                ├───────────────────────────────────────┤
                │  Middleware: CORS, JSON, UrlEncoded   │
                └───────────────────┬───────────────────┘
                                    │
                     Token Verification & Role Check
                                    │
                                    ▼
                ┌───────────────────────────────────────┐
                │     SECURITY & RBAC MIDDLEWARE        │
                │   • protect() [jwt.verify]            │
                │   • requireRole('FARMER', etc.)       │
                └───────────────────┬───────────────────┘
                                    │
               ┌────────────────────┼────────────────────┐
               ▼                    ▼                    ▼
     ┌───────────────────┐┌───────────────────┐┌───────────────────┐
     │ harvestController ││  orderController  ││deliveryController │
     │ • createHarvest() ││ • createOrder()   ││• getAvailableJobs │
     │ • getMyHarvests() ││ • respondToSale() ││• acceptJob()      │
     │ • getAvailable()  ││ • getMyOrders()   ││• updateStatus()   │
     └─────────┬─────────┘└─────────┬─────────┘└─────────┬─────────┘
               │                    │                    │
               │                    ▼                    │
               │          ┌───────────────────┐          │
               │          │ recommendation-   │          │
               │          │ Service.js        │          │
               │          └─────────┬─────────┘          │
               │                    │                    │
               ▼                    ▼                    ▼
     ┌─────────────────────────────────────────────────────────────┐
     │            CALCULATIONS ENGINE (calculations.js)            │
     │  • 26 AP District Coordinate Registry                       │
     │  • Telugu-to-Canonical Normalization & Levenshtein Typo Fix  │
     │  • Haversine Road Distance Calculation (1.22x Tortuosity)   │
     │  • Ton-Km Weight-Tiered Logistics Tariff Formula            │
     └──────────────────────────────┬──────────────────────────────┘
                                    │
                       Mongoose Models & Schema
                                    │
                                    ▼
     ┌─────────────────────────────────────────────────────────────┐
     │                   MONGODB DATA STORAGE                      │
     │  • Users (RBAC)            • Orders (Transactions)          │
     │  • Harvests (Inventory)    • Deliveries (Shipment Track)    │
     │  • Markets (APMC Mandis)   • AuditLogs (Compliance Trails)  │
     │  • MarketPrices (Daily)    • Notifications (User Alerts)    │
     │  • BuyerRequirements       • Vehicles (Transporter Fleet)   │
     └─────────────────────────────────────────────────────────────┘
```

---

### 4.3 Detailed Sequence & Flow Diagrams

#### 4.3.1 Sequence Flow 1: Normal Request (Harvest Declaration & Dashboard Synchronization)

This flow illustrates how a farmer declares newly harvested produce, how the system resolves farm geographic coordinates, saves the inventory to the database, and synchronizes the client dashboard.

```
FARMER (React Client)        EXPRESS API SERVER          CALCULATIONS ENGINE            MONGODB ATLAS
      │                               │                           │                           │
      │ 1. POST /api/harvests         │                           │                           │
      │    {cropName: "Chilli",       │                           │                           │
      │     quantity: 5000,           │                           │                           │
      │     location: "Guntur"}       │                           │                           │
      │──────────────────────────────>│                           │                           │
      │                               │ 2. protect & requireRole  │                           │
      │                               │    Validates JWT token    │                           │
      │                               │─────────────────────────┐ │                           │
      │                               │  Token Valid (FARMER)   │ │                           │
      │                               │<────────────────────────┘ │                           │
      │                               │                           │                           │
      │                               │ 3. Resolve Coordinates    │                           │
      │                               │    resolveCoordinates()   │                           │
      │                               │──────────────────────────>│                           │
      │                               │                           │ 4. Coordinate Lookup      │
      │                               │                           │    Lat: 16.3067           │
      │                               │                           │    Lng: 80.4365           │
      │                               │ 5. Return Coordinates     │<────────────────────────┐ │
      │                               │<──────────────────────────│                           │
      │                               │                           │                           │
      │                               │ 6. Harvest.create()                                   │
      │                               │    {farmerId, cropName,                               │
      │                               │     availableQuantity: 5000,                          │
      │                               │     latitude, longitude, status: "AVAILABLE"}         │
      │                               │──────────────────────────────────────────────────────>│
      │                               │                           │                           │
      │                               │ 7. AuditLog.create("HARVEST_DECLARED")                │
      │                               │──────────────────────────────────────────────────────>│
      │                               │                           │                           │
      │                               │ 8. HTTP 201 Created       │   Persisted Successfully  │
      │                               │    {harvestDocument}      │<──────────────────────────│
      │<──────────────────────────────│                           │                           │
      │                               │                           │                           │
      │ 9. UI Updates State           │                           │                           │
      │    Renders Harvest in Table   │                           │                           │
      ▼                               ▼                           ▼                           ▼
```

#### 4.3.2 Sequence Flow 2: Market Intelligence & Net Return Recommendation Pipeline

This flow captures the analytical heart of AgriLink: evaluating market clearing prices, spatial distances, freight haulage expenses, and ranking all destinations descending by net cash realization.

```
FARMER (React Client)        recommendationController     recommendationService          MONGODB ATLAS
      │                               │                           │                           │
      │ 1. POST /api/recommendations/ │                           │                           │
      │    analyze {harvestId, qty}   │                           │                           │
      │──────────────────────────────>│                           │                           │
      │                               │ 2. analyzeHarvestOptions()│                           │
      │                               │──────────────────────────>│                           │
      │                               │                           │ 3. Harvest.findById()     │
      │                               │                           │──────────────────────────>│
      │                               │                           │ 4. Return Harvest         │
      │                               │                           │<──────────────────────────│
      │                               │                           │                           │
      │                               │                           │ 5. MarketPrice.find()     │
      │                               │                           │    {crop: /^Chilli$/i}    │
      │                               │                           │──────────────────────────>│
      │                               │                           │ 6. Return Mandi Prices    │
      │                               │                           │<──────────────────────────│
      │                               │                           │                           │
      │                               │                           │ 7. BuyerRequirement.find()│
      │                               │                           │    {crop, status: ACTIVE} │
      │                               │                           │──────────────────────────>│
      │                               │                           │ 8. Return Buyer Offers    │
      │                               │                           │<──────────────────────────│
      │                               │                           │                           │
      │                               │                           │ 9. Spatial Loop (ForEach):│
      │                               │                           │    • calculateDistanceKm()│
      │                               │                           │    • calculateLogistics() │
      │                               │                           │    • calculateNetRevenue()│
      │                               │                           │─────────────────────────┐ │
      │                               │                           │  Gross = Price * Qty    │ │
      │                               │                           │  Freight = 2000+d*w*12  │ │
      │                               │                           │  Net = Gross - Freight  │ │
      │                               │                           │<────────────────────────┘ │
      │                               │                           │                           │
      │                               │                           │ 10. Sort Options:         │
      │                               │                           │     DESC by Net Revenue   │
      │                               │                           │     Set Rank 1 = 🏆 Best  │
      │                               │                           │─────────────────────────┐ │
      │                               │                           │<────────────────────────┘ │
      │                               │                           │                           │
      │                               │                           │ 11. Persist Recommendation│
      │                               │                           │     Recommendation.create │
      │                               │                           │──────────────────────────>│
      │                               │ 12. Return Analysis JSON  │                           │
      │                               │<──────────────────────────│                           │
      │ 13. HTTP 200 OK               │                           │                           │
      │     {recommendedOption,       │                           │                           │
      │      allOptions: [ranked]}    │                           │                           │
      │<──────────────────────────────│                           │                           │
      │                               │                           │                           │
      │ 14. Render RecommendationCards│                           │                           │
      │     Highlight 🏆 Best Return  │                           │                           │
      ▼                               ▼                           ▼                           ▼
```

#### 4.3.3 Sequence Flow 3: Concurrency Failure & Inventory Guard Scenario

This flow details how AgriLink's atomic inventory engine prevents race conditions when two buyers or a buyer and farmer simultaneously attempt to allocate the exact same crop lot.

```
BUYER 1 (Client A)          BUYER 2 (Client B)          orderController.createOrder()     MONGODB ATLAS
      │                           │                                    │                        │
      │ 1. POST /api/orders       │                                    │                        │
      │    Buy 5000 kg Chilli lot │                                    │                        │
      │───────────────────────────┼───────────────────────────────────>│                        │
      │                           │ 2. POST /api/orders (Simultaneous) │                        │
      │                           │    Buy 5000 kg Chilli lot          │                        │
      │                           │───────────────────────────────────>│                        │
      │                           │                                    │                        │
      │                           │                                    │ 3. Thread 1 Executes:  │
      │                           │                                    │    findOneAndUpdate({  │
      │                           │                                    │      _id: harvestId,   │
      │                           │                                    │      availQty: {$gte:  │
      │                           │                                    │                 5000}  │
      │                           │                                    │    }, {$inc: {         │
      │                           │                                    │      availQty: -5000}} │
      │                           │                                    │───────────────────────>│
      │                           │                                    │ 4. MongoDB Mutates Doc │
      │                           │                                    │    AvailQty: 5000->0   │
      │                           │                                    │    Returns Updated Doc │
      │                           │                                    │<───────────────────────│
      │                           │                                    │                        │
      │                           │                                    │ 5. Thread 2 Executes:  │
      │                           │                                    │    findOneAndUpdate({  │
      │                           │                                    │      _id: harvestId,   │
      │                           │                                    │      availQty: {$gte:  │
      │                           │                                    │                 5000}  │
      │                           │                                    │    }, {$inc: {         │
      │                           │                                    │      availQty: -5000}} │
      │                           │                                    │───────────────────────>│
      │                           │                                    │ 6. MATCH FAILS!        │
      │                           │                                    │    Current Qty = 0     │
      │                           │                                    │    Condition $gte 5000 │
      │                           │                                    │    Returns NULL        │
      │                           │                                    │<───────────────────────│
      │                           │                                    │                        │
      │                           │                                    │ 7. Thread 1 Completes: │
      │                           │                                    │    • Creates Order     │
      │                           │                                    │    • Creates Delivery  │
      │                           │                                    │    • Sends Notification│
      │ 8. HTTP 201 Created       │                                    │    • Logs Audit Trail  │
      │    Order Confirmed!       │                                    │───────────────────────>│
      │<──────────────────────────┼────────────────────────────────────│                        │
      │                           │                                    │ 8. Thread 2 Handles    │
      │                           │                                    │    Atomic Check Failure│
      │                           │ 9. HTTP 400 Bad Request            │                        │
      │                           │    "Atomic inventory check failed. │                        │
      │                           │     Quantity no longer available." │                        │
      │                           │<───────────────────────────────────│                        │
      ▼                           ▼                                    ▼                        ▼
```
"""
