# VyapaarSetu Data Flow & Lifecycle Specification

This document details how data moves through the VyapaarSetu system across ingestion, sync, escrow processing, and analytics.

---

## 1. Operational Data Lifecycle

```
[POS / Storefront Webhook Event]
              │
              ▼
    [Kafka Event Ingestion]
              │
    ┌─────────┴─────────┐
    ▼                   ▼
[Redis Cache Update]  [PostgreSQL Transaction Write]
(Stock Lock < 5ms)     (OLTP Ledger Write)
                        │
                        ▼
            [CDC Pipeline (Debezium)]
                        │
                        ▼
            [BigQuery Analytics Warehouse]
                        │
                        ▼
            [Power BI Dashboard Visuals]
```

---

## 2. Ingestion & Sync Mechanics

- **Real-Time POS Counter Sync**: When a physical item is scanned at the store POS, an HTTP POST webhook is dispatched to `/api/v1/inventory/deduct`.
- **Concurrency & Locking**: Redis Distributed Locks (Redlock) ensure that two buyers (one online, one at the POS counter) cannot purchase the last remaining physical SKU simultaneously.
- **Auditing & Analytics Ingestion**: Debezium Change-Data-Capture streams OLTP table mutations to BigQuery every 60 seconds for near real-time BI reporting.
