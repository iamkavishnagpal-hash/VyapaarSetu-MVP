# VyapaarSetu Technical Architecture Specification

## 1. System Context & Overview

VyapaarSetu is engineered as a modular microservices platform designed for high availability, transactional security, low-latency inventory syncing, and analytics isolation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CLIENT INTERFACE LAYER                            │
│           Web App (Next.js/React)  │  Mobile App  │  POS Terminal           │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ HTTPS / WebSockets / gRPC
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       API GATEWAY & AUTHENTICATION                           │
│             Kong / NGINX Gateway  │  JWT Auth & OAuth 2.0  │ Rate Limiting    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
      ┌────────────────────────────┼────────────────────────────┐
      ▼                            ▼                            ▼
┌──────────────┐            ┌──────────────┐            ┌──────────────┐
│  AI ADVISOR  │            │  INVENTORY   │            │  ESCROW      │
│   SERVICE    │            │ SYNC ENGINE  │            │ WALLET ENGINE│
│ (Python/Fast)│            │ (Node.js/Go) │            │ (Rust/Node)  │
└──────┬───────┘            └──────┬───────┘            └──────┬───────┘
       │                           │                           │
       ▼                           ▼                           ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       EVENT BUS & PERSISTENCE LAYER                         │
│   Apache Kafka Event Streams  │  PostgreSQL (Primary OLTP)  │  Redis Cache  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │ Read Replicas / CDC
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ANALYTICS & REPORTING ENGINE                          │
│         Google BigQuery / Snowflake OLAP  │  Power BI Report Suite          │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Component Layer Responsibilities

1. **Client Interface Layer**: Responsive web and mobile frontends for merchants, suppliers, and buyers; lightweight POS client integration.
2. **API Gateway & Auth**: Enforces TLS 1.3 encryption, OAuth 2.0 merchant auth, and rate-limiting to prevent DDoS on inventory webhooks.
3. **Microservices Domain Core**:
   - `AI Advisor Service`: Processes merchant queries, evaluates capital splits, and runs heuristic growth engines.
   - `Inventory Sync Engine`: Receives real-time POS and Shopify webhooks; updates Redis inventory locks.
   - `Escrow Wallet Engine`: Manages multi-sig financial escrow locks, hold dates, and release milestone triggers.
4. **Event Bus & Storage Layer**: Kafka event streams broadcast `ORDER_CREATED`, `POS_SALE_RECORDED`, and `SHIPMENT_DISPATCHED` events. PostgreSQL serves transactional storage.
5. **Analytics OLAP Layer**: Change-Data-Capture (CDC) feeds PostgreSQL transactions into BigQuery/Snowflake for Power BI dashboard processing.
