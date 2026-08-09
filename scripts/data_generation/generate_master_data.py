from scripts.data_generation.generate_categories import main as category_main
from scripts.data_generation.generate_subcategories import main as subcategory_main
from scripts.data_generation.generate_products import main as products_main
from scripts.data_generation.generate_geography import main as geography_main

def main():

    print("Category data generation started")
    category_main()

    print("subcategory data generation started")
    subcategory_main()

    print("products data generation started")
    products_main()

    print("geography data generation started")
    geography_main()

   
    print("Data generation completed")

if __name__ == "__main__":
    main()

