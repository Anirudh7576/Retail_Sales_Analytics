
from datetime import date, timedelta

from scripts.common.constants import (
    DATE_START,
    DATE_END,
    DATE_REQUIRED_FIELDS
)
from scripts.common.validation import (
    check_required_fields,
    check_unique
)
from scripts.common.file_utils import save_json
from scripts.common.logger import logger


def get_fiscal_year(current_date: date) -> str:
    """
    Indian financial year:
    April to March.

    Example:
    April 2025 to March 2026 = FY2026
    """

    if current_date.month >= 4:
        fiscal_year = current_date.year + 1
    else:
        fiscal_year = current_date.year

    return f"FY{fiscal_year}"


def get_fiscal_quarter(current_date: date) -> str:
    """
    Indian financial quarters:
    Q1: April - June
    Q2: July - September
    Q3: October - December
    Q4: January - March
    """

    month = current_date.month

    if month in (4, 5, 6):
        return "Q1"

    elif month in (7, 8, 9):
        return "Q2"

    elif month in (10, 11, 12):
        return "Q3"

    return "Q4"


def generate_date_dimension() -> list:
    date_records = []

    start_date = date.fromisoformat(DATE_START)
    end_date = date.fromisoformat(DATE_END)

    if start_date > end_date:
        raise ValueError(
            "DATE_START cannot be after DATE_END."
        )

    current_date = start_date

    while current_date <= end_date:

        # Generate stable date ID: YYYYMMDD
        date_id = int(current_date.strftime("%Y%m%d"))

        date_record = {
            "date_id": date_id,
            "full_date": current_date.isoformat(),
            "day": current_date.day,
            "day_name": current_date.strftime("%A"),
            "week": current_date.isocalendar().week,
            "month": current_date.month,
            "month_name": current_date.strftime("%B"),
            "quarter": f"Q{((current_date.month - 1) // 3) + 1}",
            "year": current_date.year,
            "fiscal_year": get_fiscal_year(current_date),
            "fiscal_quarter": get_fiscal_quarter(current_date)
        }

        date_records.append(date_record)

        current_date += timedelta(days=1)

    return date_records


def validate_date_dimension(records: list) -> None:

    # Validate required fields
    check_required_fields(
        records,
        DATE_REQUIRED_FIELDS
    )

    # Validate unique date IDs
    check_unique(records, "date_id")

    # Validate unique full dates
    check_unique(records, "full_date")

    # Validate expected date count
    start_date = date.fromisoformat(DATE_START)
    end_date = date.fromisoformat(DATE_END)

    expected_count = (end_date - start_date).days + 1

    if len(records) != expected_count:
        raise ValueError(
            f"Expected {expected_count} dates, "
            f"generated {len(records)}."
        )

    # Validate chronological sequence
    for index in range(1, len(records)):
        previous_date = date.fromisoformat(
            records[index - 1]["full_date"]
        )

        current_date = date.fromisoformat(
            records[index]["full_date"]
        )

        if current_date - previous_date != timedelta(days=1):
            raise ValueError(
                "Date dimension contains a missing or "
                "incorrectly ordered date."
            )


def main():
    try:
        logger.info("Date dimension generation started.")

        date_records = generate_date_dimension()

        logger.info(
            "Generated %s date dimension records.",
            len(date_records)
        )

        validate_date_dimension(date_records)

        logger.info(
            "Date dimension validation successful."
        )

        save_json(
            date_records,
            "dates",
            "generated",
            "master"
        )

        logger.info(
            "Date dimension generation completed successfully."
        )

    except Exception:
        logger.exception(
            "Date dimension generation failed."
        )
        raise


if __name__ == "__main__":
    main()
