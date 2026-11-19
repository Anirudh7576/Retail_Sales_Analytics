
import csv
from pathlib import Path
from decimal import Decimal, InvalidOperation
from collections import Counter


# --------------------------------------------------
# 1. PROJECT CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ORDERS_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/orders/"
    / "orders_20261118_121559_771171.csv"
)

RECONCILED_FILE = (
    PROJECT_ROOT
    / "data/generated/transactions/orders_reconciled/"
    / "orders_reconciled_20261119_114019_453348.csv"
)

VALID_STATUSES = {
    "CONFIRMED",
    "PARTIALLY_FULFILLED",
    "FULFILLED",
    "CANCELLED",
}

REQUIRED_RECONCILED_COLUMNS = {
    "order_id",
    "order_status",
    "original_order_status",
    "reconciled_order_status",
    "ordered_quantity_total",
    "fulfilled_quantity_total",
    "remaining_quantity_total",
    "fulfillment_pct",
    "reconciled_at",
}


# --------------------------------------------------
# 2. LOAD CSV FILES
# --------------------------------------------------

def load_csv(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(
        file_path,
        mode="r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError(f"CSV has no header: {file_path}")

        return reader.fieldnames, list(reader)


# --------------------------------------------------
# 3. VALIDATION FUNCTIONS
# --------------------------------------------------

def validate_duplicate_order_ids(rows):
    order_ids = [row["order_id"].strip() for row in rows]

    duplicates = [
        order_id
        for order_id, count in Counter(order_ids).items()
        if count > 1
    ]

    return duplicates


def validate_statuses(rows):
    invalid_statuses = []

    for row in rows:
        status = row["reconciled_order_status"].strip()

        if status not in VALID_STATUSES:
            invalid_statuses.append(
                (row["order_id"], status)
            )

    return invalid_statuses


def validate_quantities(rows):
    errors = []

    for row in rows:
        order_id = row["order_id"]

        try:
            ordered = Decimal(row["ordered_quantity_total"])
            fulfilled = Decimal(row["fulfilled_quantity_total"])
            remaining = Decimal(row["remaining_quantity_total"])

        except InvalidOperation:
            errors.append(
                f"{order_id}: Invalid quantity value"
            )
            continue

        if any(
            not value.is_finite() or value < 0
            for value in (ordered, fulfilled, remaining)
        ):
            errors.append(
                f"{order_id}: Negative or invalid quantity"
            )
            continue

        if ordered != ordered.to_integral_value():
            errors.append(
                f"{order_id}: Ordered quantity is not a whole number"
            )

        if fulfilled != fulfilled.to_integral_value():
            errors.append(
                f"{order_id}: Fulfilled quantity is not a whole number"
            )

        if remaining != remaining.to_integral_value():
            errors.append(
                f"{order_id}: Remaining quantity is not a whole number"
            )

        if ordered != fulfilled + remaining:
            errors.append(
                f"{order_id}: Ordered quantity does not equal "
                "fulfilled + remaining"
            )

        if fulfilled > ordered:
            errors.append(
                f"{order_id}: Fulfilled quantity exceeds ordered quantity"
            )

    return errors


def validate_status_quantity_relationship(rows):
    errors = []

    for row in rows:
        order_id = row["order_id"]

        try:
            ordered = Decimal(row["ordered_quantity_total"])
            fulfilled = Decimal(row["fulfilled_quantity_total"])
            remaining = Decimal(row["remaining_quantity_total"])

        except InvalidOperation:
            continue

        original_status = row["original_order_status"].strip()
        reconciled_status = row["reconciled_order_status"].strip()

        if original_status == "CANCELLED":
            expected_status = "CANCELLED"

        elif original_status != "CONFIRMED":
            errors.append(
                f"{order_id}: Unexpected original status "
                f"{original_status}"
            )
            continue

        elif fulfilled == 0:
            expected_status = "CONFIRMED"

        elif fulfilled < ordered:
            expected_status = "PARTIALLY_FULFILLED"

        elif fulfilled == ordered:
            expected_status = "FULFILLED"

        else:
            continue

        if reconciled_status != expected_status:
            errors.append(
                f"{order_id}: Expected {expected_status}, "
                f"found {reconciled_status}"
            )

        if reconciled_status == "CONFIRMED" and fulfilled != 0:
            errors.append(
                f"{order_id}: CONFIRMED order has fulfilled quantity"
            )

        if reconciled_status == "FULFILLED" and remaining != 0:
            errors.append(
                f"{order_id}: FULFILLED order has remaining quantity"
            )

        if reconciled_status == "CANCELLED" and fulfilled != 0:
            errors.append(
                f"{order_id}: CANCELLED order has fulfilled quantity"
            )

    return errors


def validate_fulfillment_percentage(rows):
    errors = []

    for row in rows:
        order_id = row["order_id"]

        try:
            ordered = Decimal(row["ordered_quantity_total"])
            fulfilled = Decimal(row["fulfilled_quantity_total"])
            actual_pct = Decimal(row["fulfillment_pct"])

        except InvalidOperation:
            errors.append(
                f"{order_id}: Invalid fulfillment percentage or quantity"
            )
            continue

        if ordered == 0:
            expected_pct = Decimal("0")
        else:
            expected_pct = (
                fulfilled / ordered * Decimal("100")
            ).quantize(Decimal("0.01"))

        if abs(actual_pct - expected_pct) > Decimal("0.01"):
            errors.append(
                f"{order_id}: Expected fulfillment percentage "
                f"{expected_pct}, found {actual_pct}"
            )

    return errors


def validate_original_orders(original_rows, reconciled_rows):
    errors = []

    original_by_id = {
        row["order_id"].strip(): row
        for row in original_rows
    }

    reconciled_by_id = {
        row["order_id"].strip(): row
        for row in reconciled_rows
    }

    if set(original_by_id) != set(reconciled_by_id):
        errors.append(
            "Original and reconciled order IDs do not match"
        )
        return errors

    original_columns = original_rows[0].keys() if original_rows else []

    for order_id, original in original_by_id.items():
        reconciled = reconciled_by_id[order_id]

        for column in original_columns:
            if column not in reconciled:
                errors.append(
                    f"{order_id}: Missing original column {column}"
                )
                continue

            if original[column] != reconciled[column]:
                errors.append(
                    f"{order_id}: Original field '{column}' was changed"
                )

        if (
            reconciled["order_status"].strip()
            != reconciled["original_order_status"].strip()
        ):
            errors.append(
                f"{order_id}: Original order status was not preserved"
            )

    return errors


# --------------------------------------------------
# 4. MAIN VALIDATION
# --------------------------------------------------

def main():

    print("=" * 65)
    print("ORDER RECONCILIATION INDEPENDENT VALIDATION")
    print("=" * 65)

    original_columns, original_rows = load_csv(ORDERS_FILE)

    reconciled_columns, reconciled_rows = load_csv(
        RECONCILED_FILE
    )

    print(f"Original orders loaded: {len(original_rows)}")
    print(f"Reconciled orders loaded: {len(reconciled_rows)}")

    missing_columns = (
        REQUIRED_RECONCILED_COLUMNS - set(reconciled_columns)
    )

    if missing_columns:
        raise ValueError(
            f"Missing reconciled columns: {sorted(missing_columns)}"
        )

    results = {}

    results["Duplicate order IDs"] = (
        validate_duplicate_order_ids(reconciled_rows)
    )

    results["Invalid statuses"] = (
        validate_statuses(reconciled_rows)
    )

    results["Quantity reconciliation errors"] = (
        validate_quantities(reconciled_rows)
    )

    results["Status-to-quantity errors"] = (
        validate_status_quantity_relationship(reconciled_rows)
    )

    results["Fulfillment percentage errors"] = (
        validate_fulfillment_percentage(reconciled_rows)
    )

    results["Original order integrity errors"] = (
        validate_original_orders(original_rows, reconciled_rows)
    )

    print("\n" + "=" * 65)
    print("VALIDATION RESULTS")
    print("=" * 65)

    all_passed = True

    for check_name, errors in results.items():

        if errors:
            all_passed = False
            print(f"FAIL: {check_name}: {len(errors)}")

            for error in errors[:10]:
                print(f"  - {error}")

            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")

        else:
            print(f"PASS: {check_name}")

    print("\n" + "=" * 65)

    if len(original_rows) != len(reconciled_rows):
        all_passed = False
        print("FAIL: Original and reconciled order counts differ")

    else:
        print("PASS: Original and reconciled order counts match")

    if all_passed:
        print("\nPASS: Independent validation successful.")
    else:
        print("\nFAIL: Independent validation found errors.")

    print("=" * 65)


if __name__ == "__main__":
    main()
