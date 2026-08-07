"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Common utility functions for file operations.
"""

import json
from datetime import datetime
from pathlib import Path


def save_json(records: list, file_prefix: str) -> None:
    """
    Save records as a timestamped JSON file.

    Parameters
    ----------
    records : list
        List of dictionaries to save.

    file_prefix : str
        Prefix used for both the folder name and file name.

        Example:
            categories
            subcategories
            products
            customers
            geography
            payment
            sales
    """

    # =====================================================
    # Project Root
    # =====================================================
    project_root = Path(__file__).resolve().parents[2]

    # =====================================================
    # Output Folder
    # Example:
    # data/generated/categories/
    # data/generated/subcategories/
    # =====================================================
    output_folder = (
        project_root
        / "data"
        / "generated"
        / file_prefix
    )

    # Create folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # =====================================================
    # File Name
    # Example:
    # categories_20260806_103015.json
    # =====================================================
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"{file_prefix}_{timestamp}.json"

    file_path = output_folder / file_name

    # =====================================================
    # Save JSON
    # =====================================================
    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nJSON file saved successfully.")
    print(f"Location : {file_path}\n")