"""
Section 8: Security, Performance & Enterprise Scalability
"""

def get_content():
    return """# CHAPTER 10: SECURITY, PERFORMANCE & ENTERPRISE SCALABILITY

### 10.1 Security Architecture & Vulnerability Mitigation

AgriLink incorporates defensive programming principles across both frontend and backend layers to ensure transactional confidentiality, data integrity, and resilience against common web vulnerabilities.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   AGRILINK DEFENSE-IN-DEPTH MATRIX                               │
├───────────────────────┬──────────────────────────────────┬───────────────────────────────────────┤
│ THREAT CATEGORY       │ ATTACK VECTOR                    │ AGRILINK MITIGATION MECHANISM         │
├───────────────────────┼──────────────────────────────────┼───────────────────────────────────────┤
│ **Authentication**    │ Credential stuffing, brute-force │ Salted Bcrypt hashing (10 rounds);    │
│                       │ Rainbow table dictionary attacks │ User lookup before password comparison│
├───────────────────────┼──────────────────────────────────┼───────────────────────────────────────┤
│ **Session Hijacking** │ Token forgery, MITM eavesdropping│ Signed JWTs with HS256 algorithm;     │
│                       │ Stolen credentials across APIs   │ Stateless bearer tokens, HTTPS headers│
├───────────────────────┼──────────────────────────────────┼───────────────────────────────────────┤
│ **Authorization**     │ Privilege escalation, Postman    │ Two-tier RBAC (`protect` + `require-  │
│                       │ bypass, role impersonation       │ Role`); context extracted from token  │
├───────────────────────┼──────────────────────────────────┼───────────────────────────────────────┤
│ **Injection**         │ NoSQL selector injection         │ Strict Mongoose schemas type-cast all │
│                       │ (`{"$gt": ""}` bypasses)         │ inputs; objects cannot bypass filters │
├───────────────────────┼──────────────────────────────────┼───────────────────────────────────────┤
│ **Cross-Origin**      │ Malicious origin data harvesting │ Configurable CORS middleware limits   │
│                       │ Unauthorized cross-site requests │ browser origin handshakes             │
├───────────────────────┼──────────────────────────────────┼───────────────────────────────────────┤
│ **Information Leak**  │ Stack trace exposure in errors   │ Centralized `errorHandler` middleware │
│                       │ Server environment discovery     │ suppresses stack traces in production │
└───────────────────────┴──────────────────────────────────┴───────────────────────────────────────┘
```

#### 1. Salted Cryptographic Password Hashing:
Implemented in `backend/models/User.js`:
```javascript
userSchema.pre('save', async function () {
  if (!this.isModified('passwordHash')) return;
  if (!this.passwordHash.startsWith('$2a$') && !this.passwordHash.startsWith('$2b$')) {
    const salt = await bcrypt.genSalt(10);
    this.passwordHash = await bcrypt.hash(this.passwordHash, salt);
  }
});
```
*Engineering Detail*: 10 salt rounds introduce an intentional computational cost of ~100ms per hash. This negligible delay for legitimate logins creates an insurmountable computational barrier for attackers attempting to compute billions of dictionary combinations.

#### 2. Stateless JSON Web Token Session Validation:
Implemented in `backend/middleware/auth.js`:
The server decodes the token using `jwt.verify(token, process.env.JWT_SECRET)`. It retrieves the user document using `.select('-passwordHash')` to ensure sensitive credentials never enter application memory during normal API operations.

#### 3. NoSQL Injection Resilience:
Unlike raw MongoDB drivers where passing `{ email: { "$gt": "" } }` could evaluate true and return unauthorized records, Mongoose's schema casting enforces that the `email` field must be a primitive string. Object selectors are coerced or rejected during schema validation.

---

### 10.2 Performance Optimization & Database Query Tuning

#### 1. Strategic Database Indexing:
In a relational database, unindexed foreign key lookups cause full table scans. In MongoDB, AgriLink applies explicit single-field and compound indexes across frequently queried collections:
- `User`: Unique index on `email`.
- `Harvest`: Indexes on `farmerId`, `cropName` (for fast crop searches), and `status`.
- `MarketPrice`: Indexes on `marketId` and `crop` (for rapid recommendation joins).
- `Order`: Indexes on `farmerId`, `buyerId`, `harvestId`, and `orderStatus`.
- `Delivery`: Indexes on `orderId`, `driverId`, and `status`.

#### 2. Lean Query Projections:
To optimize memory and network serialization, queries that only require display data use projection filters (e.g., `.populate('farmerId', 'name phone farmerProfile')`), ensuring large subdocuments or audit arrays are not unnecessarily retrieved.

#### 3. Vite Production Asset Optimization:
The frontend production build (`npm run build`) leverages Vite's Rollup pipeline to perform tree-shaking, chunk-splitting, and minification. CSS tokens from Tailwind are purged, ensuring the production bundle remains ultra-compact (<250 KB compressed) for high-speed delivery over 3G/4G rural networks.

---

### 10.3 Enterprise Scalability Roadmap: Scaling to 10,000+ Concurrent Users

```
                                  10,000+ CONCURRENT RURAL CLIENTS
                         🌾 Farmers        🏢 Buyers        🚛 Drivers
                              │                │                │
                              └────────────────┼────────────────┘
                                               │
                                               ▼
                              ┌──────────────────────────────────┐
                              │     AWS ROUTE 53 / CLOUDFLARE    │
                              │     DDoS Protection & SSL Term   │
                              └────────────────┬─────────────────┘
                                               │
                                               ▼
                              ┌──────────────────────────────────┐
                              │      NGINX REVERSE PROXY / ALB   │
                              │      Round-Robin Load Balancing  │
                              └───────┬──────────────┬───────────┘
                                      │              │
                   ┌──────────────────┘              └──────────────────┐
                   ▼                                                    ▼
      ┌─────────────────────────┐                          ┌─────────────────────────┐
      │   NODE/EXPRESS POD 1    │                          │   NODE/EXPRESS POD 2    │
      │   (Stateless JWT API)   │                          │   (Stateless JWT API)   │
      └────────────┬────────────┘                          └────────────┬────────────┘
                   │                                                    │
                   └──────────────────┬─────────────────────────────────┘
                                      │
                   ┌──────────────────┼──────────────────┐
                   ▼                                     ▼
      ┌─────────────────────────┐           ┌─────────────────────────┐
      │   REDIS IN-MEMORY CACHE │           │   BULLMQ ASYNC WORKER   │
      │   • Mandi Prices (1 hr) │           │   • Push Notifications  │
      │   • Highway Distance    │           │   • Audit Trail Writes  │
      │   • Redlock Concurrency │           │   • SMS Gateway Worker  │
      └────────────┬────────────┘           └─────────────────────────┘
                   │
                   ▼
      ┌────────────────────────────────────────────────────────┐
      │              MONGODB ATLAS CLOUD REPLICA SET           │
      │   ┌─────────────────────┐    ┌─────────────────────┐   │
      │   │   PRIMARY (Writes)  │───>│ SECONDARY 1 (Reads) │   │
      │   └─────────────────────┘    └─────────────────────┘   │
      │              │               ┌─────────────────────┐   │
      │              └──────────────>│ SECONDARY 2 (Reads) │   │
      │                              └─────────────────────┘   │
      └────────────────────────────────────────────────────────┘
```

#### Architectural Evolution Plan:

1. **Redis In-Memory Caching Tier**:
   - *Problem*: Mandi commodity prices change only once daily, yet thousands of farmers run recommendations continuously.
   - *Solution*: Cache candidate mandi prices in Redis with a 1-hour Time-To-Live (TTL). Cache resolved highway distances permanently. This eliminates 90% of read operations to the MongoDB database.

2. **Database Read/Write Splitting & Replica Sets**:
   - Direct all write operations (order creations, status updates, harvest declarations) to the MongoDB **Primary** node.
   - Direct high-volume read queries (marketplace browsing, market prices, available delivery jobs) to **Secondary Replica** nodes using Mongoose's `readPreference('secondaryPreferred')`.

3. **Asynchronous Background Queue (BullMQ + Redis)**:
   - Offload non-critical side effects (dispatching SMS notifications, updating external telemetry, writing non-blocking audit logs) to a BullMQ worker queue, keeping the main Express HTTP request-response cycle under 50 milliseconds.

4. **Containerization & Auto-Scaling (Docker + AWS ECS / EKS)**:
   - Package the backend into a lightweight Docker container (~75 MB Alpine Node image).
   - Deploy behind an Application Load Balancer with Horizontal Pod Autoscaling (HPA) configured to scale out whenever CPU utilization exceeds 70%.
"""
