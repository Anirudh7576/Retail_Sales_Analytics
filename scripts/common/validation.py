
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Common data validation functions.
"""


# ============================================================
# CHECK REQUIRED FIELDS
# ============================================================

def check_required_fields(
    records: list,
    required_fields: list
) -> bool:
    """
    Validate that all required fields exist
    and are not blank.
    """

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Record at index {index} must be a dictionary."
            )

        for field in required_fields:

            if field not in record:
                raise ValueError(
                    f"Missing required field '{field}'. "
                    f"Record: {record}"
                )

            value = record[field]

            if value is None:
                raise ValueError(
                    f"Null value found for '{field}'. "
                    f"Record: {record}"
                )

            if isinstance(value, str) and not value.strip():
                raise ValueError(
                    f"Blank value found for '{field}'. "
                    f"Record: {record}"
                )

    return True


# ============================================================
# CHECK UNIQUE VALUES
# ============================================================

def check_unique(
    records: list,
    field_name: str
) -> bool:
    """
    Validate uniqueness of a field.
    """

    seen_values = set()

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Record at index {index} must be a dictionary."
            )

        if field_name not in record:
            raise ValueError(
                f"Field '{field_name}' not found. "
                f"Record: {record}"
            )

        value = record[field_name]

        if value is None:
            raise ValueError(
                f"Null value found for '{field_name}'. "
                f"Record: {record}"
            )

        if isinstance(value, str) and not value.strip():
            raise ValueError(
                f"Blank value found for '{field_name}'. "
                f"Record: {record}"
            )

        try:
            if value in seen_values:
                raise ValueError(
                    f"Duplicate value found for "
                    f"'{field_name}': {value}"
                )

            seen_values.add(value)

        except TypeError:
            raise ValueError(
                f"Unhashable value found for "
                f"'{field_name}': {value}"
            )

    return True


# ============================================================
# CHECK FOREIGN KEYS
# ============================================================

def check_foreign_keys(
    fact_records: list,
    fact_field: str,
    dim_records: list,
    dim_field: str
) -> bool:
    """
    Validate that every foreign-key value in fact records
    exists in the corresponding dimension records.
    """

    # Validate dimension key uniqueness
    check_unique(
        dim_records,
        dim_field
    )

    # Build a set of valid dimension keys
    valid_values = {
        record[dim_field]
        for record in dim_records
    }

    for index, record in enumerate(fact_records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Fact record at index {index} "
                f"must be a dictionary."
            )

        if fact_field not in record:
            raise ValueError(
                f"Foreign key field '{fact_field}' "
                f"not found. Record: {record}"
            )

        value = record[fact_field]

        if value is None:
            raise ValueError(
                f"Null foreign key '{fact_field}'. "
                f"Record: {record}"
            )

        if isinstance(value, str) and not value.strip():
            raise ValueError(
                f"Blank foreign key '{fact_field}'. "
                f"Record: {record}"
            )

        if value not in valid_values:
            raise ValueError(
                f"Invalid foreign key '{fact_field}': {value}. "
                f"Record: {record}"
            )

    return True
