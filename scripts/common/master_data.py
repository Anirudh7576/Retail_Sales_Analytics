
# ============================================================
# FMCG CATEGORY MASTER DATA
# ============================================================

CATEGORY_MASTER = [
    {
        "category_name": "Self Care",
        "category_description": "Personal care and hygiene products"
    },
    {
        "category_name": "Germ Protection",
        "category_description": "Products for germ protection and disinfection"
    },
    {
        "category_name": "Household Care",
        "category_description": "Household cleaning and maintenance products"
    },
    {
    "category_name": "Personal Hygiene",
    "category_description": (
        "Products for personal hygiene, skin care, "
        "protective hygiene and everyday personal care"
    )
    }
]

# =======================================================================================
# FMCG SUB CATEGORIES MASTER DATA
# =======================================================================================

SUBCATEGORY_MASTER = [
    # Self Care
    {
        "category_name": "Self Care",
        "subcategory_name": "Skincare",
        "subcategory_description": "Skin care and moisturizing products"
    },
    {
        "category_name": "Self Care",
        "subcategory_name": "Hair Care",
        "subcategory_description": "Hair cleaning and conditioning products"
    },
    {
        "category_name": "Self Care",
        "subcategory_name": "Oral Care",
        "subcategory_description": "Toothpaste and oral hygiene products"
    },
    {
        "category_name": "Self Care",
        "subcategory_name": "Personal Hygiene",
        "subcategory_description": "Personal hygiene products"
    },
    {
        "category_name": "Self Care",
        "subcategory_name": "Baby Care",
        "subcategory_description": "Baby hygiene and care products"
    },

    # Germ Protection
    {
        "category_name": "Germ Protection",
        "subcategory_name": "Hand Wash",
        "subcategory_description": "Hand washing products"
    },
    {
        "category_name": "Germ Protection",
        "subcategory_name": "Surface Disinfectants",
        "subcategory_description": "Surface cleaning and disinfecting products"
    },
    {
        "category_name": "Germ Protection",
        "subcategory_name": "Toilet Cleaners",
        "subcategory_description": "Toilet cleaning products"
    },
    {
        "category_name": "Germ Protection",
        "subcategory_name": "Antiseptics",
        "subcategory_description": "Antiseptic hygiene products"
    },
    {
        "category_name": "Germ Protection",
        "subcategory_name": "Sanitizers",
        "subcategory_description": "Hand sanitizing products"
    },

    # Household Care
    {
        "category_name": "Household Care",
        "subcategory_name": "Laundry Detergents",
        "subcategory_description": "Laundry washing products"
    },
    {
        "category_name": "Household Care",
        "subcategory_name": "Dishwashing",
        "subcategory_description": "Dishwashing liquids and products"
    },
    {
        "category_name": "Household Care",
        "subcategory_name": "Floor Cleaners",
        "subcategory_description": "Floor cleaning products"
    },
    {
        "category_name": "Household Care",
        "subcategory_name": "Fabric Care",
        "subcategory_description": "Fabric softening and care products"
    },
    {
        "category_name": "Household Care",
        "subcategory_name": "Air Care",
        "subcategory_description": "Air freshening products"
    },

    # Personal Hygiene
    {
        "category_name": "Personal Hygiene",
        "subcategory_name": "Protective Hygiene",
        "subcategory_description": "Personal protective and hygiene products including gloves, face masks and hygiene kits"
    },
    {
        "category_name": "Personal Hygiene",
        "subcategory_name": "Skin Moisturizing Care",
        "subcategory_description": "Skin moisturizing and hydration products including lotions and skin care gels"
    },
    {
        "category_name": "Personal Hygiene",
        "subcategory_name": "Body Hygiene",
        "subcategory_description": "Body cleansing, personal hygiene wipes and body freshening products"
    },
    {
        "category_name": "Personal Hygiene",
        "subcategory_name": "Personal Care Essentials",
        "subcategory_description": "Everyday personal care products including aloe vera gel, care kits and hygiene wipes"
    },
    {
        "category_name": "Personal Hygiene",
        "subcategory_name": "Gentle Skin Care",
        "subcategory_description": "Gentle skin cleansing and care products including creams, wipes and cleansing washes"
    }
]


# ============================================================
# Map each brand to the categories it is allowed to sell.

BRAND_CATEGORY_MAPPING = {
    1: {2, 4},       # PureShield: Germ Protection, Personal Hygiene
    2: {3},          # FreshNest: Household Care
    3: {1, 4},       # CarePlus: Self Care, Personal Hygiene
    4: {1, 4},       # WellSpring: Self Care, Personal Hygiene
}

CATEGORY_COST_FACTORS = {
    1: 0.62,  # Self Care
    2: 0.58,  # Germ Protection
    3: 0.60,  # Household Care
    4: 0.55,  # Personal Hygiene
}

