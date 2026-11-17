
"""
Consolidated validation of all approved master datasets.

Run:
python -m scripts.validation.validate_all_master_data
"""

import json
import math
import sys

from collections import defaultdict
from datetime import date
from pathlib import Path

from scripts.validation.master_validation_config import (
    MASTER_DATA_DIR,
    MASTER_FILES,
    REQUIRED_FIELDS,
    PRIMARY_KEYS,
    FOREIGN_KEYS,
    UNIQUE_FIELDS,
    COMPOSITE_UNIQUE_FIELDS,
)

from scripts.common.master_data import (
    CATEGORY_COST_FACTORS,
    BRAND_CATEGORY_MAPPING,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class MasterDataValidator:

    def __init__(self):
        self.datasets = {}
        self.errors = []
        self.warnings = []
        self.record_counts = {}

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    @staticmethod
    def is_blank(value):
        return value is None or (
            isinstance(value, str) and not value.strip()
        )

    def load_datasets(self):
        """Load only the explicitly configured JSON files."""

        print("\n========== MASTER DATA LOADING ==========\n")

        for dataset_name, relative_path in MASTER_FILES.items():

            file_path = (
                PROJECT_ROOT
                / MASTER_DATA_DIR
                / relative_path
            )

            if not file_path.exists():
                self.add_error(
                    f"{dataset_name}: File not found: {file_path}"
                )
                continue

            try:
                with file_path.open("r", encoding="utf-8") as file:
                    records = json.load(file)

                if not isinstance(records, list):
                    self.add_error(
                        f"{dataset_name}: JSON root must be a list."
                    )
                    continue

                if not records:
                    self.add_error(
                        f"{dataset_name}: Dataset is empty."
                    )
                    continue

                self.datasets[dataset_name] = records
                self.record_counts[dataset_name] = len(records)

                print(
                    f"LOADED: {dataset_name:<32} "
                    f"Records: {len(records):,}"
                )

            except json.JSONDecodeError as exc:
                self.add_error(
                    f"{dataset_name}: Invalid JSON: {exc}"
                )

            except OSError as exc:
                self.add_error(
                    f"{dataset_name}: File read error: {exc}"
                )

        print("\nMaster data loading completed.")

    def validate_record_structure(self):
        """Check record types, required fields and blank values."""

        print("\n========== REQUIRED FIELD VALIDATION ==========\n")

        for dataset_name, records in self.datasets.items():

            required_fields = REQUIRED_FIELDS[dataset_name]

            for index, record in enumerate(records):

                record_label = f"{dataset_name}[{index}]"

                if not isinstance(record, dict):
                    self.add_error(
                        f"{record_label}: Record must be a dictionary."
                    )
                    continue

                for field in required_fields:

                    if field not in record:
                        self.add_error(
                            f"{record_label}: Missing field '{field}'."
                        )

                    elif self.is_blank(record[field]):
                        self.add_error(
                            f"{record_label}: Blank field '{field}'."
                        )

            print(f"Checked required fields: {dataset_name}")

    def validate_primary_keys(self):
        """Check primary keys for nulls and duplicates."""

        print("\n========== PRIMARY KEY VALIDATION ==========\n")

        for dataset_name, primary_key in PRIMARY_KEYS.items():

            records = self.datasets.get(dataset_name)

            if records is None:
                continue

            seen = set()

            for index, record in enumerate(records):

                if not isinstance(record, dict):
                    continue

                value = record.get(primary_key)

                if self.is_blank(value):
                    continue

                try:
                    if value in seen:
                        self.add_error(
                            f"{dataset_name}: Duplicate "
                            f"{primary_key} = {value!r}"
                        )
                    else:
                        seen.add(value)

                except TypeError:
                    self.add_error(
                        f"{dataset_name}[{index}]: "
                        f"Unhashable primary key {primary_key}."
                    )

            print(f"Checked primary key: {dataset_name}.{primary_key}")

    def validate_unique_fields(self):
        """Check unique business attributes."""

        print("\n========== BUSINESS KEY VALIDATION ==========\n")

        for dataset_name, fields in UNIQUE_FIELDS.items():

            records = self.datasets.get(dataset_name)

            if records is None:
                continue

            for field in fields:

                seen = set()

                for index, record in enumerate(records):

                    if not isinstance(record, dict):
                        continue

                    value = record.get(field)

                    if self.is_blank(value):
                        continue

                    normalized = (
                        value.strip().casefold()
                        if isinstance(value, str)
                        else value
                    )

                    try:
                        if normalized in seen:
                            self.add_error(
                                f"{dataset_name}: Duplicate "
                                f"{field} = {value!r}"
                            )
                        else:
                            seen.add(normalized)

                    except TypeError:
                        self.add_error(
                            f"{dataset_name}[{index}]: "
                            f"Invalid unique field '{field}'."
                        )

        for dataset_name, fields in COMPOSITE_UNIQUE_FIELDS.items():

            records = self.datasets.get(dataset_name)

            if records is None:
                continue

            seen = set()

            for index, record in enumerate(records):

                if not isinstance(record, dict):
                    continue

                values = tuple(
                    (
                        record.get(field).strip().casefold()
                        if isinstance(record.get(field), str)
                        else record.get(field)
                    )
                    for field in fields
                )

                if any(self.is_blank(value) for value in values):
                    continue

                if values in seen:
                    self.add_error(
                        f"{dataset_name}: Duplicate composite key "
                        f"{values!r}"
                    )
                else:
                    seen.add(values)

    def validate_foreign_keys(self):
        """Check all configured foreign-key relationships."""

        print("\n========== FOREIGN KEY VALIDATION ==========\n")

        for dataset_name, relationships in FOREIGN_KEYS.items():

            records = self.datasets.get(dataset_name)

            if records is None:
                continue

            for foreign_key, parent_dataset, parent_key in relationships:

                parent_records = self.datasets.get(parent_dataset)

                if parent_records is None:
                    self.add_error(
                        f"{dataset_name}: Parent dataset "
                        f"'{parent_dataset}' is unavailable."
                    )
                    continue

                valid_ids = {
                    record.get(parent_key)
                    for record in parent_records
                    if isinstance(record, dict)
                    and not self.is_blank(record.get(parent_key))
                }

                for index, record in enumerate(records):

                    if not isinstance(record, dict):
                        continue

                    value = record.get(foreign_key)

                    if self.is_blank(value):
                        continue

                    if value not in valid_ids:
                        self.add_error(
                            f"{dataset_name}[{index}]: "
                            f"Invalid {foreign_key} = {value!r}; "
                            f"not found in {parent_dataset}.{parent_key}."
                        )

                print(
                    f"Checked FK: {dataset_name}.{foreign_key} "
                    f"-> {parent_dataset}.{parent_key}"
                )

    def validate_product_rules(self):
        """Validate product pricing, pack sizes and brand/category rules."""

        print("\n========== PRODUCT BUSINESS RULES ==========\n")

        products = self.datasets.get("products")
        subcategories = self.datasets.get("subcategories")

        if products is None or subcategories is None:
            return

        subcategory_category = {
            record["subcategory_id"]: record["category_id"]
            for record in subcategories
            if isinstance(record, dict)
            and "subcategory_id" in record
            and "category_id" in record
        }

        for index, product in enumerate(products):

            if not isinstance(product, dict):
                continue

            product_label = (
                f"products[{index}] "
                f"(product_id={product.get('product_id')})"
            )

            numeric_fields = [
                "pack_size", "mrp", "standard_cost"
            ]

            numeric_values = {}

            for field in numeric_fields:

                value = product.get(field)

                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)
                    or value <= 0
                ):
                    self.add_error(
                        f"{product_label}: "
                        f"{field} must be a positive finite number."
                    )
                else:
                    numeric_values[field] = value

            if (
                "mrp" in numeric_values
                and "standard_cost" in numeric_values
                and numeric_values["standard_cost"] >= numeric_values["mrp"]
            ):
                self.add_error(
                    f"{product_label}: standard_cost must be lower than MRP."
                )

            for field in ["shelf_life_days", "units_per_case"]:

                value = product.get(field)

                if (
                    isinstance(value, bool)
                    or not isinstance(value, int)
                    or value <= 0
                ):
                    self.add_error(
                        f"{product_label}: "
                        f"{field} must be a positive integer."
                    )

            subcategory_id = product.get("subcategory_id")
            brand_id = product.get("brand_id")

            category_id = subcategory_category.get(subcategory_id)

            if category_id is None:
                continue

            # Validate configured category cost factor.
            factor = CATEGORY_COST_FACTORS.get(category_id)

            if factor is not None and "mrp" in numeric_values:
                expected_cost = round(numeric_values["mrp"] * factor, 2)
                actual_cost = numeric_values.get("standard_cost")

                if (
                    actual_cost is not None
                    and round(actual_cost, 2) != expected_cost
                ):
                    self.add_error(
                        f"{product_label}: standard_cost "
                        f"{actual_cost} does not match expected "
                        f"category cost {expected_cost}."
                    )

            # Validate brand-category compatibility.
            allowed_categories = BRAND_CATEGORY_MAPPING.get(brand_id)

            if (
                allowed_categories is not None
                and category_id not in allowed_categories
            ):
                self.add_error(
                    f"{product_label}: Brand {brand_id} "
                    f"is not permitted for category {category_id}."
                )

        print("Product business-rule validation completed.")

    @staticmethod
    def parse_date(value):
        """Parse an ISO date or ISO datetime into a date."""

        if not isinstance(value, str):
            raise ValueError("Date must be a string.")

        return date.fromisoformat(value[:10])

    def validate_date_dimension(self):
        """Validate date uniqueness and daily continuity."""

        print("\n========== DATE DIMENSION VALIDATION ==========\n")

        records = self.datasets.get("dates")

        if records is None:
            return

        parsed_dates = []

        for index, record in enumerate(records):

            if not isinstance(record, dict):
                continue

            try:
                parsed_dates.append(
                    self.parse_date(record["full_date"])
                )
            except (ValueError, KeyError, TypeError):
                self.add_error(
                    f"dates[{index}]: Invalid full_date "
                    f"{record.get('full_date')!r}."
                )

        if len(parsed_dates) != len(set(parsed_dates)):
            self.add_error(
                "dates: Duplicate full_date values found."
            )

        ordered_dates = sorted(parsed_dates)

        for previous, current in zip(
            ordered_dates, ordered_dates[1:]
        ):
            if (current - previous).days != 1:
                self.add_error(
                    f"dates: Date gap found between "
                    f"{previous} and {current}."
                )

        print(
            f"Date dimension checked. "
            f"Valid parsed dates: {len(parsed_dates):,}"
        )

    def validate_distributor_retailer_mappings(self):
        """Validate mapping periods and overlapping assignments."""

        print(
            "\n========== DISTRIBUTOR-RETAILER MAPPING VALIDATION ==========\n"
        )

        records = self.datasets.get("distributor_retailer_mappings")

        if records is None:
            return

        retailer_periods = defaultdict(list)

        for index, record in enumerate(records):

            if not isinstance(record, dict):
                continue

            try:
                start_date = self.parse_date(
                    record["effective_start_date"]
                )
                end_date = self.parse_date(
                    record["effective_end_date"]
                )
            except (ValueError, KeyError, TypeError):
                self.add_error(
                    f"Mapping[{index}]: Invalid effective date."
                )
                continue

            if start_date > end_date:
                self.add_error(
                    f"Mapping[{index}]: Start date is after end date."
                )
                continue

            retailer_id = record.get("retailer_id")
            distributor_id = record.get("distributor_id")

            if not self.is_blank(retailer_id):
                retailer_periods[retailer_id].append(
                    (start_date, end_date, distributor_id, index)
                )

        # A retailer must not have overlapping mapping periods.
        for retailer_id, periods in retailer_periods.items():

            periods.sort(key=lambda item: item[0])

            for previous, current in zip(periods, periods[1:]):

                previous_start, previous_end, previous_dist, previous_index = previous
                current_start, current_end, current_dist, current_index = current

                if current_start <= previous_end:
                    self.add_error(
                        f"Retailer {retailer_id}: Overlapping mapping "
                        f"periods in records {previous_index} and "
                        f"{current_index}."
                    )

        print(
            f"Mapping periods checked for "
            f"{len(retailer_periods):,} retailers."
        )

    def print_report(self):
        """Print the final validation summary."""

        print("\n" + "=" * 65)
        print("                 MASTER DATA VALIDATION REPORT")
        print("=" * 65)

        print("\nRECORD COUNTS")

        for dataset_name, count in self.record_counts.items():
            print(f"{dataset_name:<35} {count:>10,}")

        print(f"\nTotal records loaded: {sum(self.record_counts.values()):,}")
        print(f"Total errors: {len(self.errors)}")
        print(f"Total warnings: {len(self.warnings)}")

        if self.errors:
            print("\n< FAILED > MASTER DATA VALIDATION")

            for index, error in enumerate(self.errors, start=1):
                print(f"{index}. {error}")

        else:
            print("\n< PASSED > MASTER DATA VALIDATION")

        if self.warnings:
            print("\nWARNINGS")

            for warning in self.warnings:
                print(f"- {warning}")

        print("\n" + "=" * 65)

    def run(self):
        self.load_datasets()

        if self.datasets:
            self.validate_record_structure()
            self.validate_primary_keys()
            self.validate_unique_fields()
            self.validate_foreign_keys()
            self.validate_product_rules()
            self.validate_date_dimension()
            self.validate_distributor_retailer_mappings()

        self.print_report()

        return len(self.errors) == 0


def main():

    validator = MasterDataValidator()
    success = validator.run()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
