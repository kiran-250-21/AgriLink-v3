"""
Section 4: Feature-by-Feature Code Walkthrough & Implementation Details
"""

def get_content():
    return """# CHAPTER 5: FEATURE-BY-FEATURE CODE WALKTHROUGH & IMPLEMENTATION DETAILS

### 5.1 Feature 1: Multi-Role Authentication & Role-Based Access Control (RBAC)

#### What the Feature Does:
Enables secure user registration, cryptographic login, and stateless session verification across four distinct enterprise roles: `FARMER`, `BUYER`, `DRIVER`, and `ADMIN`. Protects API endpoints against unauthorized access and role impersonation.

#### Files Implementing the Feature:
- `backend/controllers/authController.js` (`registerUser`, `loginUser`, `getMe`)
- `backend/routes/authRoutes.js`
- `backend/middleware/auth.js` (`protect`)
- `backend/middleware/role.js` (`requireRole`)
- `backend/models/User.js`
- `backend/utils/generateToken.js`
- `frontend/src/context/AuthContext.jsx`
- `frontend/src/components/ProtectedRoute.jsx`

#### Key Code Snippet: RBAC Authorization Middleware (`backend/middleware/role.js`)
```javascript
const requireRole = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ message: 'Authentication required' });
    }
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({
        message: `Forbidden: Access restricted to role(s) [${roles.join(', ')}]. Your role is ${req.user.role}.`,
      });
    }
    next();
  };
};
module.exports = { requireRole };
```
*Beginner Explanation*: This higher-order function acts as a security guard at the door of each API route. It checks if the logged-in user possesses one of the allowed roles (e.g., `requireRole('FARMER')`). If an unverified user or a Driver attempts to declare a harvest, the gatekeeper immediately halts execution and returns an HTTP 403 Forbidden status.

#### Realistic Sample Input & Output:
- **Input (POST /api/auth/login)**:
  ```json
  { "email": "kiran@farmer.com", "password": "farmer123" }
  ```
- **Output (HTTP 200 OK)**:
  ```json
  {
    "_id": "67be10a4f10283c842e12a91",
    "name": "Kiran Farmer",
    "email": "kiran@farmer.com",
    "role": "FARMER",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

---

### 5.2 Feature 2: Harvest Declaration & Produce Quality Grading

#### What the Feature Does:
Allows farmers to register harvest batches, including crop name, expected and available mass in kilograms, quality grading (`GRADE_A`, `GRADE_B`, `GRADE_C`), farm location, and expected harvest date. The system automatically geocodes the farm location to latitude/longitude coordinates.

#### Files Implementing the Feature:
- `backend/controllers/harvestController.js` (`createHarvest`, `getMyHarvests`, `getAvailableHarvests`)
- `backend/models/Harvest.js`
- `backend/routes/harvestRoutes.js`
- `backend/utils/calculations.js` (`resolveCoordinates`)
- `frontend/src/pages/farmer/CreateHarvest.jsx`

#### Key Code Snippet: Automatic Spatial Coordinate Resolution (`backend/controllers/harvestController.js`)
```javascript
const coords = resolveCoordinates(farmLocation);
const harvest = await Harvest.create({
  farmerId: req.user._id,
  cropName: cropName.trim(),
  category: category || 'Spices',
  expectedQuantity: Number(expectedQuantity),
  availableQuantity: Number(expectedQuantity),
  unit: unit || 'Kg',
  quality: quality || 'GRADE_A',
  farmLocation,
  latitude: coords ? coords.lat : null,
  longitude: coords ? coords.lng : null,
  expectedHarvestDate: expectedHarvestDate || Date.now(),
  status: 'AVAILABLE',
});
```
*Beginner Explanation*: When a farmer types their village or district name (e.g., "Guntur" or "Tenali"), the backend consults its spatial coordinate registry. It attaches exact GPS coordinates to the harvest record. This enables the recommendation engine to calculate distance without requiring the farmer to manually enter GPS numbers.

---

### 5.3 Feature 3: Market Intelligence & Net Return Engine

#### What the Feature Does:
The analytical centerpiece of AgriLink. Analyzes regional APMC mandi prices and institutional buyer buy offers for a farmer's specific crop, calculates distance-based logistics freight costs, subtracts freight from gross revenue, ranks all options descending by net cash realization, flags the 🏆 **Best Net Return**, and persists a historical snapshot.

#### Files Implementing the Feature:
- `backend/services/recommendationService.js` (`analyzeHarvestOptions`)
- `backend/controllers/recommendationController.js` (`analyzeRecommendation`)
- `backend/utils/calculations.js` (`calculateNetRevenue`, `calculateDistanceKm`, `calculateLogisticsCost`)
- `backend/models/Recommendation.js`
- `frontend/src/pages/farmer/MarketIntelligence.jsx`
- `frontend/src/components/RecommendationCard.jsx`

#### Key Code Snippet: Net Return Calculation Loop (`backend/services/recommendationService.js`)
```javascript
// Evaluate candidate APMC Markets
for (const mp of marketPrices) {
  if (mp.marketId && mp.marketId.active) {
    const destCoords = (mp.marketId.latitude != null && mp.marketId.longitude != null)
      ? { lat: mp.marketId.latitude, lng: mp.marketId.longitude }
      : null;
    const distance = calculateDistanceKm(farmLoc, mp.marketId.location, farmCoords, destCoords);
    const metrics = calculateNetRevenue(mp.pricePerUnit, qty, distance);

    options.push({
      destinationName: mp.marketId.name,
      destinationType: 'MARKET',
      marketId: mp.marketId._id,
      location: mp.marketId.location,
      sellingPrice: mp.pricePerUnit,
      grossRevenue: metrics.grossRevenue,
      estimatedLogisticsCost: metrics.estimatedLogisticsCost,
      estimatedNetRevenue: metrics.estimatedNetRevenue,
      distanceKm: distance,
    });
  }
}
// Sort descending by Estimated Net Revenue
options.sort((a, b) => b.estimatedNetRevenue - a.estimatedNetRevenue);
```

#### Realistic Sample Input & Output:
- **Input (POST /api/recommendations/analyze)**:
  ```json
  { "harvestId": "67be10b0f10283c842e12a95", "quantity": 5000 }
  ```
- **Output (HTTP 200 OK)**:
  ```json
  {
    "harvest": { "cropName": "Chilli", "availableQuantity": 5000, "farmLocation": "Guntur" },
    "recommendedOption": {
      "rank": 1,
      "destinationName": "Buyer: Godavari Agro Processing Ltd",
      "destinationType": "BUYER",
      "sellingPrice": 205,
      "grossRevenue": 1025000,
      "estimatedLogisticsCost": 4100,
      "estimatedNetRevenue": 1020900,
      "distanceKm": 35,
      "isRecommended": true
    },
    "allOptions": [ /* Ranked list of Mandis and Buyers */ ]
  }
  ```

---

### 5.4 Feature 4: Dual Destination Selling Pathways

#### What the Feature Does:
Provides farmers with two distinct, legally structured commercial fulfillment pathways:
1. **Direct APMC Mandi Order**: Immediate lock. The farmer bypasses middlemen and directly books mandi dispatch. The order status is instantly set to `LOGISTICS_REQUIRED`, and a transport job is created.
2. **Buyer Procurement Sale Intent**: The farmer selects an institutional buyer's offer. Because buyers must verify inventory before shipment, an order is created with status `PENDING_BUYER_CONFIRMATION`. The buyer can then Accept or Reject the sale request.

#### Files Implementing the Feature:
- `backend/controllers/orderController.js` (`createOrder`, lines 126–228)
- `backend/models/Order.js`
- `backend/models/Delivery.js`
- `frontend/src/pages/farmer/MarketIntelligence.jsx`
- `frontend/src/pages/buyer/SaleRequests.jsx`

---

### 5.5 Feature 5: Concurrency-Safe Atomic Inventory Engine

#### What the Feature Does:
Guarantees that produce is never oversold or double-allocated, even if dozens of buyers or farmers trigger simultaneous purchase requests on the exact same crop lot.

#### Files Implementing the Feature:
- `backend/controllers/orderController.js` (Lines 58–66, 133–140, 268–280)
- `backend/models/Harvest.js`

#### Key Code Snippet: Atomic Guard Pattern (`backend/controllers/orderController.js`)
```javascript
// Atomic inventory deduction with conditional safety guard
const updatedHarvest = await Harvest.findOneAndUpdate(
  { _id: harvestId, availableQuantity: { $gte: qty } },
  { $inc: { availableQuantity: -qty } },
  { new: true }
);

if (!updatedHarvest) {
  return res.status(400).json({ 
    message: 'Atomic inventory check failed. Quantity no longer available.' 
  });
}

if (updatedHarvest.availableQuantity === 0) updatedHarvest.status = 'SOLD_OUT';
else updatedHarvest.status = 'PARTIALLY_SOLD';
await updatedHarvest.save();
```
*Beginner Explanation*: In standard web code, developers often do: (1) read harvest from DB, (2) check if `qty <= available`, (3) update `available = available - qty`. If two requests hit simultaneously between steps 1 and 3, both read the old quantity and both succeed, causing produce overselling! AgriLink executes the check and the deduction in **a single atomic MongoDB instruction**. The database checks `{ availableQuantity: { $gte: qty } }` and performs `$inc: -qty` simultaneously under a single document lock. The second request immediately fails and receives a clean error message.

---

### 5.6 Feature 6: Driver Logistics Workflow & Dispatch State Machine

#### What the Feature Does:
Enables commercial drivers to browse available agricultural haulage jobs matching their vehicle capacity, accept shipments, and advance an immutable status state machine from pickup to final delivery.

```
┌────────────────────┐      Driver Accepts      ┌────────────────────┐
│ LOGISTICS_REQUIRED │ ───────────────────────> │  DRIVER_ASSIGNED   │
└────────────────────┘                          └─────────┬──────────┘
                                                          │ Driver arrives at farm
                                                          ▼
┌────────────────────┐     Driver leaves farm   ┌────────────────────┐
│     IN_TRANSIT     │ <─────────────────────── │     PICKED_UP      │
└─────────┬──────────┘                          └────────────────────┘
          │ Driver arrives at destination
          ▼
┌────────────────────┐      Buyer verifies      ┌────────────────────┐
│     DELIVERED      │ ───────────────────────> │     COMPLETED      │
└────────────────────┘                          └────────────────────┘
```

#### Files Implementing the Feature:
- `backend/controllers/deliveryController.js` (`getAvailableJobs`, `acceptDeliveryJob`, `updateDeliveryStatus`, `getMyDeliveries`)
- `backend/models/Delivery.js`
- `backend/models/Vehicle.js`
- `backend/routes/deliveryRoutes.js`
- `frontend/src/pages/driver/AvailableJobs.jsx`
- `frontend/src/pages/driver/ActiveDeliveries.jsx`

#### Key Code Snippet: State Machine Transition Guard (`backend/controllers/deliveryController.js`)
```javascript
const validStatuses = [
  'PICKUP_SCHEDULED',
  'PICKED_UP',
  'IN_TRANSIT',
  'DELIVERED',
  'BUYER_CONFIRMED',
  'COMPLETED',
];

if (!validStatuses.includes(status)) {
  return res.status(400).json({ message: 'Invalid delivery status state' });
}

delivery.status = status;
delivery.timeline.push({
  status,
  timestamp: new Date(),
  note: note || `Status updated to ${status}`,
});
await delivery.save();
```

---

### 5.7 Feature 7: In-App Lifecycle Notifications & Audit Logging

#### What the Feature Does:
- **Notifications**: Delivers real-time role-specific alerts when orders are placed, sale intents are accepted or rejected, or drivers are assigned.
- **Audit Logging**: Immutably records every transactional operation (user ID, role, action, target resource, timestamp, and details) to support compliance and dispute resolution.

#### Files Implementing the Feature:
- `backend/services/notificationService.js` (`createNotification`)
- `backend/controllers/notificationController.js`
- `backend/models/Notification.js`
- `backend/models/AuditLog.js`
- `frontend/src/components/Navbar.jsx` (Notification bell)
- `frontend/src/pages/admin/AuditLogs.jsx`

---

### 5.8 Feature 8: Administrative Command Center & Market Rate Management

#### What the Feature Does:
Empowers regulatory administrators to register regional APMC mandis, update official clearing rates, monitor platform analytics (users, harvests, revenue), verify or suspend users, and inspect immutable audit trails.

#### Files Implementing the Feature:
- `backend/controllers/adminController.js` (`getAllUsers`, `updateUserStatus`, `getPlatformAnalytics`, `getAuditLogs`)
- `backend/controllers/marketController.js` (`createMarket`, `updateMarketPrice`)
- `backend/routes/adminRoutes.js`
- `backend/routes/marketRoutes.js`
- `frontend/src/pages/admin/AdminDashboard.jsx`
- `frontend/src/pages/admin/MarketManagement.jsx`
- `frontend/src/pages/admin/UserManagement.jsx`
"""