# Map each subcategory to its parent category.
SUBCATEGORY_CATEGORY_MAPPING = {
    1: 1, 2: 1, 3: 1, 4: 1, 5: 1,
    6: 2, 7: 2, 8: 2, 9: 2, 10: 2,
    11: 3, 12: 3, 13: 3, 14: 3, 15: 3,
    16: 4, 17: 4, 18: 4, 19: 4, 20: 4,
}

RETAILER_TYPE_CHANNEL_MAPPING = {
    "Kirana Store": "General Trade",
    "Convenience Store": "General Trade",
    "Supermarket": "Modern Trade",
    "Department Store": "Modern Trade",
    "Pharmacy": "Pharmacy",
    "Online Retailer": "E-commerce",
    "Institutional Buyer": "Institutional"
}

# ============================================================
# FMCG BRAND MASTER DATA
# ============================================================

BRAND_MASTER = [
    {   
        "brand_id" :1,
        "brand_name": "PureShield",
        "brand_description": "Personal hygiene and protection products"
    },
    {   
        "brand_id" : 2,
        "brand_name": "FreshNest",
        "brand_description": "Household cleaning and care products"
    },
    {
        "brand_id": 3,
        "brand_name": "CarePlus",
        "brand_description": "Personal care and wellness products"
    },
    {
        "brand_id": 4,
        "brand_name": "WellSpring",
        "brand_description": "Health and personal wellness products"
    }
]

BRAND_LOOKUP = {
    brand["brand_id"]: brand["brand_name"]
    for brand in BRAND_MASTER
}

# print("Brand-category mapping:")
# for brand_id, category_ids in BRAND_CATEGORY_MAPPING.items():
#     print(brand_id, BRAND_LOOKUP[brand_id], category_ids)

# assert len(SUBCATEGORY_MASTER) == 20

# assert len({
#     item["subcategory_id"] for item in SUBCATEGORY_MASTER
# }) == 20

# assert all(
#     item["category_id"] in CATEGORY_MASTER
#     for item in SUBCATEGORY_MASTER
# )

# print("Subcategory master validation successful.")

# =======================================================================
# FMCG UOM MASTER DATA
# =======================================================================

UOM_MASTER = [
    {
        "uom_id"  : 1,
        "uom_code": "EA",
        "uom_name": "Each",
        "uom_description": "Individual sellable product unit"
    },
    { 
        "uom_id" : 2,
        "uom_code": "CASE",
        "uom_name": "Case",
        "uom_description": "Multiple individual units grouped into a case"
    },
    {
        "uom_id" : 3,
        "uom_code": "G",
        "uom_name": "Gram",
        "uom_description": "Unit of mass"
    },
    {
        "uom_id" : 4,
        "uom_code": "KG",
        "uom_name": "Kilogram",
        "uom_description": "Unit of mass equal to 1000 grams"
    },
    {
        "uom_id" : 5,
        "uom_code": "ML",
        "uom_name": "Millilitre",
        "uom_description": "Unit of liquid volume"
    },
    {
        "uom_id": 6,
        "uom_code": "L",
        "uom_name": "Litre",
        "uom_description": "Unit of liquid volume equal to 1000 millilitres"
    }
]

UOM_LOOKUP = {
    uom["uom_id"]: uom["uom_code"]
    for uom in UOM_MASTER
}

# ======================================================================
# FMCG PACKAGING_TYPE_MASTER DATA
# ======================================================================

PACKAGING_TYPE_MASTER = [
    {"packaging_type_id": 1, "packaging_type_name": "Bottle"},
    {"packaging_type_id": 2, "packaging_type_name": "Tube"},
    {"packaging_type_id": 3, "packaging_type_name": "Sachet"},
    {"packaging_type_id": 4, "packaging_type_name": "Pouch"},
    {"packaging_type_id": 5, "packaging_type_name": "Jar"},
    {"packaging_type_id": 6, "packaging_type_name": "Can"},
    {"packaging_type_id": 7, "packaging_type_name": "Box"},
    {"packaging_type_id": 8, "packaging_type_name": "Carton"}
]

def generate_packaging_types() -> list:
    return [dict(record) for record in PACKAGING_TYPE_MASTER]
# ========================================================================
# FMCG GEOGRAPHY MASTER DATA
# ========================================================================

