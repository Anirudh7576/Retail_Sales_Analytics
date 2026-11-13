
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

MONEY_PRECISION = Decimal("0.01")

def to_decimal(value, field_name: str, sales_key: str) -> Decimal:
    """
    Convert a numeric value into Decimal.
    Reject missing, non-numeric and infinite values.
    """

    try:
        if isinstance(value, bool) or value is None:
            raise ValueError

        result = Decimal(str(value))

        if not result.is_finite():
            raise ValueError

        return result

    except (InvalidOperation, ValueError, TypeError):
        raise ValueError(
            f"Invalid {field_name} for sales key {sales_key}: {value}"
        )

def round_money(value: Decimal) -> Decimal:
    """Round a monetary value to two decimal places."""
    return value.quantize(
        MONEY_PRECISION,
        rounding = ROUND_HALF_UP
    )


def check_sales_business_rules(records: list) -> bool:
    required_fields = [
    "sales_key",
    "quantity",
    "unit_price",
    "unit_cost",
    "discount_amount",
    "tax_amount",
    "net_sales_amount",
    "invoice_amount",
    "profit_amount"
     ]
    
    for record in records:

        if not isinstance(record, dict):
            raise ValueError("Each sales record must be a dictionary.")

        missing_fields = [
            field for field in required_fields
            if field not in record
        ]

        if missing_fields:
            raise ValueError(
                f"Missing fields {missing_fields} in sales record."
            )

        sales_key = record["sales_key"]

        quantity = to_decimal(
            record["quantity"], "quantity", sales_key
        )
        unit_price = to_decimal(
            record["unit_price"], "unit_price", sales_key
        )
        unit_cost = to_decimal(
            record["unit_cost"], "unit_cost", sales_key
        )
        discount_amount = to_decimal(
            record["discount_amount"], "discount_amount", sales_key
        )
        tax_amount = to_decimal(
            record["tax_amount"], "tax_amount", sales_key
        )
        sales_amount = to_decimal(
            record["net_sales_amount"], "net_sales_amount", sales_key
        )
        profit_amount = to_decimal(
            record["profit_amount"], "profit_amount", sales_key
        )

        if quantity <= 0:
            raise ValueError(
                f"Quantity must be greater than 0. Sales key: {sales_key}"
            )

        if unit_price <= 0:
            raise ValueError(
                f"Unit price must be greater than 0. Sales key: {sales_key}"
            )

        if unit_cost < 0:
            raise ValueError(
                f"Unit cost cannot be negative. Sales key: {sales_key}"
            )

        if discount_amount < 0:
            raise ValueError(
                f"Discount amount cannot be negative. Sales key: {sales_key}"
            )

        if tax_amount < 0:
            raise ValueError(
                f"Tax amount cannot be negative. Sales key: {sales_key}"
            )

        if sales_amount < 0:
            raise ValueError(
                f"Sales amount cannot be negative. Sales key: {sales_key}"
            )

        gross_amount = round_money(quantity * unit_price)

        if discount_amount > gross_amount:
            raise ValueError(
                f"Discount cannot exceed gross amount. "
                f"Sales key: {sales_key}"
            )

        # Profit can be negative, for example, when a product is sold
        # below its cost. Therefore, do not reject negative profit.

    return True


def check_sales_calculations(records: list) -> bool:

    for record in records:

        quantity = Decimal(str(record["quantity"]))
        unit_price = Decimal(str(record["unit_price"]))
        unit_cost = Decimal(str(record["unit_cost"]))
        discount_amount = Decimal(str(record["discount_amount"]))
        tax_amount = Decimal(str(record["tax_amount"]))

        actual_net_sales_amount = Decimal(
            str(record["net_sales_amount"])
        )

        actual_invoice_amount = Decimal(
            str(record["invoice_amount"])
        )

        actual_profit_amount = Decimal(
            str(record["profit_amount"])
        )

        gross_amount = round_money(
            quantity * unit_price
        )

        expected_net_sales_amount = round_money(
            gross_amount - discount_amount
        )

        expected_invoice_amount = round_money(
            expected_net_sales_amount + tax_amount
        )

        expected_profit = round_money(
            expected_net_sales_amount - (quantity * unit_cost)
        )

        if actual_net_sales_amount != expected_net_sales_amount:
            raise ValueError(
                f"Incorrect net sales amount for {record['sales_key']}"
            )

        if actual_invoice_amount != expected_invoice_amount:
            raise ValueError(
                f"Incorrect invoice amount for {record['sales_key']}"
            )

        if actual_profit_amount != expected_profit:
            raise ValueError(
                f"Incorrect profit amount for {record['sales_key']}"
            )

    return True