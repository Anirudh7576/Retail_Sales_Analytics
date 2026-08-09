from faker import Faker

fake = Faker("en_IN")

def generate_postalcode() -> str:

    print("generating postal code")
    return fake.postcode()

def generate_address() -> str:

    print("generating address")
    return fake.address()