GEOGRAPHY_MASTER = [
    # Andhra Pradesh
    {
        "city": "Visakhapatnam",
        "district": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "region": "South",
        "country": "India",
        "postal_code": "530001"
    },
    {
        "city": "Vijayawada",
        "district": "NTR",
        "state": "Andhra Pradesh",
        "region": "South",
        "country": "India",
        "postal_code": "520001"
    },
    {
        "city": "Tirupati",
        "district": "Tirupati",
        "state": "Andhra Pradesh",
        "region": "South",
        "country": "India",
        "postal_code": "517501"
    },

    # Telangana
    {
        "city": "Hyderabad",
        "district": "Hyderabad",
        "state": "Telangana",
        "region": "South",
        "country": "India",
        "postal_code": "500001"
    },
    {
        "city": "Warangal",
        "district": "Hanumakonda",
        "state": "Telangana",
        "region": "South",
        "country": "India",
        "postal_code": "506001"
    },
    {
        "city": "Karimnagar",
        "district": "Karimnagar",
        "state": "Telangana",
        "region": "South",
        "country": "India",
        "postal_code": "505001"
    },

    # Karnataka
    {
        "city": "Bengaluru",
        "district": "Bengaluru Urban",
        "state": "Karnataka",
        "region": "South",
        "country": "India",
        "postal_code": "560001"
    },
    {
        "city": "Mysuru",
        "district": "Mysuru",
        "state": "Karnataka",
        "region": "South",
        "country": "India",
        "postal_code": "570001"
    },
    {
        "city": "Mangaluru",
        "district": "Dakshina Kannada",
        "state": "Karnataka",
        "region": "South",
        "country": "India",
        "postal_code": "575001"
    },

    # Tamil Nadu
    {
        "city": "Chennai",
        "district": "Chennai",
        "state": "Tamil Nadu",
        "region": "South",
        "country": "India",
        "postal_code": "600001"
    },
    {
        "city": "Coimbatore",
        "district": "Coimbatore",
        "state": "Tamil Nadu",
        "region": "South",
        "country": "India",
        "postal_code": "641001"
    },
    {
        "city": "Madurai",
        "district": "Madurai",
        "state": "Tamil Nadu",
        "region": "South",
        "country": "India",
        "postal_code": "625001"
    },

    # Kerala
    {
        "city": "Thiruvananthapuram",
        "district": "Thiruvananthapuram",
        "state": "Kerala",
        "region": "South",
        "country": "India",
        "postal_code": "695001"
    },
    {
        "city": "Kochi",
        "district": "Ernakulam",
        "state": "Kerala",
        "region": "South",
        "country": "India",
        "postal_code": "682001"
    },
    {
        "city": "Kozhikode",
        "district": "Kozhikode",
        "state": "Kerala",
        "region": "South",
        "country": "India",
        "postal_code": "673001"
    },

    # Maharashtra
    {
        "city": "Mumbai",
        "district": "Mumbai City",
        "state": "Maharashtra",
        "region": "West",
        "country": "India",
        "postal_code": "400001"
    },
    {
        "city": "Pune",
        "district": "Pune",
        "state": "Maharashtra",
        "region": "West",
        "country": "India",
        "postal_code": "411001"
    },
    {
        "city": "Nagpur",
        "district": "Nagpur",
        "state": "Maharashtra",
        "region": "West",
        "country": "India",
        "postal_code": "440001"
    },

    # Gujarat
    {
        "city": "Ahmedabad",
        "district": "Ahmedabad",
        "state": "Gujarat",
        "region": "West",
        "country": "India",
        "postal_code": "380001"
    },
    {
        "city": "Surat",
        "district": "Surat",
        "state": "Gujarat",
        "region": "West",
        "country": "India",
        "postal_code": "395003"
    },
    {
        "city": "Vadodara",
        "district": "Vadodara",
        "state": "Gujarat",
        "region": "West",
        "country": "India",
        "postal_code": "390001"
    },

    # Rajasthan
    {
        "city": "Jaipur",
        "district": "Jaipur",
        "state": "Rajasthan",
        "region": "North",
        "country": "India",
        "postal_code": "302001"
    },
    {
        "city": "Jodhpur",
        "district": "Jodhpur",
        "state": "Rajasthan",
        "region": "North",
        "country": "India",
        "postal_code": "342001"
    },

    # Delhi
    {
        "city": "New Delhi",
        "district": "New Delhi",
        "state": "Delhi",
        "region": "North",
        "country": "India",
        "postal_code": "110001"
    },

    # Uttar Pradesh
    {
        "city": "Lucknow",
        "district": "Lucknow",
        "state": "Uttar Pradesh",
        "region": "North",
        "country": "India",
        "postal_code": "226001"
    },
    {
        "city": "Kanpur",
        "district": "Kanpur Nagar",
        "state": "Uttar Pradesh",
        "region": "North",
        "country": "India",
        "postal_code": "208001"
    },

    # West Bengal
    {
        "city": "Kolkata",
        "district": "Kolkata",
        "state": "West Bengal",
        "region": "East",
        "country": "India",
        "postal_code": "700001"
    },

    # Odisha
    {
        "city": "Bhubaneswar",
        "district": "Khordha",
        "state": "Odisha",
        "region": "East",
        "country": "India",
        "postal_code": "751001"
    },

    # Bihar
    {
        "city": "Patna",
        "district": "Patna",
        "state": "Bihar",
        "region": "East",
        "country": "India",
        "postal_code": "800001"
    },

    # Madhya Pradesh
    {
        "city": "Bhopal",
        "district": "Bhopal",
        "state": "Madhya Pradesh",
        "region": "Central",
        "country": "India",
        "postal_code": "462001"
    },

    # Punjab
    {
        "city": "Ludhiana",
        "district": "Ludhiana",
        "state": "Punjab",
        "region": "North",
        "country": "India",
        "postal_code": "141001"
    },

    # Haryana
    {
        "city": "Gurugram",
        "district": "Gurugram",
        "state": "Haryana",
        "region": "North",
        "country": "India",
        "postal_code": "122001"
    }
]

