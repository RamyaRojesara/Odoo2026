# TransitOps - Enterprise Fleet & Dispatch Management

![Odoo 18/19 Compatible](https://img.shields.io/badge/Odoo-18%20%7C%2019-714B67?style=flat-square&logo=odoo&logoColor=white)
![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![OWL Framework](https://img.shields.io/badge/Frontend-OWL%20Client%20Actions-00A98F?style=flat-square)

**TransitOps** is a comprehensive, production-ready Odoo suite designed for modern transport and fleet management. Built specifically for Odoo 18/19, this project completely bypasses standard Odoo views in favor of highly optimized, custom-built **OWL (Odoo Web Library)** Client Actions.

## 🚀 Key Features

* **Custom OWL Architecture**: Every module runs as a full-page Client Action. No generic Odoo tree/form views. We built a pixel-perfect, dark-themed UI that is blazing fast.
* **State Machine & Locking**: 
  * Vehicles are locked out of dispatch if they are under maintenance.
  * Drivers cannot be dispatched if their licenses are expired.
* **Role-Based Access Control (RBAC)**: Custom authentication controller allowing users to select their specific role (Admin, Dispatcher, Safety Officer, Technician) right from the login screen.
* **Optimized RPC Payloads**: Python controllers return specifically crafted JSON payloads, heavily reducing the frontend rendering time and database querying overhead.

## 📦 Modules

The system is broken down into 6 core modules, demonstrating excellent decoupling and architectural design:

1. `transitops_auth`: Custom RBAC, Session Management, and Login UI.
2. `transitops_dashboard`: Global KPI Dashboard using Chart.js for real-time visualization.
3. `transitops_vehicle`: Fleet registry, capacity tracking, and status state machine.
4. `transitops_driver`: Driver profiles, safety scores, and compliance/license tracking.
5. `transitops_trip`: The core dispatch engine orchestrating drivers and vehicles.
6. `transitops_maintenance`: Service logging, cost tracking, and vehicle lockout integration.

## 🎨 UI / UX Design

We prioritized a **Premium, Dark-Themed Aesthetic**:
* Deep background colors (`#111827`, `#1f2937`) with vibrant accent colors (`#3b82f6` for actions, `#10b981` for success, `#ef4444` for alerts).
* Glassmorphism effects and modern typography.
* Seamless single-page application (SPA) feel within the Odoo ecosystem.

## 🛠️ Installation & Deployment

Since TransitOps overrides standard Odoo behaviors with custom Client Actions, it must be installed directly into the Odoo server's `addons` directory.

### Windows (Local Odoo 19 Installation)
1. Ensure your Odoo service (`odoo-server-19.0`) is installed.
2. Run the provided PowerShell script as **Administrator**:
   ```powershell
   .\install_to_odoo.ps1
   ```
   *(This script stops the Odoo service, copies the TransitOps modules to `C:\Program Files\Odoo 19.0.xxxx\server\odoo\addons`, and restarts the service).*
3. Open Odoo in your browser (`http://localhost:8069`), enable **Developer Mode**, and click **Update Apps List**.
4. Search for `TransitOps` and click **Install**.

## 💻 Tech Stack
- **Backend**: Python 3.12, Odoo ORM, PostgreSQL.
- **Frontend**: OWL (Odoo Web Library), XML, SCSS, Vanilla JS.
- **Visualization**: Chart.js.

---
*Built for the 2026 Odoo Hackathon.*
