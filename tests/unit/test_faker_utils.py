
from scripts.common.faker_utils import (
    generate_postalcode,
    generate_phone_number
)


def test_generate_postalcode():

    postal_code = generate_postalcode()

    assert isinstance(postal_code, str)
    assert len(postal_code) == 6
    assert postal_code.isdigit()
    assert postal_code[0] != "0"


def test_generate_phone_number():

    phone_number = generate_phone_number()

    assert isinstance(phone_number, str)
    assert len(phone_number) == 10
    assert phone_number.isdigit()
    assert phone_number[0] in "6789"


if __name__ == "__main__":

    test_generate_postalcode()
    test_generate_phone_number()

    print("Faker utility tests passed.")
