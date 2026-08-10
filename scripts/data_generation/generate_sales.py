from scripts.data_generation.generate_products import generate_products
from scripts.data_generation.generate_customers import generate_customers
from scripts.data_generation.generate_geography import generate_geography
from scripts.data_generation.generate_date_dimension import generate_date_dimension
from scripts.data_generation.generate_payments import generate_payments

from scripts.common.constants import FACT_SALES_REQUIRED_FIELDS
from scripts.common.validation import check_required_fields, check_unique
from scripts.common.file_utils import save_json

import random
from datetime import date

# ==============================================================================
# create dimension data
# ==============================================================================

def generate_sales(number_of_rows:int =  1) -> list:

    customers = generate_customers()
    products = generate_products()
    geographies = generate_geography()
    dates = generate_date_dimension()
    payments = generate_payments()
   
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

        discount_amount = round(
            gross_amount * discount_percentage ,2)

        # example GST/Tax by 18%
        taxable_amount = gross_amount - discount_amount

        tax_amount = round(
            taxable_amount * 0.18, 2
        )

        sales_amount = round(
            taxable_amount + tax_amount
        )

        profit_amount = round(
            taxable_amount - (quantity * unit_cost),
            2
        )

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

def main():

    sales = generate_sales()

    try:

        check_required_fields(
            sales,
            FACT_SALES_REQUIRED_FIELDS
        )

        check_unique(
            sales,
            "sales_key"
        )

        save_json(
            sales,
            file_prefix= "sales"
        )

    except Exception as error:
        print(f"file is not valid: {error}")

if __name__ == "__main__":
    main()

        





