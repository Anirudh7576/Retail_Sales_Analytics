from faker import Faker
import random

fake = Faker("en_IN")

def generate_postalcode() -> str:

    print("generating postal code")
    return f"5{random.randint(10000,99999)}"