# ==============================================================
# FMCG DISTRIBUTOR MASTER DATA
# ==============================================================

DISTRIBUTOR_MASTER = [
    {
        "distributor_name": f"ABC Distribution Partner {i:03d}",
        "geography_id": ((i - 1) % len(GEOGRAPHY_MASTER)) + 1
    }
    for i in range(1, 101)
]

# ===============================================================
# FMCG RETAIL MASTER DATA
# ================================================================

RETAILER_TYPES = [
    "Kirana Store",
    "Supermarket",
    "Pharmacy",
    "Convenience Store",
    "Department Store"
]

RETAILER_MASTER = [
    {
        "retailer_name": f"ABC Retail Outlet {i:05d}",
        "retailer_type": RETAILER_TYPES[(i - 1) % len(RETAILER_TYPES)],
        "geography_id": ((i - 1) % len(GEOGRAPHY_MASTER)) + 1
    }
    for i in range(1, 20001)
]

# =======================================================
# FMCG WAREHOUSE MASTER DATA
# =======================================================

WAREHOUSE_MASTER = [
    {
        "warehouse_name": f"ABC Regional Warehouse {i:03d}",
        "geography_id": ((i - 1) % len(GEOGRAPHY_MASTER)) + 1
    }
    for i in range(1, 51)
]
# ========================================================
# FMCG SALES_CHANNEL_MASTER DATA
# ========================================================

SALES_CHANNEL_MASTER = [
    {
        "sales_channel_name": "General Trade",
        "sales_channel_description": "Traditional retail outlets such as kirana stores and independent shops"
    },
    {
        "sales_channel_name": "Modern Trade",
        "sales_channel_description": "Organized retail outlets such as supermarkets and hypermarkets"
    },
    {
        "sales_channel_name": "Pharmacy",
        "sales_channel_description": "Pharmacies and medical retail outlets"
    },
    {
        "sales_channel_name": "E-commerce",
        "sales_channel_description": "Online retail and digital commerce platforms"
    },
    {
        "sales_channel_name": "Institutional",
        "sales_channel_description": "Bulk sales to institutions and business customers"
    }
]

# ===========================================================
# FMCG DISTRIBUTOR_RETAILER_MAPPING_MASTER DATA
# ===========================================================

DISTRIBUTOR_RETAILER_MAPPING_MASTER = [
    {
        "distributor_id": ((retailer_id - 1) % len(DISTRIBUTOR_MASTER)) + 1,
        "retailer_id": retailer_id,
        "effective_start_date": "2026-01-01",
        "effective_end_date": "9999-12-31"
    }
    for retailer_id in range(1, 20001)
] + [
    {
        "distributor_id": (retailer_id % len(DISTRIBUTOR_MASTER)) + 1,
        "retailer_id": retailer_id,
        "effective_start_date": "2025-01-01",
        "effective_end_date": "2025-12-31"
    }
    for retailer_id in range(1, 5001)
]

# =======================================================
#  FMCG PRODUCT MASTER DATA
# =======================================================

