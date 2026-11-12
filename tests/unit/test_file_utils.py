
from scripts.common.file_utils import (
    save_json,
    get_latest_json
)


def test_save_and_read_json():

    records = [
        {
            "category_id": 1,
            "category_name": "Self Care"
        },
        {
            "category_id": 2,
            "category_name": "Germ Protection"
        }
    ]

    # Save records
    save_json(
        records,
        "test_categories",
        "generated",
        "master"
    )

    # Read latest records
    result = get_latest_json(
        "master/test_categories",
        "test_categories"
    )

    assert result == records

    print("File utility test passed.")


if __name__ == "__main__":
    test_save_and_read_json()
