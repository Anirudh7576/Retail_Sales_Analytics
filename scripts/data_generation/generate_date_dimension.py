"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Generate Date Dimension data and validate it.
"""

from scripts.common.constants import (
    DATE_START,
    DATE_END, 
    DATE_REQUIRED_FIELDS
    )
from scripts.common.validation import (
    check_required_fields, 
    check_unique
    )
from scripts.common.file_utils import save_json

from datetime import date, timedelta

# ======================================================================
# generate date dimension data
# ======================================================================

def generate_date_dimension()-> list:
    dim_date = []

    start_date = date.fromisoformat(DATE_START)
    end_date = date.fromisoformat(DATE_END)

    current_date = start_date

    while current_date <= end_date:

        date_record = {
            "date_id"    : int(current_date.strftime("%Y%m%d")),
            "full_date"  : current_date.isoformat(),
            "day"        : current_date.day,
            "day_name"   : current_date.strftime("%A"),
            "week"       : current_date.isocalendar().week,
            "month"      : current_date.month,
            "month_name" :current_date.strftime("%B"),
            "quarter"    :(current_date.month -1) // 3 +1 ,
            "year"       : current_date.year

        }


        dim_date.append(date_record)
        current_date += timedelta(days= 1)

    return dim_date

# ===================================================
# validation
# ===================================================

def main():

    dates = generate_date_dimension()

    try:
        check_required_fields(
            dates,
            DATE_REQUIRED_FIELDS
        )

        check_unique(
            dates,
            "date_id"

        )

        save_json(
            dates,
            file_prefix = "dates"
        )

    except Exception as error:
        print(f"the generation_dates not valid and has a error : {error}")

if __name__ == "__main__":
    main()



