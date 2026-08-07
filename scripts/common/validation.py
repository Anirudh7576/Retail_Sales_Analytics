def check_required_fields(records: list,
                          required_fields: list) -> bool:
    """
    Validate that all required fields exist
    and are not blank.
    """

    for record in records:

        for field in required_fields:

            if field not in record:
                raise ValueError(
                    f"Missing required field '{field}'. "
                    f"Record: {record}"
                )

            if record[field] in (None, ""):
                raise ValueError(
                    f"Blank value found for '{field}'. "
                    f"Record: {record}"
                )

    return True


def check_unique(records: list, field_name: str) -> bool:
    """
    Validate uniqueness of a field.
    """

    seen_values = set()

    for record in records:

        if field_name not in record:
            raise ValueError(
                f"Field '{field_name}' not found. Record: {record}"
            )

        value = record[field_name]

        if value in seen_values:
            raise ValueError(
                f"Duplicate value found for '{field_name}': {value}"
            )

        seen_values.add(value)

    return True