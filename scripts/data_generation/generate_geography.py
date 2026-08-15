"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Category Dimension data and validate it.
"""

from scripts.common.constants import (
    GEOGRAPHY_MASTER,
    GEOGRAPHY_REQUIRED_FIELDS
    )
from scripts.common.validation import (
    check_required_fields, 
    check_unique
    )
from scripts.common.file_utils import save_json
from scripts.common.faker_utils import generate_postalcode

from faker import Faker
fake = Faker("en_IN")

# =====================================================================================
# generate geography
# =====================================================================================
def generate_geography():
    dim_geography = []

    for geography_id, location in enumerate(GEOGRAPHY_MASTER, start = 10001):

        geography_record = {
        "geography_id": geography_id,
        "city": location["city"],
        "state": location["state"],
        "country": location["country"],
        "region": location["region"],
        "postal_code": generate_postalcode()
        }

        dim_geography.append(geography_record)

    return dim_geography

# =======================================================================================
# validation
# =======================================================================================

def main():

    try:

        geography = generate_geography()

        check_required_fields(
                geography,
                GEOGRAPHY_REQUIRED_FIELDS
        )

        check_unique(
                geography,
                "geography_id"

        )

        print("\n validating geography data")

        save_json(
            geography,
            file_prefix= "geography",
            folder_type= "generated"
        )
        print("geography file saved")

    except Exception as error:
        if geography is not None:
            save_json(
                geography,
                file_prefix= "geography",
                folder_type= "rejected"
            )

        print(f"Found an error :{error}")

if __name__ == "__main__":
    main()






        

        








