"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Category Dimension data and validate it.
"""
from scripts.common.constants import (
    PAYMENT_MASTER, 
    PAYMENT_REQUIRED_FIELDS
    )
from scripts.common.validation import (
    check_required_fields, 
    check_unique
    )
from scripts.common.file_utils import save_json

# ======================================================================
# generate payments data
# ======================================================================

def generate_payments() -> list:

    dim_payments = []

    for payment_id, payment in enumerate(PAYMENT_MASTER, start= 100001):

        payment_record = {

            "payment_id" : payment_id,
            "payment_method" : payment["payment_method"],
            "payment_type" : payment["payment_type"]

        }

        dim_payments.append(payment_record)
    return dim_payments

#=====================================================================================
# Validation
#=====================================================================================

def main():
    payments = generate_payments()

    try:

        check_required_fields(
            payments,
            PAYMENT_REQUIRED_FIELDS
            
        )

        check_unique(
            payments,
            "payment_id"
            
        )

        check_unique(
            payments,
            "payment_method"
        )

        for payment in payments:
            print(payment)
            
        save_json(
            payments,
            file_prefix= "payments"
        )

    except Exception as error:
        print(f"Found an error : {error}")

if __name__ == "__main__":
    main()



