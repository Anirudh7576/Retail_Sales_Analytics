def check_sales_business_rules(records:list) -> bool:

    for record in records:

        if record["quantity"] <= 0:
            raise ValueError(
                 f"Quantity must be greater than 0. "
                 f"Sales key: {record['sales_key']}"
            )

        if record["unit_price"] < 0:
            raise ValueError(
                f"unit_price must be greater than 0. "
                f"Sales key: {record['sales_key']}"
            )

        if record["unit_cost"] < 0:
            raise ValueError(
                f"unit_cost must be greater than 0. "
                f"Sales key: {record['sales_key']}"
            )

        if record["discount_amount"] < 0:
            raise ValueError(
                f"discount_amount must be greater than 0. "
                f"Sales key: {record['sales_key']}"

            )

        if record["tax_amount"] < 0:
            raise ValueError(
                 f"tax_amount must be greater than 0. "
                 f"Sales key: {record['sales_key']}"
            )

        if record["sales_amount"] < 0 :
            raise ValueError(
                f"sales_amount must be greater than 0. "
                f"Sales key: {record['sales_key']}"

            )

    return True

def check_sales_calculations(records: list) -> bool:

    for record in records:

        gross_amount = (
            record["quantity"] * record["unit_price"]
        )

        taxable_amount = (
            gross_amount - record["discount_amount"]
        )

        expected_sales_amount = taxable_amount + record["tax_amount"]

        expected_profit = taxable_amount - (record["quantity"] * record["unit_cost"])

        if record["sales_amount"] != expected_sales_amount:
            raise ValueError (
                f"Incorrect sales amount for "
                f"{record['sales_key']}. "
                f"Expected: {expected_sales_amount}, "
                f"Actual: {record['sales_amount']}"
            )

        if record["profit_amount"] != expected_profit :
            raise ValueError (
                f"Incorrect profit amount for "
                f"{record['sales_key']}. "
                f"Expected: {expected_profit}, "
                f"Actual: {record['profit_amount']}"
            )

