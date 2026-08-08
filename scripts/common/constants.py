#==================================================================================================================
# "Category Data"
#==================================================================================================================
CATEGORY_MASTER = [
    {
        "category_name": "Electronics",
        "category_description": "Electronic devices and accessories"
    },
    {
        "category_name": "Clothing",
        "category_description": "Men's, women's and children's apparel"
    },
    {
        "category_name": "Furniture",
        "category_description": "Home and office furniture"
    },
    {
        "category_name": "Sports",
        "category_description": "Sports equipment and fitness accessories"
    },
    {
        "category_name": "Books",
        "category_description": "Educational, fiction and non-fiction books"
    },
    {
        "category_name": "Beauty",
        "category_description": "Beauty and personal care products"
    },
    {
        "category_name": "Grocery",
        "category_description": "Daily grocery and household essentials"
    },
    {
        "category_name": "Toys",
        "category_description": "Toys and games for children"
    },
    {
        "category_name": "Automotive",
        "category_description": "Vehicle accessories and spare parts"
    },
    {
        "category_name": "Home & Kitchen",
        "category_description": "Kitchen appliances and home essentials"
    }
]

# ===================================
# Category data Validation Configuration
# ===================================
CATEGORY_REQUIRED_FIELDS = [
    "category_id",
    "category_name",
    "category_description"
]
# ==================================================================================================================
# "Sub category data"
# ==================================================================================================================

SUBCATEGORY_MASTER = [
    # Electronics
    {
        "category_name": "Electronics",
        "subcategory_name": "Mobile Phones",
        "subcategory_description": "Smartphones and accessories"
    },
    {
        "category_name": "Electronics",
        "subcategory_name": "Laptops",
        "subcategory_description": "Laptops and notebooks"
    },
    {
        "category_name": "Electronics",
        "subcategory_name": "Televisions",
        "subcategory_description": "LED, OLED and Smart TVs"
    },
    {
        "category_name": "Electronics",
        "subcategory_name": "Audio",
        "subcategory_description": "Speakers, headphones and sound systems"
    },

    # Clothing
    {
        "category_name": "Clothing",
        "subcategory_name": "Men",
        "subcategory_description": "Men's clothing and accessories"
    },
    {
        "category_name": "Clothing",
        "subcategory_name": "Women",
        "subcategory_description": "Women's clothing and accessories"
    },
    {
        "category_name": "Clothing",
        "subcategory_name": "Kids",
        "subcategory_description": "Children's clothing"
    },

    # Furniture
    {
        "category_name": "Furniture",
        "subcategory_name": "Living Room",
        "subcategory_description": "Living room furniture"
    },
    {
        "category_name": "Furniture",
        "subcategory_name": "Bedroom",
        "subcategory_description": "Bedroom furniture"
    },
    {
        "category_name": "Furniture",
        "subcategory_name": "Office",
        "subcategory_description": "Office furniture"
    },

    # Sports
    {
        "category_name": "Sports",
        "subcategory_name": "Cricket",
        "subcategory_description": "Cricket equipment"
    },
    {
        "category_name": "Sports",
        "subcategory_name": "Football",
        "subcategory_description": "Football equipment"
    },
    {
        "category_name": "Sports",
        "subcategory_name": "Fitness",
        "subcategory_description": "Gym and fitness accessories"
    },

    # Books
    {
        "category_name": "Books",
        "subcategory_name": "Fiction",
        "subcategory_description": "Fiction books"
    },
    {
        "category_name": "Books",
        "subcategory_name": "Education",
        "subcategory_description": "Educational books"
    },
    {
        "category_name": "Books",
        "subcategory_name": "Biography",
        "subcategory_description": "Biographies and autobiographies"
    },

    # Beauty
    {
        "category_name": "Beauty",
        "subcategory_name": "Skincare",
        "subcategory_description": "Skin care products"
    },
    {
        "category_name": "Beauty",
        "subcategory_name": "Hair Care",
        "subcategory_description": "Hair care products"
    },
    {
        "category_name": "Beauty",
        "subcategory_name": "Makeup",
        "subcategory_description": "Cosmetics and makeup"
    },

    # Grocery
    {
        "category_name": "Grocery",
        "subcategory_name": "Beverages",
        "subcategory_description": "Tea, coffee and soft drinks"
    },
    {
        "category_name": "Grocery",
        "subcategory_name": "Snacks",
        "subcategory_description": "Chips, biscuits and snacks"
    },
    {
        "category_name": "Grocery",
        "subcategory_name": "Staples",
        "subcategory_description": "Rice, flour and pulses"
    },

    # Toys
    {
        "category_name": "Toys",
        "subcategory_name": "Educational Toys",
        "subcategory_description": "Learning toys"
    },
    {
        "category_name": "Toys",
        "subcategory_name": "Action Figures",
        "subcategory_description": "Action figures and collectibles"
    },
    {
        "category_name": "Toys",
        "subcategory_name": "Board Games",
        "subcategory_description": "Indoor board games"
    },

    # Automotive
    {
        "category_name": "Automotive",
        "subcategory_name": "Car Accessories",
        "subcategory_description": "Interior and exterior accessories"
    },
    {
        "category_name": "Automotive",
        "subcategory_name": "Motorcycle Accessories",
        "subcategory_description": "Bike accessories"
    },
    {
        "category_name": "Automotive",
        "subcategory_name": "Engine Oils",
        "subcategory_description": "Lubricants and engine oils"
    },

    # Home & Kitchen
    {
        "category_name": "Home & Kitchen",
        "subcategory_name": "Kitchen Appliances",
        "subcategory_description": "Mixers, ovens and kitchen appliances"
    },
    {
        "category_name": "Home & Kitchen",
        "subcategory_name": "Cookware",
        "subcategory_description": "Pots, pans and utensils"
    },
    {
        "category_name": "Home & Kitchen",
        "subcategory_name": "Home Decor",
        "subcategory_description": "Decorative home products"
    }
]

# ===========================================
# Sub Category data Validation Configuration
# ===========================================
SUBCATEGORY_REQUIRED_FIELDS = [
    "subcategory_id",
    "category_id",
    "subcategory_name",
    "subcategory_description"
]
# ======================================================================================
# "Products data"
# ======================================================================================
PRODUCT_MASTER = [
    {
        "subcategory_name": "Mobile Phones",
        "product_name": "iPhone 16",
        "brand": "Apple",
        "unit_cost": 72000,
        "unit_price": 89999
    },
    {
        "subcategory_name": "Mobile Phones",
        "product_name": "Galaxy S25",
        "brand": "Samsung",
        "unit_cost": 65000,
        "unit_price": 79999
    },
    {
        "subcategory_name": "Laptops",
        "product_name": "MacBook Air M4",
        "brand": "Apple",
        "unit_cost": 85000,
        "unit_price": 99999
    }
]
# =================================================================
PRODUCT_REQUIRED_FIELDS = [
    "product_id",
    "subcategory_id",
    "product_name",
    "brand",
    "unit_cost",
    "unit_price"
]
# =================================================================
