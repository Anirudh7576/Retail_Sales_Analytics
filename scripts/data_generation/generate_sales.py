"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Sales fact data and validate it.
"""
# from scripts.data_generation.generate_products import generate_products
# from scripts.data_generation.generate_customers import generate_customers
# from scripts.data_generation.generate_geography import generate_geography
# from scripts.data_generation.generate_date_dimension import generate_date_dimension
# from scripts.data_generation.generate_payments import generate_payments

from scripts.common.constants import FACT_SALES_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields, 
    check_unique,
    check_foreign_keys
)
from scripts.common.file_utils import (
    save_json, 
    get_latest_json
)

from scripts.common.business_rules import (
    check_sales_business_rules, 
    check_sales_calculations
)

from scripts.common.logger import logger 

import random
from datetime import date

    # =============================================================================
    # load dimension data
    # =============================================================================
def load_dimension_data():
    customers = get_latest_json(
                "customers",
                "customers"
            )

    products = get_latest_json(
                "products",
                "products"
            )

    geographies = get_latest_json(
                "geography",
                "geography"
            )

    dates = get_latest_json(
                "dates",
                "dates"
            )

    payments = get_latest_json(
                "payments",
                "payments"
            )

    return {
        "customers"  : customers,
        "products"   : products,
        "geographies" : geographies,
        "dates"      : dates,
        "payments"   : payments
    }
    # ==============================================================================
    # create dimension data
    # ==============================================================================

def generate_sales(dimensions: str, number_of_rows:int) -> list:
    # =======================================================================
    # load latest dimensions
    # =======================================================================

    customers   = dimensions["customers"]
    products    = dimensions["products"]
    geographies = dimensions["geographies"]
    dates       = dimensions["dates"]
    payments    = dimensions["payments"]
    
    # =========================================================================
    # create lookup data
    # =========================================================================

    customer_ids = [
            customer["customer_id"]
            for customer in customers
    ]

    product_records = products

    geography_ids = [
        geography["geography_id"]
        for geography in geographies
    ]

    payments_ids = [
        payment["payment_id"]
        for payment in payments
    ]

    date_ids = [
        date["date_id"]
        for date in dates
    ]

    # =========================================================
    # generate fact records
    # =========================================================

    fact_sales = []

    for sales_key in range(1, number_of_rows + 1):

        # select  a product
        product = random.choice(product_records)
        quantity = random.randint(1,5)
        unit_price = product["unit_price"]
        unit_cost = product["unit_cost"]

        # Discount between 0% to 15%
        discount_percentage = random.uniform(0, 0.15)
        gross_amount = quantity * unit_price

        discount_amount = gross_amount * discount_percentage 

        # example GST/Tax by 18%
        taxable_amount = gross_amount - discount_amount

        tax_amount = taxable_amount * 0.18
        

        sales_amount = taxable_amount + tax_amount

        profit_amount = taxable_amount - (quantity * unit_cost)

        sales_record = {

            "sales_key"      : f"SALE{sales_key}",
            "order_id"       : f"ORD{sales_key:06d}",
            "customer_id"    : random.choice(customer_ids),
            "product_id"     : product["product_id"],
            "geography_id"   : random.choice(geography_ids),
            "payment_id"     : random.choice(payments_ids),
            "date_id"        : random.choice(date_ids),
            "quantity"       : quantity,
            "unit_price"     : unit_price,
            "unit_cost"      : unit_cost,
            "discount_amount": discount_amount,
            "tax_amount"     : tax_amount,
            "sales_amount"   : sales_amount,
            "profit_amount"  : profit_amount

        }

        fact_sales.append(sales_record)

    return fact_sales

# ==========================================================
# Validate FACT_SALES
# ==========================================================

def validate_sales(
    fact_sales: list,
    dimensions: dict
) -> bool:

    """
    Validate FACT_SALES records.
    """

    # ------------------------------------------------------
    # Required fields
    # ------------------------------------------------------

    check_required_fields(
        fact_sales,
        FACT_SALES_REQUIRED_FIELDS
    )

    # ------------------------------------------------------
    # Unique fields
    # ------------------------------------------------------

    check_unique(
        fact_sales,
        "sales_key"
    )

    check_unique(
        fact_sales,
        "order_id"
    )

    # ------------------------------------------------------
    # Foreign keys
    # ------------------------------------------------------

    check_foreign_keys(
        fact_sales,
        "customer_id",
        dimensions["customers"],
        "customer_id"
    )

    check_foreign_keys(
        fact_sales,
        "product_id",
        dimensions["products"],
        "product_id"
    )

    check_foreign_keys(
        fact_sales,
        "geography_id",
        dimensions["geographies"],
        "geography_id"
    )

    check_foreign_keys(
        fact_sales,
        "payment_id",
        dimensions["payments"],
        "payment_id"
    )

    check_foreign_keys(
        fact_sales,
        "date_id",
        dimensions["dates"],
        "date_id"
    )

    return True

# ==========================================================
# Main
# ==========================================================

def main():

    print("\n FACT_SALES generation started")

    fact_sales = []

    try:

        logger.info(
            "FACT_SALES generation started..."
            )
        

        # Load dimensions
        dimensions = load_dimension_data()

        # Generate fact data
        fact_sales = generate_sales(
            dimensions,
            number_of_rows= 10

        )

        # Validate
        validate_sales(
            fact_sales,
            dimensions
        )

        check_sales_business_rules(
            fact_sales
        )

        check_sales_calculations(
            fact_sales
        )

        # Save
        save_json(
            fact_sales,
            "sales",
            "generated"
        )

        logger.info("FACT_SALES saved successfully")

    except Exception as error:
        logger.exception(
            f"\nFACT_SALES process failed: {error}"
        )

        # --------------------------------------------------
        # Save rejected data ONLY if generation succeeded
        # --------------------------------------------------

        if fact_sales is not None:
            save_json(
                fact_sales,
                "sales",
                "rejected")


            logger.info(
                f"\nFACT_SALES process failed: "
                f"{error}"
            )

if __name__ == "__main__":
    main()