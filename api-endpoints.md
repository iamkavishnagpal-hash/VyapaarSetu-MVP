# VyapaarSetu API Documentation

## Base URL
```
https://api.vyapaarsetu.com/v1
```

## Authentication
```http
Authorization: Bearer <JWT_TOKEN>
```

---

## 1. Auth

### POST /auth/signup
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "Kavish Shah",
  "phone": "+919876543210",
  "role": "entrepreneur"
}
```

### POST /auth/login
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

### POST /auth/refresh
```json
{
  "refresh_token": "..."
}
```

### GET /auth/me
Returns current user profile

### PATCH /auth/role
```json
{
  "role": "store_owner" // entrepreneur | store_owner | vendor
}
```

---

## 2. Users

### GET /users/:id
Get user profile

### PATCH /users/:id
```json
{
  "full_name": "Updated Name",
  "avatar_url": "https://..."
}
```

### POST /users/:id/kyc
```json
{
  "document_type": "aadhar",
  "document_url": "https://...",
  "document_number": "XXXX-XXXX-XXXX"
}
```

---

## 3. Stores

### GET /stores
```json
{
  "category": "fashion",
  "listing_type": "sale", // sale | rent | both
  "min_price": 50000,
  "max_price": 500000,
  "rating": 4.0,
  "search": "fashion",
  "page": 1,
  "limit": 20
}
```

### GET /stores/:id
Returns store details with metrics

### POST /stores
```json
{
  "name": "My Fashion Store",
  "description": "Premium fashion store",
  "category": "fashion",
  "listing_type": "sale",
  "sale_price": 250000,
  "rent_price": 5000,
  "monthly_revenue": 85000,
  "profit_margin": 32,
  "total_products": 1247,
  "avg_order_value": 1200
}
```

### PATCH /stores/:id
```json
{
  "name": "Updated Name",
  "status": "active"
}
```

### DELETE /stores/:id

### GET /stores/:id/metrics
Store performance snapshots

### POST /stores/:id/verify
Request verification

---

## 4. Market

### GET /market/featured
Featured stores for homepage

### GET /market/search
Search stores with filters

### GET /market/categories
All available categories

---

## 5. Escrow

### POST /escrow/create
```json
{
  "store_id": "uuid",
  "amount": 250000,
  "type": "purchase" // purchase | rent
}
```

### GET /escrow/:id
Escrow status and details

### POST /escrow/:id/release
```json
{
  "percentage": 70 // 70 or 30
}
```

### POST /escrow/:id/dispute
```json
{
  "reason": "Store not as described",
  "description": "..."
}
```

---

## 6. Wallet

### GET /wallet
```json
{
  "available_balance": 125000,
  "escrow_balance": 45000,
  "pending_balance": 12500
}
```

### GET /wallet/transactions
```json
{
  "type": "credit", // credit | debit
  "page": 1,
  "limit": 20
}
```

### POST /wallet/withdraw
```json
{
  "amount": 50000,
  "bank_account_id": "uuid"
}
```

### POST /wallet/topup
```json
{
  "amount": 50000,
  "payment_method_id": "razorpay"
}
```

### GET /wallet/ escrow
Escrow balance breakdown

---

## 7. Orders

### GET /orders
```json
{
  "status": "paid", // paid | preparing | packed | shipped | delivered
  "vendor_id": "uuid",
  "store_id": "uuid",
  "page": 1,
  "limit": 20
}
```

### GET /orders/:id
Order details with timeline

### POST /orders
```json
{
  "store_id": "uuid",
  "items": [
    {
      "product_id": "uuid",
      "quantity": 2,
      "price": 850
    }
  ],
  "shipping_address": {
    "address": "Flat 204, Tower A",
    "city": "Gurgaon",
    "state": "Haryana",
    "pincode": "122002"
  }
}
```

### PATCH /orders/:id/status
```json
{
  "status": "preparing", // paid → preparing → packed → shipped → delivered
  "note": "Order being prepared"
}
```

### GET /orders/:id/tracking
```json
{
  "courier": "Delhivery",
  "tracking_number": "DL123456789",
  "current_status": "In Transit",
  "estimated_delivery": "2026-04-25"
}
```

---

## 8. Products

### GET /products
```json
{
  "vendor_id": "uuid",
  "category": "fashion",
  "search": "shirt",
  "page": 1,
  "limit": 20
}
```

### GET /products/:id

### POST /products
```json
{
  "name": "Classic White Shirt",
  "description": "Premium cotton",
  "category": "fashion",
  "SKU": "SHIRT-WHT-001",
  "price": 850,
  "cost_price": 400,
  "stock_quantity": 100
}
```

### PATCH /products/:id
```json
{
  "price": 900,
  "stock_quantity": 50
}
```

### DELETE /products/:id

---

## 9. Vendors

### GET /vendors
```json
{
  "category": "fashion",
  "verified": true
}
```

### GET /vendors/:id
Vendor profile and products

### POST /vendors/connect
```json
{
  "vendor_id": "uuid",
  "store_id": "uuid"
}
```

---

## 10. Notifications

### GET /notifications
```json
{
  "is_read": false,
  "type": "order", // order | stock | payment
  "page": 1,
  "limit": 20
}
```

### PATCH /notifications/:id/read

### DELETE /notifications/:id

---

## 11. Saved Stores

### GET /saved-stores
User's saved stores

### POST /saved-stores
```json
{
  "store_id": "uuid"
}
```

### DELETE /saved-stores/:store_id

---

## 12. Inquiries

### GET /inquiries
```json
{
  "store_id": "uuid",
  "status": "active" // active | responded | closed
}
```

### POST /inquiries
```json
{
  "store_id": "uuid",
  "message": "Interested in this store"
}
```

### POST /inquiries/:id/respond
```json
{
  "response": "Thank you for your interest..."
}
```

---

## 13. AI (MargDarshak)

### POST /ai/chat
```json
{
  "message": "Best stores under 1 lakh"
}
```

### GET /ai/suggestions
Returns suggested prompts

---

## 14. Reviews

### GET /stores/:id/reviews
```json
{
  "rating": 4, // filter by rating
  "page": 1
}
```

### POST /stores/:id/reviews
```json
{
  "rating": 5,
  "comment": "Great store, smooth transfer!"
}
```

---

## Response Format

### Success
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

### Error
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [...]
  }
}
```

---

## Common Error Codes

| Code | Description |
|------|------------|
| UNAUTHORIZED | Invalid or missing token |
| FORBIDDEN | Access denied |
| NOT_FOUND | Resource not found |
| VALIDATION_ERROR | Invalid input |
| RATE_LIMIT | Too many requests |
| ESCROW_DISPUTE | Escrow under dispute |
| VERIFICATION_PENDING | KYC not verified |