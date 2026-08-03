1. FACT_SALES

    | Column          | Data Type    | Description       |
    | --------------- | ------------ | ----------------- |
    | sales_key       | NUMBER       | Surrogate Key     |
    | order_id        | VARCHAR      | Business Order ID |
    | customer_id     | NUMBER       | FK                |
    | product_id      | NUMBER       | FK                |
    | category_id     | NUMBER       | FK                |
    | subcategory_id  | NUMBER       | FK                |
    | geography_id    | NUMBER       | FK                |
    | payment_id      | NUMBER       | FK                |
    | date_id         | NUMBER       | FK                |
    | quantity        | NUMBER       | Units sold        |
    | unit_price      | NUMBER(10,2) | Selling price     |
    | discount_amount | NUMBER(10,2) | Discount          |
    | tax_amount      | NUMBER(10,2) | Tax               |
    | sales_amount    | NUMBER(10,2) | Final amount      |
    | profit_amount   | NUMBER(10,2) | Profit            |


2. DIM_PRODUCTS
    
    | Column         | Data Type    | Description                |
    | -------------- | ------------ | -------------------------- |
    | product_id     | NUMBER       | Primary Key                |
    | product_name   | VARCHAR      | Name of the product        |
    | brand_name     | VARCHAR      | Brand name                 |
    | category_id    | NUMBER       | References DIM_CATEGORY    |
    | subcategory_id | NUMBER       | References DIM_SUBCATEGORY |
    | unit_price     | NUMBER(10,2) | Selling price              |
    | unit_cost      | NUMBER(10,2) | Cost price                 |
    | color          | VARCHAR      | Product color              |
    | size           | VARCHAR      | Product size               |
    | weight         | NUMBER(8,2)  | Weight of product          |
    | launch_date    | DATE         | Product launch date        |
    | product_status | VARCHAR      | Active / Discontinued      |


3. DIM_CATEGORY

    | Column               | Data Type | Description                 |
    | -------------------- | --------- | --------------------------- |
    | category_id          | NUMBER    | Primary Key                 |
    | category_name        | VARCHAR   | Electronics, Clothing, etc. |
    | category_description | VARCHAR   | Category description        |

4. DIM_SUBCATGORY

    | Column                  | Data Type | Description                  |
    | ----------------------- | --------- | ---------------------------- |
    | subcategory_id          | NUMBER    | Primary Key                  |
    | category_id             | NUMBER    | References DIM_CATEGORY      |
    | subcategory_name        | VARCHAR   | Mobile Phones, Laptops, etc. |
    | subcategory_description | VARCHAR   | Description                  |


5. DIM_CUSTOMER

    | Column            | Data Type | Description                |
    | ----------------- | --------- | -------------------------- |
    | customer_id       | NUMBER    | Primary Key                |
    | first_name        | VARCHAR   | Customer first name        |
    | last_name         | VARCHAR   | Customer last name         |
    | gender            | VARCHAR   | Male/Female/Other          |
    | date_of_birth     | DATE      | DOB                        |
    | email             | VARCHAR   | Email address              |
    | phone_number      | VARCHAR   | Contact number             |
    | city              | VARCHAR   | City                       |
    | state             | VARCHAR   | State                      |
    | country           | VARCHAR   | Country                    |
    | postal_code       | VARCHAR   | Postal code                |
    | registration_date | DATE      | Customer registration date |
    | customer_status   | VARCHAR   | Active/Inactive            |

6. DIM_GEOGRAPY

    | Column          | Data Type | Description     |
    | --------------- | --------- | --------------- |
    | geography_id    | NUMBER    | Primary Key     |
    | country         | VARCHAR   | Country         |
    | region          | VARCHAR   | Region          |
    | state           | VARCHAR   | State           |
    | city            | VARCHAR   | City            |
    | postal_code     | VARCHAR   | Postal code     |
    | sales_territory | VARCHAR   | Sales territory |

7. DIM_PAYMENT

    | Column           | Data Type | Description                            |
    | ---------------- | --------- | -------------------------------------- |
    | payment_id       | NUMBER    | Primary Key                            |
    | payment_method   | VARCHAR   | Credit Card, Debit Card, UPI, Cash     |
    | payment_provider | VARCHAR   | Visa, Mastercard, PayPal, Stripe, etc. |
    | payment_status   | VARCHAR   | Success, Failed, Pending               |
    | payment_type     | VARCHAR   | Online / Offline                       |

8. DIM_DATE

    | Column      | Data Type | Description       |
    | ----------- | --------- | ----------------- |
    | date_id     | NUMBER    | YYYYMMDD          |
    | full_date   | DATE      | Actual date       |
    | day         | NUMBER    | Day               |
    | month       | NUMBER    | Month             |
    | month_name  | VARCHAR   | January           |
    | quarter     | NUMBER    | Quarter           |
    | year        | NUMBER    | Year              |
    | day_of_week | VARCHAR   | Monday            |
    | week_number | NUMBER    | Week number       |
    | is_weekend  | BOOLEAN   | Weekend indicator |
    | fiscal_year | NUMBER    | Fiscal year       |


9. Relationship Diagram

                            DIM_DATE
                            │
                            │
    DIM_PRODUCT ────────────┐
                            │
    DIM_CATEGORY ───────────┤
                            │
    DIM_SUBCATEGORY ────────┤
                            │
    DIM_CUSTOMER ───────────┤
                            │
    DIM_GEOGRAPHY ──────────┤
                            │
    DIM_PAYMENT ────────────┤
                            │
                    FACT_SALES