-- ═══════════════════════════════════════════════════════════
-- VYAPAARSETU DATABASE SCHEMA (PostgreSQL)
-- Export-ready for development
-- ═══════════════════════════════════════════════════════════

-- Enable UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ═══════════════════════════════════════════════════════════
-- USERS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20) UNIQUE,
    full_name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    role VARCHAR(50) NOT NULL CHECK (role IN ('entrepreneur', 'store_owner', 'vendor')),
    kyc_status VARCHAR(50) DEFAULT 'pending' CHECK (kyc_status IN ('pending', 'verified', 'rejected')),
    kyc_documents JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_kyc ON users(kyc_status);

-- ═══════════════════════════════════════════════════════════
-- STORES
-- ═══════════════════════════════════════════════════════════
CREATE TABLE stores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    category VARCHAR(100) NOT NULL,
    logo_url TEXT,
    hero_image_url TEXT,
    status VARCHAR(50) DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'sold', 'rented', 'suspended')),
    listing_type VARCHAR(50) CHECK (listing_type IN ('sale', 'rent', 'both')),
    sale_price DECIMAL(12, 2),
    rent_price DECIMAL(10, 2),
    monthly_revenue DECIMAL(10, 2),
    profit_margin DECIMAL(5, 2),
    total_products INTEGER DEFAULT 0,
    avg_order_value DECIMAL(10, 2),
    total_orders INTEGER DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    verification_status VARCHAR(50) DEFAULT 'unverified',
    api_connected BOOLEAN DEFAULT FALSE,
    escrow_protected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_stores_owner ON stores(owner_id);
CREATE INDEX idx_stores_category ON stores(category);
CREATE INDEX idx_stores_status ON stores(status);

-- ═══════════════════════════════════════════════════════════
-- STORE METRICS (Trust Snapshots)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE store_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    store_id UUID REFERENCES stores(id) ON DELETE CASCADE,
    snapshot_date DATE NOT NULL,
    revenue DECIMAL(10, 2),
    orders_count INTEGER,
    avg_order_value DECIMAL(10, 2),
    profit_margin DECIMAL(5, 2),
    data_source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(store_id, snapshot_date)
);

-- ═══════════════════════════════════════════════════════════
-- ESCROW TRANSACTIONS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE escrow_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    store_id UUID REFERENCES stores(id) ON DELETE CASCADE,
    buyer_id UUID REFERENCES users(id),
    amount DECIMAL(12, 2) NOT NULL,
    escrow_type VARCHAR(50) CHECK (escrow_type IN ('purchase', 'rent')),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'held', 'releasing', 'released', 'disputed')),
    buyer_paid_at TIMESTAMP,
    released_70_at TIMESTAMP,
    released_30_at TIMESTAMP,
    holdback_days INTEGER DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_escrow_store ON escrow_transactions(store_id);
CREATE INDEX idx_escrow_buyer ON escrow_transactions(buyer_id);

-- ═══════════════════════════════════════════════════════════
-- WALLETS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE wallets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) UNIQUE ON DELETE CASCADE,
    available_balance DECIMAL(12, 2) DEFAULT 0,
    escrow_balance DECIMAL(12, 2) DEFAULT 0,
    pending_balance DECIMAL(12, 2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- WALLET TRANSACTIONS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE wallet_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    wallet_id UUID REFERENCES wallets(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL CHECK (type IN ('credit', 'debit', 'escrow_hold', 'escrow_release', 'withdraw', 'refund')),
    amount DECIMAL(12, 2) NOT NULL,
    reference_type VARCHAR(100),
    reference_id UUID,
    status VARCHAR(50) DEFAULT 'completed',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- VENDORS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE vendors (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    company_name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    product_count INTEGER DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active',
    verified BOOLEAN DEFAULT FALSE,
    api_integration JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- PRODUCTS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    vendor_id UUID REFERENCES vendors(id) ON DELETE CASCADE,
    store_id UUID REFERENCES stores(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    sku VARCHAR(100) UNIQUE,
    price DECIMAL(10, 2),
    cost_price DECIMAL(10, 2),
    stock_quantity INTEGER DEFAULT 0,
    images JSONB,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- ORDERS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    store_id UUID REFERENCES stores(id) ON DELETE SET NULL,
    vendor_id UUID REFERENCES vendors(id) ON DELETE SET NULL,
    buyer_id UUID REFERENCES users(id),
    order_number VARCHAR(100) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'paid' CHECK (status IN ('paid', 'escrow_held', 'preparing', 'packed', 'shipped', 'delivered', 'cancelled', 'refunded')),
    items JSONB NOT NULL,
    subtotal DECIMAL(10, 2),
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    total DECIMAL(10, 2) NOT NULL,
    escrow_amount DECIMAL(10, 2),
    escrow_released BOOLEAN DEFAULT FALSE,
    shipping_address JSONB,
    buyer_phone VARCHAR(20),
    buyer_name VARCHAR(255),
    courier_name VARCHAR(100),
    tracking_number VARCHAR(100),
    estimated_delivery DATE,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_orders_store ON orders(store_id);
CREATE INDEX idx_orders_vendor ON orders(vendor_id);
CREATE INDEX idx_orders_buyer ON orders(buyer_id);
CREATE INDEX idx_orders_status ON orders(status);

-- ═══════════════════════════════════════════════════════════
-- ORDER TIMELINE
-- ═══════════════════════════════════════════════════════════
CREATE TABLE order_timeline (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID REFERENCES orders(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id)
);

-- ═══════════════════════════════════════════════════════════
-- NOTIFICATIONS
-- ═══════════════════════════════════════════════════════════
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    data JSONB,
    is_read BOOLEAN DEFAULT FALSE,
    action_link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- SAVED STORES (Wishlist)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE saved_stores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    store_id UUID REFERENCES stores(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, store_id)
);

-- ═══════════════════════════════════════════════════════════
-- INQUIRIES
-- ═══════════════════════════════════════════════════════════
CREATE TABLE inquiries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    store_id UUID REFERENCES stores(id) ON DELETE CASCADE,
    buyer_id UUID REFERENCES users(id),
    message TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- AI CONVERSATIONS (MargDarshak)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE ai_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    user_message TEXT NOT NULL,
    ai_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
