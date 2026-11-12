
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Common utility functions for synthetic data generation.
"""

from faker import Faker

fake = Faker("en_IN")


# ============================================================
# SET RANDOM SEED
# ============================================================

def set_faker_seed(seed: int) -> None:
    """
    Set seed for reproducible synthetic data generation.
    """

    Faker.seed(seed)


# ============================================================
# GENERATE INDIAN POSTAL CODE
# ============================================================

def generate_postalcode() -> str:
    """
    Generate a six-digit Indian PIN-code format.

    Note:
    This generates a syntactically plausible PIN code,
    not necessarily an officially allocated PIN code.
    """

    first_digit = fake.random_element(
        elements=("1", "2", "3", "4", "5", "6", "7", "8", "9")
    )

    remaining_digits = fake.numerify(
        text="#####"
    )

    return first_digit + remaining_digits


# ============================================================
# GENERATE INDIAN MOBILE NUMBER
# ============================================================

def generate_phone_number() -> str:
    """
    Generate a synthetic 10-digit Indian mobile-number format.

    Note:
    Generated numbers are synthetic and should not be used
    to contact real people.
    """

    first_digit = fake.random_element(
        elements=("6", "7", "8", "9")
    )

    remaining_digits = fake.numerify(
        text="#########"
    )

    return first_digit + remaining_digits
