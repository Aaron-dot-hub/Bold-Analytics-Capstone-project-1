# 🚀 Bold Analytics Gateway & Telemetry Platform
### Full-Stack B2B Location Data API Engine (All India Dataset)

A centralized, secure, and production-ready SaaS API platform engineered to provide structured, lightning-fast access to All India states, districts, sub-districts, and villages data. This solution features multi-tiered PostgreSQL database normalization, secure API middleware token authentication, a front-end cascading address validation flow, and a live administrative tracking system dashboard.

---

## 📌 Architectural Core Objectives Achieved
1. **Centralized Location Data API Platform:** Built a unified Node.js/Express.js backend cluster that serves as a single source of truth for high-volume geographical datasets.
2. **Normalized & Scalable Database:** Structured flat raw tables into highly indexable relational PostgreSQL tables (`states`, `districts`, `sub_districts`, `villages`) minimizing redundancy.
3. **Secure B2B Client Authentication:** Deployed robust endpoint authorization filtering via custom API Key/Secret validation middleware.
4. **High-Performance Cascade Filtering:** Handled queries efficiently across half a million child/village rows using strict database lookups and query volume constraints (`LIMIT 500`).
5. **Live Administrative Telemetry Hub:** Built an automated monitoring system using high-resolution millisecond tracking (`process.hrtime()`) to store traffic volume and latency.

---

## 📂 System Project Layout
```text
Bold Analytics Capstone project/
├── public/                 # 🌐 Client Interface Web Assets
│   ├── index.html          # Gateway Layout & Telemetry View Panel
│   └── app.js              # Cascade Data Fetches & Metrics Binder
├── server.js               # ⚡ Central Express Backend Core Engine
├── setup_security.py       # 🔒 Database Identity Init Pipeline Script
├── setup_metrics.py        # 📊 Telemetry System Architecture Blueprint
├── test_api.py             # 🔌 API Loopback Diagnostics Script
└── .env                    # 🔑 Encrypted System Environment Bindings




🛠️ Getting Started & Local Execution1. Database ConstructionRun the database architecture scripts to initialize tables and seed your testing api keys:Bashpython setup_security.py
python setup_metrics.py
2. Launch the API Platform EngineStart the Express backend instance. The static client files will automatically be served dynamically:Bashnode server.js
3. Access the Live Platform Dashboard, Open the web browser and navigate directly to:Plaintexthttp://localhost:5000
🔐 API Documentation & EndpointsAll secure API operational data vectors require an authenticated x-api-key sent directly inside the request header pipeline.Endpoint Target RouteMethodHeader SecurityPayload Output/api/v1/locations/statesGETx-api-key RequiredList of all normalized Indian States/api/v1/locations/districts/:state_idGETx-api-key RequiredDistricts scoped under specific State/api/v1/locations/subdistricts/:district_idGETx-api-key RequiredSub-districts / Talukas/api/v1/locations/villages/:sub_district_idGETx-api-key RequiredLocal Villages (Constrained via LIMIT 500)/api/v1/admin/metricsGETPublic RouteReal-time global aggregations & hits📊 Live Metrics & Usage MonitoringThe administrative view panel updates on the fly via isolated non-blocking transactional calculations:Total Handled Requests Counter: Increments dynamically on every interface dropdown mutation select event.Average Database Latency Metrics: Analyzes high-resolution system speed to prevent background data congestion on deep recursive tables.Usage Profiler Grid: Displays database row query patterns grouped by specific client destination route parameters.
---

### 🎉 Project Complete!

This file serves as the complete "proof of work" for evaluation. I have successfully designed and built a full-stack, enterprise-grade system from scratch that implements [database normalization, large dataset handling, secure API design, and a full tracking dashboard](https://workspace.boldanalytics.in/projectsDetail?id=60660b3f-7b37-4fa1-9936-2daf120ec3ab&tab=description). 



