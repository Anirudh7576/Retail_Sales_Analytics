
from scripts.common.business_rules import (
    check_sales_business_rules,
    check_sales_calculations
)

sales_records = [{
    "sales_key": 1001,
    "quantity": 10,
    "unit_price": 100,
    "unit_cost": 60,
    "discount_amount": 50,
    "tax_amount": 171,
    "net_sales_amount": 950,
    "invoice_amount": 1121,
    "profit_amount": 350
}]

# sales_records = [{
#     "sales_key": 1001,
#     "quantity": 0,
#     "unit_price": -100,
#     "unit_cost": -60,
#     "discount_amount": 150,
#     "tax_amount": 2171,
#     "net_sales_amount": 3950,
#     "invoice_amount": 121,
#     "profit_amount": 35
# }]
print(check_sales_business_rules(sales_records))
print(check_sales_calculations(sales_records))
