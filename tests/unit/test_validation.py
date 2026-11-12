
import pytest

from scripts.common.validation import (
    check_required_fields,
    check_unique,
    check_foreign_keys
)


def test_required_fields():

    records = [
        {
            "category_id": 1,
            "category_name": "Self Care"
        }
    ]

    assert check_required_fields(
        records,
        ["category_id", "category_name"]
    ) is True


def test_required_fields_blank_value():

    records = [
        {
            "category_id": 1,
            "category_name": "   "
        }
    ]

    with pytest.raises(ValueError):
        check_required_fields(
            records,
            ["category_id", "category_name"]
        )


def test_unique():

    records = [
        {"product_id": 1},
        {"product_id": 2}
    ]

    assert check_unique(records, "product_id") is True


def test_duplicate_values():

    records = [
        {"product_id": 1},
        {"product_id": 1}
    ]

    with pytest.raises(ValueError):
        check_unique(records, "product_id")


def test_foreign_keys():

    dimensions = [
        {"subcategory_id": 101},
        {"subcategory_id": 102}
    ]

    facts = [
        {"subcategory_id": 101},
        {"subcategory_id": 102}
    ]

    assert check_foreign_keys(
        facts,
        "subcategory_id",
        dimensions,
        "subcategory_id"
    ) is True


def test_invalid_foreign_key():

    dimensions = [
        {"subcategory_id": 101},
        {"subcategory_id": 102}
    ]

    facts = [
        {"subcategory_id": 999}
    ]

    with pytest.raises(ValueError):
        check_foreign_keys(
            facts,
            "subcategory_id",
            dimensions,
            "subcategory_id"
        )
