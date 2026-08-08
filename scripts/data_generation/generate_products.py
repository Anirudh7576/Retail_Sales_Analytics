from scripts.common.constants import (PRODUCT_MASTER, PRODUCT_REQUIRED_FIELDS,)
from scripts.data_generation.generate_subcategories import generate_subcategories 

from scripts.common.file_utils import save_json
from scripts.common.validation import (check_required_fields, check_unique)

from faker import Faker
import random

fake = Faker()


def generate_products() -> list:

    subcategories = generate_subcategories()

    subcategory_lookup = {
        subcategory["subcategory_name"]: subcategory["subcategory_id"]
        for subcategory in subcategories
    }

    dim_product = []

    for product_id in range(1001, 10001):

        template = random.choice(PRODUCT_MASTER)

        subcategory_id = subcategory_lookup[
            template["subcategory_name"]
        ]

        product_name = f"{template['product_name']} {fake.unique.random_number(digits=5)}"

        unit_cost = random.randint(500, 100000)

        unit_price = unit_cost + random.randint(500, 30000)

        product_record = {
            "product_id": product_id,
            "subcategory_id": subcategory_id,
            "product_name": product_name,
            "brand": template["brand"],
            "unit_cost": unit_cost,
            "unit_price": unit_price
        }

        dim_product.append(product_record)

    return dim_product

    #============================================================
    # create main
    #============================================================
def main():
    try:
        products = generate_products()

        #Validation
        check_required_fields(
            products,
            PRODUCT_REQUIRED_FIELDS
        )

        check_unique(
            products, 
            'product_id'
        )

        check_unique(
            products,
            'product_name'
        )

        save_json(
            records = products,
            file_prefix = "products"
        )

        print("\nGenerating products file\n")

        for product in products:
            print(product)

        print("\nproduct generation successfully")

    except Exception as error:

        print(f"process failed :{error}")

if __name__ == "__main__":
    main()