PRODUCT_PACKAGING_PROFILES = {
    "G_TUBE_SACHET": {
        "content_uom_id": 3,
        "options": [
            (20, 3, "sachet", 0.35),
            (50, 2, "tube", 0.72),
            (100, 2, "tube", 1.00),
            (150, 2, "tube", 1.35),
            (200, 2, "tube", 1.65),
        ],
    },

    "G_TUBE": {
        "content_uom_id": 3,
        "options": [
            (20, 2, "tube", 0.35),
            (30, 2, "tube", 0.48),
            (50, 2, "tube", 0.72),
            (100, 2, "tube", 1.00),
            (150, 2, "tube", 1.35),
        ],
    },

    "G_POWDER": {
        "content_uom_id": 3,
        "options": [
            (50, 4, "pouch", 0.45),
            (100, 4, "pouch", 0.70),
            (200, 4, "pouch", 1.00),
            (400, 5, "jar", 1.70),
            (500, 5, "jar", 2.00),
        ],
    },

    "G_DETERGENT": {
        "content_uom_id": 3,
        "options": [
            (500, 4, "pouch", 0.65),
            (1000, 4, "pouch", 1.00),
            (2000, 4, "pouch", 1.75),
            (3000, 8, "carton", 2.40),
            (5000, 8, "carton", 3.60),
        ],
    },

    "G_BAR": {
        "content_uom_id": 3,
        "options": [
            (75, 7, "box", 0.80),
            (100, 7, "box", 1.00),
            (125, 7, "box", 1.20),
            (150, 7, "box", 1.40),
            (200, 7, "box", 1.75),
        ],
    },

    "ML_BOTTLE": {
        "content_uom_id": 5,
        "options": [
            (100, 1, "bottle", 0.65),
            (200, 1, "bottle", 1.00),
            (250, 1, "bottle", 1.20),
            (500, 1, "bottle", 2.00),
            (1000, 1, "bottle", 3.50),
        ],
    },

    "ML_TUBE_BOTTLE": {
        "content_uom_id": 5,
        "options": [
            (50, 2, "tube", 0.45),
            (100, 2, "tube", 0.70),
            (200, 1, "bottle", 1.00),
            (500, 1, "bottle", 2.00),
            (1000, 1, "bottle", 3.50),
        ],
    },

    "ML_AEROSOL": {
        "content_uom_id": 5,
        "options": [
            (50, 6, "can", 0.55),
            (100, 6, "can", 0.80),
            (150, 6, "can", 1.00),
            (200, 6, "can", 1.25),
            (250, 6, "can", 1.50),
        ],
    },

    "ML_REFILL": {
        "content_uom_id": 5,
        "options": [
            (200, 4, "pouch", 0.55),
            (500, 4, "pouch", 1.00),
            (750, 4, "pouch", 1.35),
            (1000, 4, "pouch", 1.70),
            (2000, 4, "pouch", 2.90),
        ],
    },

    "WIPE_POUCH": {
        "content_uom_id": 1,
        "options": [
            (10, 4, "pouch", 1.00),
            (20, 4, "pouch", 1.70),
            (30, 4, "pouch", 2.30),
            (50, 4, "pouch", 3.40),
            (72, 4, "pouch", 4.60),
        ],
    },

    "COUNT_BOX": {
        "content_uom_id": 1,
        "options": [
            (3, 7, "box", 2.80),
            (6, 7, "box", 5.20),
            (10, 7, "box", 8.00),
            (12, 7, "box", 9.30),
            (20, 8, "carton", 14.50),
        ],
    },

    "EA_KIT": {
        "content_uom_id": 1,
        "options": [
            (1, 7, "box", 1.00),
            (2, 7, "box", 1.80),
            (3, 7, "box", 2.50),
            (4, 8, "carton", 3.20),
            (5, 8, "carton", 3.80),
        ],
    },


    "EA_PROTECTIVE_PACK": {
        "content_uom_id": 1,
        "options": [
            (10, 7, "box", 0.30),
            (20, 7, "box", 0.55),
            (50, 7, "box", 1.00),
            (100, 8, "carton", 1.85),
            (200, 8, "carton", 3.40),
        ],
    },
    
    "G_JAR": {
    "content_uom_id": 3,
    "options": [
        (50, 5, "jar", 0.65),
        (100, 5, "jar", 1.00),
        (200, 5, "jar", 1.75),
        (400, 5, "jar", 2.80),
        (500, 5, "jar", 3.30),
      ],
    },

}


