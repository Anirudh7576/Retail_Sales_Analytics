
"""
Central configuration for FMCG transaction data generation.
"""

from datetime import date

# --------------------------------------------------
# TRANSACTION PERIOD
# --------------------------------------------------

TRANSACTION_START_DATE = date(2026, 1, 1)
TRANSACTION_END_DATE = date(2026, 12, 31)

# --------------------------------------------------
# GENERATION VOLUME
# --------------------------------------------------

TARGET_ORDER_COUNT = 100_000

# Reproducible synthetic data generation
RANDOM_SEED = 42

# --------------------------------------------------
# BUSINESS CONFIGURATION
# --------------------------------------------------

CURRENCY_CODE = "INR"

ORDER_STATUSES = [
    "SUBMITTED",
    "CONFIRMED",
    "PARTIALLY_FULFILLED",
    "FULFILLED",
    "CANCELLED",
]

INVOICE_STATUSES = [
    "ISSUED",
    "VOID",
]

# --------------------------------------------------
# IDENTIFIER PREFIXES
# --------------------------------------------------

ORDER_ID_PREFIX = "ORD"
ORDER_ITEM_ID_PREFIX = "OI"
INVOICE_ID_PREFIX = "INV"
SALES_ID_PREFIX = "SAL"

# --------------------------------------------------
# FILE CONFIGURATION
# --------------------------------------------------

TRANSACTION_OUTPUT_DIR = "data/generated/transactions"

TAX_CONFIG_FILE = "data/config/product_tax_rates.json"

# --------------------------------------------------
# INITIAL VALIDATION RULES
# --------------------------------------------------

MIN_ORDER_QUANTITY = 1

# These are initial technical limits, not finalized
# business distributions.
MIN_PRODUCTS_PER_ORDER = 1
MAX_PRODUCTS_PER_ORDER = 5

# Financial rounding precision
CURRENCY_DECIMAL_PLACES = 2



# --------------------------------------------------
# ORDER GENERATION
# --------------------------------------------------

# Safe default for initial testing.
DEFAULT_ORDER_SAMPLE_SIZE = 100

# Initial cancellation rate for synthetic testing.
ORDER_CANCELLATION_RATE = 0.02

# Requested delivery window after order date.
MIN_DELIVERY_DAYS = 1
MAX_DELIVERY_DAYS = 7

# order items

MAX_ORDER_QUANTITY = 24

MIN_DISCOUNT_PCT = 0.00
MAX_DISCOUNT_PCT = 20.00
