
"""
Synthetic tax configuration for FMCG transaction testing.

IMPORTANT:
These rates are illustrative test values.
They are NOT verified GST rates or legal tax classifications.
"""

from datetime import date

TAX_EFFECTIVE_START_DATE = date(2026, 1, 1)
TAX_EFFECTIVE_END_DATE = date(2026, 12, 31)

# Synthetic test rates by category ID.
# Replace these with approved product tax classifications
# and rates before using the data for real tax reporting.

CATEGORY_TAX_RATE = {
    1: 5.00,
    2: 12.00,
    3: 18.00,
    4: 28.00,
}

TAX_SOURCE = "SYNTHETIC_TEST_DATA"

MIN_TAX_RATE = 0.00
MAX_TAX_RATE = 100.00
