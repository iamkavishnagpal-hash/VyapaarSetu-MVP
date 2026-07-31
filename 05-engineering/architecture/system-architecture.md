# VyapaarSetu Technical Architecture Specification

## System Architecture

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
