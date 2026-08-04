""" 
Project : Retail Sales Anayltics

Author : Anirudh Krishna

Purpose : Generate Category master data and save it as json

"""
Categories = categories = [
    {
        "category_name": "Electronics",
        "category_description": "Electronic devices, gadgets, and accessories."
    },
    {
        "category_name": "Clothing",
        "category_description": "Men's, women's, and children's apparel."
    },
    {
        "category_name": "Furniture",
        "category_description": "Home and office furniture products."
    },
    {
        "category_name": "Sports",
        "category_description": "Sports equipment, fitness gear, and outdoor accessories."
    },
    {
        "category_name": "Books",
        "category_description": "Educational, fiction, non-fiction, and reference books."
    },
    {
        "category_name": "Beauty",
        "category_description": "Cosmetics, skincare, haircare, and personal care products."
    },
    {
        "category_name": "Grocery",
        "category_description": "Daily household groceries, beverages, and packaged foods."
    },
    {
        "category_name": "Toys",
        "category_description": "Toys, games, puzzles, and children's entertainment products."
    },
    {
        "category_name": "Automotive",
        "category_description": "Vehicle accessories, spare parts, and maintenance products."
    },
    {
        "category_name": "Home & Kitchen",
        "category_description": "Kitchen appliances, cookware, home décor, and household essentials."
    }
]

def generate_categories():
    """ Generate catregories data"""
    dim_category = []
    for category_id, category_name in enumerate(Categories,start = 1):
        category_record = {
            'category_id' : category_id ,
            'category_name': category_name,
            'category_description': f"{category_name} products"
        }
        dim_category.append(category_record)

    return dim_category

def validate_categories(Categories):
    """Validate categories data"""
    seen_ids = set()
    for category in Categories:
        if category['category_id'] in seen_ids:
            raise ValueError(f"Duplicate values are found for : {category['category_id']}")
    
        seen_ids.add(category['category_id'])
        
        if not category['category_name']:
            raise ValueError(f"Category name cannot be blank. Record: {category}")


        if not category['category_description']:
            raise ValueError(f"Category Description cannot be blank. Record: {category}")

    print("Category validation completed")

    return True

# def save_categories(Categories):
#     """Save data in json format"""
#     pass

def main():
    try:
        categories = generate_categories()

        validate_categories(categories)

        for category in categories:
            print(category)

        print("Process completed successfully.")

    except Exception as error:
        print(f"Process failed: {error}")

if __name__ == "__main__":
    main()



