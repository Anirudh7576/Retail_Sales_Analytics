from scripts.data_generation.generate_categories import main as dim_category_main
from scripts.data_generation.generate_subcategories import main as dim_subcategory_main
from scripts.data_generation.generate_products import main as dim_products_main
from scripts.data_generation.generate_geography import main as dim_geography_main
from scripts.data_generation.generate_payments import main as dim_payments_main
from scripts.data_generation.generate_customers import main as dim_customers_main
from scripts.data_generation.generate_date_dimension import main as dim_date_main
from scripts.data_generation.generate_sales import main as fact_sales_main

def main():

    print("Category data generation started")
    dim_category_main()

    print("subcategory data generation started")
    dim_subcategory_main()

    print("products data generation started")
    dim_products_main()

    print("geography data generation started")
    dim_geography_main()

    print("payments data generation started")
    dim_payments_main()

    print("customers data generation started")
    dim_customers_main()

    print("date dimension date generation started")
    dim_date_main()

    print("fact sales data generation started")
    fact_sales_main()
    
    print("Data generation completed")


if __name__ == "__main__":
    main()