PRODUCT_FAMILY_PACKAGING_PROFILE = {

    # ==================================
    # 1. SELF CARE
    # ==================================

    "Face Wash": "G_TUBE_SACHET",
    "Moisturizer": "G_TUBE",
    "Sunscreen": "G_TUBE",

    "Shampoo": "ML_TUBE_BOTTLE",
    "Conditioner": "ML_TUBE_BOTTLE",
    "Hair Oil": "ML_BOTTLE",

    "Toothpaste": "G_TUBE",
    "Toothbrush": "COUNT_BOX",
    "Mouthwash": "ML_BOTTLE",

    "Body Wash": "ML_TUBE_BOTTLE",
    "Deodorant": "ML_AEROSOL",
    "Talcum Powder": "G_POWDER",

    "Baby Lotion": "ML_BOTTLE",
    "Baby Shampoo": "ML_BOTTLE",
    "Baby Wipes": "WIPE_POUCH",

    # ==================================
    # 2. GERM PROTECTION
    # ==================================

    "Liquid Hand Wash": "ML_BOTTLE",
    "Hand Sanitizer": "ML_BOTTLE",
    "Hand Soap": "G_BAR",

    "Surface Disinfectant": "ML_BOTTLE",
    "Multipurpose Cleaner": "ML_BOTTLE",
    "Disinfectant Spray": "ML_AEROSOL",

    "Toilet Cleaner": "ML_BOTTLE",
    "Toilet Blocks": "COUNT_BOX",
    "Toilet Gel": "ML_BOTTLE",

    "Antiseptic Liquid": "ML_BOTTLE",
    "Antiseptic Cream": "G_TUBE",
    "Antiseptic Spray": "ML_AEROSOL",

    "Sanitizing Hand Gel": "ML_BOTTLE",
    "Sanitizing Wipes": "WIPE_POUCH",
    "Sanitizer Refill": "ML_REFILL",

    # ==================================
    # 3. HOUSEHOLD CARE
    # ==================================

    "Detergent Powder": "G_DETERGENT",
    "Liquid Detergent": "ML_REFILL",
    "Detergent Bar": "G_BAR",

    "Dishwash Liquid": "ML_BOTTLE",
    "Dishwash Bar": "G_BAR",
    "Dishwash Gel": "ML_BOTTLE",

    "Floor Cleaner": "ML_BOTTLE",
    "Floor Disinfectant": "ML_BOTTLE",
    "Concentrated Floor Cleaner": "ML_BOTTLE",

    "Fabric Conditioner": "ML_BOTTLE",
    "Fabric Whitener": "ML_BOTTLE",
    "Stain Remover": "ML_BOTTLE",

    "Room Freshener": "ML_AEROSOL",
    "Air Freshener Gel": "G_JAR",
    "Air Freshener Spray": "ML_AEROSOL",

    # ==================================
    # 4. PERSONAL HYGIENE
    # ==================================
    
    "Hand Protection Gloves": "EA_PROTECTIVE_PACK",
    "Disposable Face Masks": "EA_PROTECTIVE_PACK",
    "Protective Hygiene Kit": "EA_KIT",
    "Personal Care Kit": "EA_KIT",

    "Body Lotion": "ML_BOTTLE",
    "Moisturizing Lotion": "ML_BOTTLE",
    "Skin Care Gel": "G_TUBE",

    "Gentle Body Wash": "ML_BOTTLE",
    "Personal Hygiene Wipes": "WIPE_POUCH",
    "Body Freshener": "ML_AEROSOL",

    "Aloe Vera Gel": "G_TUBE",
    "Multipurpose Hygiene Wipes": "WIPE_POUCH",

    "Skin Care Cream": "G_TUBE",
    "Gentle Cleansing Wipes": "WIPE_POUCH",
    "Gentle Cleansing Wash": "ML_BOTTLE",

}

# ==========================================================
def validate_product_family_profiles():

    family_details = {
        family[0]: family[1]
        for families in PRODUCT_FAMILIES.values()
        for family in families
    }

    mapped_names = set(PRODUCT_FAMILY_PACKAGING_PROFILE)
    family_names = set(family_details)

    missing_profiles = family_names - mapped_names
    unused_mappings = mapped_names - family_names

    if missing_profiles:
        raise ValueError(
            f"Missing product mappings: {missing_profiles}"
        )

    if unused_mappings:
        raise ValueError(
            f"Unused product mappings: {unused_mappings}"
        )

    for family_name, profile_key in PRODUCT_FAMILY_PACKAGING_PROFILE.items():

        if profile_key not in PRODUCT_PACKAGING_PROFILES:
            raise ValueError(
                f"Unknown packaging profile: {profile_key}"
            )

        expected_uom = family_details[family_name]

        actual_uom = PRODUCT_PACKAGING_PROFILES[profile_key][
            "content_uom_id"
        ]

        if expected_uom != actual_uom:
            raise ValueError(
                f"UOM mismatch for {family_name}: "
                f"Expected {expected_uom}, got {actual_uom}"
            )

    print("Product family packaging validation successful.")


# --------------------------------------------------
# PRODUCT FAMILY DEFINITIONS
# --------------------------------------------------

# Format:
# product family, content UOM ID, base MRP, shelf life days

