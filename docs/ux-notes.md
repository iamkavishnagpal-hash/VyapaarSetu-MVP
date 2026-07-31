# VyapaarSetu UX Strategy & Design Tokens

This document documents the design system, visual aesthetics, color tokens, and accessibility standards powering the VyapaarSetu user experience.

---

## 1. Visual Aesthetics & Design System Tokens

VyapaarSetu uses a **modern, premium dark-mode aesthetic** built on high-contrast emerald greens, deep slate blues, and warm amber accents to evoke financial trust, operational clarity, and high performance.

### Design Tokens (CSS Variables)

```css
:root {
  /* Brand Core Colors */
  --vs-color-primary: #10B981;        /* Emerald Green (Trust & Growth) */
  --vs-color-primary-dark: #059669;   /* Dark Emerald */
  --vs-color-secondary: #3B82F6;      /* Electric Blue (Technology) */
  --vs-color-accent: #F59E0B;         /* Amber (Escrow Hold & Alerts) */
  --vs-color-danger: #EF4444;         /* Coral Red (Shrinkage & Leakage) */
  
  /* Background & Surface Colors */
  --vs-bg-dark: #0F172A;              /* Slate 900 */
  --vs-bg-surface: #1E293B;           /* Slate 800 */
  --vs-bg-card: rgba(30, 41, 59, 0.7); /* Glassmorphism Card Surface */

  /* Typography */
  --vs-font-heading: 'Outfit', sans-serif;
  --vs-font-body: 'Inter', sans-serif;
  --vs-font-mono: 'JetBrains Mono', monospace;
}
```

---

## 2. UX Guidelines & Micro-Interactions

1. **Clear Mode Gateway**: On initial load, users choose explicitly between **Start**, **Run**, **Sell**, and **Grow** to avoid dashboard clutter.
2. **Instant Visual Feedback**: Escrow status changes feature animated micro-badges (Held = Amber pulse, Released = Emerald checkmark).
3. **No Decorative Placeholders**: All metrics, charts, and table rows display live or realistic demo values with explicit unit labels (INR, %, Days).
