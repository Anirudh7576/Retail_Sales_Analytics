from scripts.data_generation.generate_categories import main as category_main
from scripts.data_generation.generate_subcategories import main as subcategory_main


def main():

    print("Category data generation started")
    category_main()

    print("subcategory data generation completed")
    subcategory_main()

    print("Data generation completed")

if __name__ == "__main__":
    main()

