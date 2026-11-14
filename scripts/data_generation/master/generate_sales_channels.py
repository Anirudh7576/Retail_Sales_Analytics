
from scripts.common.master_data import SALES_CHANNEL_MASTER
from scripts.common.constants import SALES_CHANNEL_REQUIRED_FIELDS
from scripts.common.validation import (
    check_required_fields,
    check_unique
)
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def generate_sales_channels() -> list:
    sales_channel_records = []

    for sales_channel_id, channel in enumerate(
        SALES_CHANNEL_MASTER, start=1
    ):
        sales_channel_record = {
            "sales_channel_id": sales_channel_id,
            **channel
        }

        sales_channel_records.append(sales_channel_record)

    return sales_channel_records


def validate_sales_channels(records: list) -> None:

    # Validate required fields
    check_required_fields(
        records,
        SALES_CHANNEL_REQUIRED_FIELDS
    )

    # Validate unique sales channel IDs
    check_unique(
        records,
        "sales_channel_id"
    )

    # Validate unique sales channel names
    check_unique(
        records,
        "sales_channel_name"
    )


def main():
    try:
        logger.info("Sales channel generation started.")

        sales_channels = generate_sales_channels()

        logger.info(
            "Generated %s sales channel records.",
            len(sales_channels)
        )

        # Validate generated records
        validate_sales_channels(sales_channels)

        logger.info("Sales channel validation successful.")

        # Save generated JSON
        save_json(
            sales_channels,
            "sales_channels",
            "generated",
            "master"
        )

        logger.info(
            "Sales channel generation completed successfully."
        )

    except Exception:
        logger.exception(
            "Sales channel generation failed."
        )
        raise


if __name__ == "__main__":
    main()
