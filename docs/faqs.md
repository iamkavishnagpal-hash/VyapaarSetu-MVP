# VyapaarSetu — Frequently Asked Questions (FAQs)

**Target Version:** Version 2.0 (Production Portfolio Edition)  

---

## 1. General Business Questions

### Q1: What is VyapaarSetu and who is it built for?
VyapaarSetu is a B2B retail commerce, escrow vault, and analytics platform designed specifically for Indian MSME kiranas, electronics dealers, apparel retailers, and hardware distributors.

### Q2: How does the ICICI trade escrow vault protect buyers and sellers?
When an order is placed, buyer funds are locked securely in an escrow vault. The funds are only released to the seller once the buyer inspects the delivered goods and approves the release (or upon 72-hour inspection window expiry).

---

## 2. Technical & Architecture Questions

### Q3: How are the 10 Python automation engines executed?
All Python scripts in `automation/` are modular CLI utilities with standalone synthetic execution logic. Run `python automation/inventory_sync.py` or `python automation/business_health_engine.py` directly from the command line.

### Q4: Can this repository run against live databases like PostgreSQL or Snowflake?
Yes. The datasets in `data/` map cleanly to ANSI SQL schemas. The 25 SQL queries in `analytics/sql_queries.sql` are standard PostgreSQL 14+ compliant and run seamlessly over DuckDB, Snowflake, or BigQuery.

---

## 3. Security & Compliance Questions

### Q5: How is merchant financial data kept secure?
VyapaarSetu uses role-based access control (RBAC), end-to-end webhook signing, and anonymized merchant health scoring to ensure zero leak of sensitive business data.
