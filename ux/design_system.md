# VyapaarSetu — Design System & Visual Token Specifications

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Outlines design tokens, typography, color palettes, spacing grids, and reusable UI component standards.

---

## 1. Color Tokens & Palette (Sleek Dark / Glassmorphism Theme)

```css
:root {
  /* Primary & Accent Colors */
  --color-brand-primary: #6366f1; /* Emerald / Indigo Electric */
  --color-brand-accent: #10b981;  /* Mint Emerald Success */
  --color-brand-warning: #f59e0b; /* Amber Alert */
  --color-brand-danger: #ef4444;  /* Crimson Defect */

  /* Neutral Surface Colors */
  --bg-surface-main: #0f172a;     /* Deep Slate Background */
  --bg-surface-card: #1e293b;     /* Glass Dark Card */
  --bg-surface-hover: #334155;    /* Hover State */

  /* Text & Border Tokens */
  --text-primary: #f8fafc;        /* High-contrast Pure White */
  --text-secondary: #94a3b8;      /* Slate Muted Text */
  --border-glass: rgba(255, 255, 255, 0.1);
  --shadow-glass: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
```

---

## 2. Typography Hierarchy

- **Primary Font Family:** Inter, system-ui, -apple-system, sans-serif
- **Monospace Font:** JetBrains Mono, Fira Code (For SKU IDs, SQL queries, DAX formulas)
- **Scale:**
  - `Display H1`: 32px / Line Height 40px / Bold 700
  - `Header H2`: 24px / Line Height 32px / SemiBold 600
  - `Section H3`: 18px / Line Height 26px / Medium 500
  - `Body Text`: 14px / Line Height 20px / Regular 400
  - `Caption / Badge`: 12px / Line Height 16px / SemiBold 600

---

## 3. UI Component Standards

- **Metric KPI Card:** Dark glass container (`backdrop-filter: blur(12px)`), 1px subtle white border, prominent numeric value, small sparkline or percentage pill tag.
- **Data Table:** Sticky header row, zebra striping on hover, inline status pill badges (Green = Active/Delivered, Yellow = Pending/In-Inspection, Red = Disputed/Stockout).
- **Buttons:**
  - `Primary CTA`: Gradient background (`#6366f1` to `#4f46e5`), hover glow effect.
  - `Secondary Action`: Outlined glass border with subtle background hover fill.