PRODUCT_FAMILIES = {
    # Self Care
    1: [
        ("Face Wash", 3, 120, 730),
        ("Moisturizer", 3, 150, 730),
        ("Sunscreen", 3, 250, 730)
    ],
    2: [
        ("Shampoo", 5, 180, 730),
        ("Conditioner", 5, 170, 730),
        ("Hair Oil", 5, 120, 730)
    ],
    3: [
        ("Toothpaste", 3, 90, 730),
        ("Toothbrush", 1, 40, 1095),
        ("Mouthwash", 5, 150, 730)
    ],
    4: [
        ("Body Wash", 5, 160, 730),
        ("Deodorant", 5, 180, 1095),
        ("Talcum Powder", 3, 100, 1095)
    ],
    5: [
        ("Baby Lotion", 5, 180, 730),
        ("Baby Shampoo", 5, 160, 730),
        ("Baby Wipes", 1, 90, 730)
    ],

    # Germ Protection
    6: [
        ("Liquid Hand Wash", 5, 110, 730),
        ("Hand Sanitizer", 5, 90, 730),
        ("Hand Soap", 3, 45, 1095)
    ],
    7: [
        ("Surface Disinfectant", 5, 140, 730),
        ("Multipurpose Cleaner", 5, 130, 730),
        ("Disinfectant Spray", 5, 180, 730)
    ],
    8: [
        ("Toilet Cleaner", 5, 100, 730),
        ("Toilet Blocks", 1, 80, 1095),
        ("Toilet Gel", 5, 120, 730)
    ],
    9: [
        ("Antiseptic Liquid", 5, 110, 730),
        ("Antiseptic Cream", 3, 75, 730),
        ("Antiseptic Spray", 5, 130, 730)
    ],
    10: [
        ("Sanitizing Hand Gel", 5, 90, 730),
        ("Sanitizing Wipes", 1, 80, 730),
        ("Sanitizer Refill", 5, 100, 730),
    ],

    # Household Care
    11: [
        ("Detergent Powder", 3, 150, 730),
        ("Liquid Detergent", 5, 220, 730),
        ("Detergent Bar", 3, 35, 1095)
    ],
    12: [
        ("Dishwash Liquid", 5, 120, 730),
        ("Dishwash Bar", 3, 25, 1095),
        ("Dishwash Gel", 5, 100, 730)
    ],
    13: [
        ("Floor Cleaner", 5, 140, 730),
        ("Floor Disinfectant", 5, 130, 730),
        ("Concentrated Floor Cleaner", 5, 180, 730)
    ],
    14: [
        ("Fabric Conditioner", 5, 160, 730),
        ("Fabric Whitener", 5, 90, 730),
        ("Stain Remover", 5, 130, 730)
    ],
    15: [
        ("Room Freshener", 5, 180, 1095),
        ("Air Freshener Gel", 3, 120, 730),
        ("Air Freshener Spray", 5, 200, 1095)
    ],

    # Personal Hygiene
    
    16: [
        ("Hand Protection Gloves", 1, 120, 1095),
        ("Disposable Face Masks", 1, 80, 1095),
        ("Protective Hygiene Kit", 1, 250, 1095),
    ],
    17: [
        ("Body Lotion", 5, 180, 730),
        ("Moisturizing Lotion", 5, 160, 730),
        ("Skin Care Gel", 3, 250, 730),
    ],
    18: [
        ("Gentle Body Wash", 5, 150, 730),
        ("Personal Hygiene Wipes", 1, 100, 730),
        ("Body Freshener", 5, 160, 1095),
    ],
    19: [
        ("Aloe Vera Gel", 3, 200, 730),
        ("Personal Care Kit", 1, 350, 1095),
        ("Multipurpose Hygiene Wipes", 1, 100, 730),
    ],
    20: [
        ("Skin Care Cream", 3, 180, 730),
        ("Gentle Cleansing Wipes", 1, 110, 730),
        ("Gentle Cleansing Wash", 5, 150, 730),
    ]

}

def validate_case_quantity_mapping():

    product_families = {
        family[0]
        for families in PRODUCT_FAMILIES.values()
        for family in families
    }

    mapped_families = set(PRODUCT_CASE_QUANTITIES)

    missing_mappings = product_families - mapped_families
    unused_mappings = mapped_families - product_families

    if missing_mappings:
        raise ValueError(
            f"Missing case quantity mappings: {sorted(missing_mappings)}"
        )

    if unused_mappings:
        raise ValueError(
            f"Unused case quantity mappings: {sorted(unused_mappings)}"
        )

    print("Product case quantity mapping validation successful."
          f"{len(mapped_families)} product families."
          )
