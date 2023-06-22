EXTENSION_UUID_DDL = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
"""

# Table names
TABLE_APP_OUTPUT_NAME = "app_output"
TABLE_MAX_PRICE_NAME = "max_price"
TABLE_LIVE_PRICE_NAME = "live_price"
TABLE_LIVE_PRICE_ARCHIVE_NAME = "live_price_archive"

# Table creation DDL
TABLE_MAX_PRICE_DDL = """
CREATE TABLE IF NOT EXISTS max_price (
    uuid UUID PRIMARY KEY,
    max_price DECIMAL NOT NULL DEFAULT 0.00
)
"""

TABLE_APP_OUTPUT_DDL = """
CREATE TABLE IF NOT EXISTS app_output (
    uuid UUID,
    max_price DECIMAL,
    live_price DECIMAL,
    created_at TIMESTAMP
)
"""

TABLE_LIVE_PRICE_DDL = """
CREATE TABLE IF NOT EXISTS live_price (
    id INTEGER,
    uuid UUID,
    price DECIMAL,
    currency VARCHAR(3),
    last_seen TIMESTAMP
)
"""

TABLE_LIVE_PRICE_ARCHIVE_DDL = """
CREATE TABLE IF NOT EXISTS live_price_archive (
    uuid UUID,
    price DECIMAL,
    currency VARCHAR(3),
    last_seen TIMESTAMP
)
"""



