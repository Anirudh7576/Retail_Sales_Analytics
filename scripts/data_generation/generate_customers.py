from scripts.common.constants import CUSTOMER_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields, 
    check_unique
)
from scripts.common.file_utils import save_json
from scripts.common.faker_utils import generate_phone_number

from faker import Faker
fake = Faker("en_IN")

# ==========================================================================
#  generate customers
# ==========================================================================

def generate_customers() -> list:
    dim_customer = []

    for customer_id in range(50001, 50001 + 10):

        customer_record = {
            "customer_id" : customer_id,
            "first_name"  : fake.first_name(),
            "last_name"   : fake.last_name(),
            "email"       : fake.email(),
            "phone"       : generate_phone_number(),
            "gender"      : fake.random_element(elements= ("Male", "Female")),
            "date_of_birth": fake.date_of_birth(
                minimum_age=18,
                maximum_age= 70).isoformat()
            }
        dim_customer.append(customer_record)

    return dim_customer

# ===============================================================================
# validation
# ===============================================================================

def main():

    customers = generate_customers()

    try:

        check_required_fields(
            customers,
            CUSTOMER_REQUIRED_FIELDS

        )

        check_unique(
            customers,
            "customer_id"
        )

        save_json(
            customers,
            file_prefix = "customers",
            folder_type="generated"
        )

    except Exception as error:
        if customers is not None:

             save_json(
                 customers,
                 file_prefix= "customers",
                 folder_type= "rejected"
             )
             print(f"file not validated because the error is : {error}")

if __name__ == "__main__":
    main()

     