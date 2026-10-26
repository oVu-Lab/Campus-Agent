<div align="center">

# 🎓 CampusAgent
### Autonomous AI Negotiation & Automated Campus Marketplace

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google%20gemini&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![PayPal Sandbox](https://img.shields.io/badge/PayPal-003087?style=for-the-badge&logo=paypal&logoColor=white)](https://developer.paypal.com)
[![Zapier](https://img.shields.io/badge/Zapier-FF4A00?style=for-the-badge&logo=zapier&logoColor=white)](https://zapier.com)
[![Render](https://img.shields.io/badge/Render-000000?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](./LICENSE)

---

> **CampusAgent** transforms university secondhand trading by deploying autonomous **Google Gemini AI** agents to negotiate item prices on behalf of student sellers within strict floor-price guardrails, concluding transactions instantly via **PayPal Sandbox** and **Zapier** automation.

</div>

---

## 📸 Key Capabilities & Visual Overview

```text
  [ Student Buyer ]               [ Gemini AI Negotiator ]           [ Seller Dashboard ]
          │                                  │                                │
          ├─── 1. Counter-Offers Price ─────►│                                │
          │                                  ├─── 2. Checks AG Grid Limits ──►│
          │◄── 3. Dynamic Counter/Accept ────┤                                │
          │                                  │                                │
          ├─── 4. Initiates Checkout ───────►│                                │
          │                                  ├─── 5. Creates Payment Link ───► (PayPal Sandbox)
          │                                  │                                │
          │                                  └─── 6. Triggers Deal Webhook ──► (Zapier Alert)

```

---

## 🤖 AI & Technology Stack

| Sponsor / Tool | Tech Role & Implementation Details |
| --- | --- |
| **Google Gemini** | **AI Negotiation Engine:** Processes real-time buyer conversations, evaluating offers dynamically against protected floor prices to counter or accept deals. |
| **AG Grid** | **Interactive Inventory Control:** Powers the Seller Dashboard with an editable, high-performance table to configure live prices and protected margins. |
| **PayPal Sandbox** | **Payment Session Creation:** Generates secure buyer approval links immediately upon agreed negotiations without holding sensitive card data. |
| **Zapier** | **Automated Deal Dispatch:** Emits a `DEAL_FINALIZED` webhook payload (`PAYPAL_CHECKOUT_CREATED`) to dispatch instant seller notifications & receipt logs. |
| **Render** | **Cloud Hosting:** Continuous integration deployment via `render.yaml` Blueprint managing environment secrets securely. |
| **APIMatic** | **API Specification Standard:** Validates structural consistency against OpenAPI 3.0 standards (`openapi.yaml`). |

---

## 🚀 Local Quickstart Guide

### 1. Clone & Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

```

### 2. Configure Environment Secrets

For repeatable local development, create `.streamlit/secrets.toml` *(git-ignored)*:

```toml
GEMINI_API_KEY = "your-gemini-key"
PAYPAL_CLIENT_ID = "your-paypal-id"
PAYPAL_SECRET = "your-paypal-secret"
ZAPIER_WEBHOOK_URL = "your-zapier-url" # Optional

```

### 3. Launch App

```bash
streamlit run APP.py

```
> 💡 **Hackathon Demo Note:** The Zapier webhook is pre-configured to route test notification payloads to the developer's demo inbox, providing an instant end-to-end proof of concept when judges test deal finalization.
---

## ☁️ Render Blueprint Deployment

The repo includes a pre-configured `render.yaml` Blueprint.

1. Connect `Campus-Agent` on **Render**.
2. Set Environment Variables in Render: `GEMINI_API_KEY`, `PAYPAL_CLIENT_ID`, `PAYPAL_SECRET`, `ZAPIER_WEBHOOK_URL`.
3. Render automatically binds to `$PORT` using Streamlit health checks!

---

## 📜 License

Distributed under the **MIT License**. See [`LICENSE`](https://github.com/oVu-Lab/Campus-Agent/blob/main/LICENSE) for full details.

```

```
