from faker import Faker
import random

fake = Faker("en_IN")

# ==============================================
# generate postal code for generate_geography.py
# ==============================================
def generate_postalcode() -> str:
    return f"5{random.randint(10000,99999)}"

# ==============================================
# generate phone number for generate_customers.py
# ==============================================
def generate_phone_number() -> str:
    return fake.numerify("##########")
