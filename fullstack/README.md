# AgriLink Full-Stack Application

This directory contains the production-ready full-stack web application for **AgriLink: An Empirical, Logistics-Aware Decision Framework for Agricultural Wholesale Market Selection and Supply Chain Optimization**.

---

## 📁 Architecture Overview

```
fullstack/
├── backend/                  # Node.js & Express REST API Server
│   ├── config/               # Database connection (MongoDB / Mongoose)
│   ├── controllers/          # Business logic (Auth, Harvest, Market, Orders, Transporter)
│   ├── middleware/           # JWT auth, role validation, error handlers
│   ├── models/               # Mongoose schemas (User, Harvest, Market, Order, Transporter)
│   ├── routes/               # API endpoints (/api/auth, /api/markets, /api/harvests, etc.)
│   ├── services/             # Spatial recommendation & linear optimization engine
│   ├── utils/                # Geodesic Haversine math, circuity factor (Cf=1.28), seed script
│   ├── server.js             # Application entry point
│   ├── package.json          # Node dependencies
│   └── .env                  # Environment variables
│
└── frontend/                 # React 19 + Vite 6 + TailwindCSS Single-Page Application
    ├── src/
    │   ├── components/       # Reusable UI widgets, navigation, role guards
    │   ├── context/          # React authentication & user context
    │   ├── pages/            # Role dashboards (Farmer, Buyer, Driver, FPO, Admin)
    │   ├── services/         # Axios REST client with interceptors
    │   └── data/             # Static APMC coordinates & crop archetypes
    ├── public/               # Static assets & SVG icons
    ├── index.html            # HTML template
    ├── vite.config.js        # Vite config with API proxy
    └── package.json          # Frontend dependencies
```

---

## 🚀 Quickstart Guide

### 1. Start the Backend API Server
```bash
cd backend

# Install dependencies
npm install

# (Optional) Seed realistic APMC markets and initial demo users
npm run seed

# Run in development mode (auto-reload on save)
npm run dev

# Or run in production mode
npm start
```
* Backend runs by default at `http://localhost:5000`
* Health check: `http://localhost:5000/api/health`

### 2. Start the Frontend Client
```bash
cd frontend

# Install dependencies
npm install

# Launch Vite dev server
npm run dev
```
* Frontend runs at `http://localhost:3000`
* Vite automatically proxies all `/api` calls to `http://localhost:5000`.

---

## 🔑 Role Accounts & Features

| Role | Access URL | Core Features |
|---|---|---|
| **Farmer** | `/farmer/dashboard` | Harvest consignment parcel entry, real-time spatial mandi ranking, net realization calculator, transporter booking |
| **Buyer** | `/buyer/dashboard` | Wholesale procurement orders, mandi price discovery, delivery tracking |
| **Driver** | `/driver/dashboard` | Consignment trip matching, route circuity details, backhaul capacity filling |
| **FPO Admin**| `/fpo/dashboard` | Multi-farmer dispatch aggregation, cooperative freight pooling, bulk haul optimization |
| **Platform Admin** | `/admin/markets` | AGMARKNET market coordinate management, statutory cess/hamali fee updates |

---

## 🌐 Cloud Deployment (Render)
The repository root contains `render.yaml` pre-configured to deploy:
- **Backend Service**: Node.js web service running `node server.js` from `fullstack/backend`.
- **Frontend Site**: Static web application running `npm run build` from `fullstack/frontend`.