# -------------------------------------------------
#  UNITS PER CASE
# -------------------------------------------------
PRODUCT_CASE_QUANTITIES = {

    # Self Care
    "Face Wash": 24,
    "Moisturizer": 24,
    "Sunscreen": 24,

    "Shampoo": 12,
    "Conditioner": 12,
    "Hair Oil": 12,

    "Toothpaste": 24,
    "Toothbrush": 48,
    "Mouthwash": 12,

    "Body Wash": 12,
    "Deodorant": 24,
    "Talcum Powder": 12,

    "Baby Lotion": 12,
    "Baby Shampoo": 12,
    "Baby Wipes": 24,

    # Germ Protection
    "Liquid Hand Wash": 12,
    "Hand Sanitizer": 12,
    "Hand Soap": 48,

    "Surface Disinfectant": 12,
    "Multipurpose Cleaner": 12,
    "Disinfectant Spray": 12,

    "Toilet Cleaner": 12,
    "Toilet Blocks": 24,
    "Toilet Gel": 12,

    "Antiseptic Liquid": 12,
    "Antiseptic Cream": 24,
    "Antiseptic Spray": 12,

    "Sanitizing Hand Gel": 12,
    "Sanitizing Wipes": 24,
    "Sanitizer Refill": 12,

    # Household Care
    "Detergent Powder": 10,
    "Liquid Detergent": 12,
    "Detergent Bar": 48,

    "Dishwash Liquid": 12,
    "Dishwash Bar": 48,
    "Dishwash Gel": 12,

    "Floor Cleaner": 12,
    "Floor Disinfectant": 12,
    "Concentrated Floor Cleaner": 12,

    "Fabric Conditioner": 12,
    "Fabric Whitener": 12,
    "Stain Remover": 12,

    "Room Freshener": 12,
    "Air Freshener Gel": 12,
    "Air Freshener Spray": 12,

    # Personal Hygiene
    "Hand Protection Gloves": 20,
    "Disposable Face Masks": 20,
    "Protective Hygiene Kit": 6,

    "Body Lotion": 12,
    "Moisturizing Lotion": 12,
    "Skin Care Gel": 24,

    "Gentle Body Wash": 12,
    "Personal Hygiene Wipes": 24,
    "Body Freshener": 12,

    "Aloe Vera Gel": 24,
    "Personal Care Kit": 6,
    "Multipurpose Hygiene Wipes": 24,

    "Skin Care Cream": 24,
    "Gentle Cleansing Wipes": 24,
    "Gentle Cleansing Wash": 12
}
# ======================================================

def get_units_per_case(product_family):

    if product_family not in PRODUCT_CASE_QUANTITIES:
        raise ValueError(
            f"Missing case quantity for {product_family}"
        )

    return PRODUCT_CASE_QUANTITIES[product_family]

# --------------------------------------------------
# PRODUCT MASTER GENERATION
# --------------------------------------------------


def build_product_master():
    products = []
    product_id = 1

    for subcategory_id, families in PRODUCT_FAMILIES.items():

        category_id = SUBCATEGORY_CATEGORY_MAPPING[subcategory_id]
        cost_factor = CATEGORY_COST_FACTORS[category_id]

        for product_family, content_uom_id, base_mrp, shelf_life_days in families:

            profile_key = PRODUCT_FAMILY_PACKAGING_PROFILE[product_family]
            profile = PRODUCT_PACKAGING_PROFILES[profile_key]

            if content_uom_id != profile["content_uom_id"]:
                raise ValueError(
                    f"UOM mismatch for {product_family}: "
                    f"family UOM={content_uom_id}, "
                    f"profile UOM={profile['content_uom_id']}"
                )

            units_per_case = get_units_per_case(product_family)

            for brand_id, brand_name in BRAND_LOOKUP.items():

                if category_id not in BRAND_CATEGORY_MAPPING[brand_id]:
                    continue

                for pack_size, packaging_type_id, pack_label, price_factor in profile["options"]:

                    mrp = round(base_mrp * price_factor, 2)
                    standard_cost = round(mrp * cost_factor, 2)

                    packaging_label = pack_label.strip().title()

                    if content_uom_id == 1:

                        if product_family in {
                            "Personal Care Kit",
                            "Protective Hygiene Kit"
                        }:
                            product_name = (
                                f"{brand_name} {product_family} "
                                f"{pack_size} {packaging_label}"
                            )
                        else:
                            product_name = (
                                f"{brand_name} {product_family} "
                                f"{pack_size} Count {packaging_label}"
                            )

                    else:
                        content_uom = UOM_LOOKUP[content_uom_id]

                        product_name = (
                            f"{brand_name} {product_family} "
                            f"{pack_size} {content_uom} {packaging_label}"
                        )

                    product = {
                        "product_id": product_id,
                        "subcategory_id": subcategory_id,
                        "brand_id": brand_id,
                        "product_name": product_name,
                        "sku": f"FMCG-{product_id:04d}",
                        "uom_id": 1,
                        "packaging_type_id": packaging_type_id,
                        "pack_size": pack_size,
                        "content_uom_id": content_uom_id,
                        "mrp": mrp,
                        "standard_cost": standard_cost,
                        "shelf_life_days": shelf_life_days,
                        "units_per_case": units_per_case
                    }

                    products.append(product)
                    product_id += 1

    return products

# solution = build_product_master()
# print(solution)

