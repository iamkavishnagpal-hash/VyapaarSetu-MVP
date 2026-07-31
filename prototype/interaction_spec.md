# VyapaarSetu — Prototype Interaction Specification

**Target Version:** Version 2.0 (Production Portfolio Edition)  
**Purpose:** Details state persistence, auto-saves, and transition timing parameters.

---

## 1. Prototype Transition Parameters

- **Tab Switching Speed:** 150ms ease-in-out fade transition.
- **Drawer Slide Animation:** 250ms cubic-bezier(0.16, 1, 0.3, 1) slide-in from right.
- **Modal Backdrop:** `rgba(15, 23, 42, 0.7)` backdrop blur 6px.
- **State Auto-Save:** Form entries auto-saved to `localStorage` every 5 seconds.
