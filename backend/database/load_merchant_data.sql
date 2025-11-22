-- SQL Script to create tables and load CSV data for fraud detection

-- Create merchants table (matching CSV structure EXACTLY)
DROP TABLE IF EXISTS merchant_edges CASCADE;
DROP TABLE IF EXISTS merchants CASCADE;

CREATE TABLE merchants (
    merchant_id VARCHAR(50) PRIMARY KEY,
    is_fraud INTEGER,
    merchant_registration_date TIMESTAMP,
    merchant_category VARCHAR(50),
    business_city VARCHAR(50),
    merchant_tier VARCHAR(20),
    is_kyc_verified NUMERIC,
    pan_hash VARCHAR(100),
    device_id_hash VARCHAR(100),
    ip_hash VARCHAR(100),
    total_txns_90d INTEGER,
    avg_txn_value NUMERIC(10, 2),
    chargeback_rate NUMERIC(5, 4),
    refund_ratio NUMERIC(5, 4),
    merchant_age_days INTEGER,
    total_txns_30d INTEGER,
    total_txns_7d INTEGER,
    avg_txn_value_30d NUMERIC(10, 2),
    median_txn_value_90d NUMERIC(10, 2),
    std_txn_value_90d NUMERIC(10, 2),
    min_txn_value_30d NUMERIC(10, 2),
    max_txn_value_30d NUMERIC(10, 2),
    pct_high_value_txns NUMERIC(5, 4),
    high_value_txns_90d INTEGER,
    high_value_txns_30d INTEGER,
    shared_pan_count INTEGER,
    shared_device_count INTEGER,
    shared_ip_count INTEGER,
    phone_hash VARCHAR(100),
    email_hash VARCHAR(100),
    pos_terminal_id_hash VARCHAR(100),
    shared_phone_count INTEGER,
    shared_email_count INTEGER,
    shared_pos_terminal_count INTEGER,
    emb_0 NUMERIC(10, 8),
    emb_1 NUMERIC(10, 8),
    emb_2 NUMERIC(10, 8),
    emb_3 NUMERIC(10, 8),
    emb_4 NUMERIC(10, 8),
    emb_5 NUMERIC(10, 8),
    emb_6 NUMERIC(10, 8),
    emb_7 NUMERIC(10, 8),
    emb_8 NUMERIC(10, 8),
    emb_9 NUMERIC(10, 8),
    emb_10 NUMERIC(10, 8),
    emb_11 NUMERIC(10, 8),
    emb_12 NUMERIC(10, 8),
    emb_13 NUMERIC(10, 8),
    emb_14 NUMERIC(10, 8),
    emb_15 NUMERIC(10, 8)
);

-- Create indexes for faster queries
CREATE INDEX idx_merchants_is_fraud ON merchants(is_fraud);
CREATE INDEX idx_merchants_tier ON merchants(merchant_tier);
CREATE INDEX idx_merchants_city ON merchants(business_city);
CREATE INDEX idx_merchants_pan ON merchants(pan_hash);

-- Create merchant_edges table (matching CSV structure EXACTLY)
CREATE TABLE merchant_edges (
    id SERIAL PRIMARY KEY,
    merchant_A VARCHAR(50) NOT NULL,
    merchant_B VARCHAR(50) NOT NULL,
    weight NUMERIC(5, 2),
    reason VARCHAR(50),
    FOREIGN KEY (merchant_A) REFERENCES merchants(merchant_id),
    FOREIGN KEY (merchant_B) REFERENCES merchants(merchant_id)
);

-- Create indexes for faster graph queries
CREATE INDEX idx_edges_merchant_a ON merchant_edges(merchant_A);
CREATE INDEX idx_edges_merchant_b ON merchant_edges(merchant_B);
CREATE INDEX idx_edges_ab ON merchant_edges(merchant_A, merchant_B);

-- Add comments
COMMENT ON TABLE merchants IS 'Merchant profile data with fraud labels and embeddings';
COMMENT ON TABLE merchant_edges IS 'Network edges between merchants (shared identifiers)';

-- Instructions for importing in pgAdmin:
-- 1. Right-click on merchants table → Import/Export Data
-- 2. Select merchant_synthetic_100k_phase6.csv
-- 3. Format: csv, Header: YES
-- 4. Click OK
-- 
-- 5. Right-click on merchant_edges table → Import/Export Data
-- 6. Select merchant_edges.csv  
-- 7. Format: csv, Header: YES
-- 8. Click OK
