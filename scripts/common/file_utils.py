"""
Project : Retail Sales Analytics

Author : Anirudh Krishna

Purpose : Common utility functions for file operations.
"""

import json
from datetime import datetime
from pathlib import Path

def save_json(records: list, file_prefix: str, folder_type: str ) -> None:
    """
    Save records as a timestamped JSON file
    """
    allower_folders = {
        "generated",
        "rejected",
        "archive"
    }

    if folder_type not in allower_folders:
        raise ValueError(
            f"invalid folder type {folder_type}"
            f"allowed folders {allower_folders}"
        )
    
    # =====================================================
    # Project Root
    # =====================================================

    project_root = Path(__file__).resolve().parents[2]

    output_folder = (
        project_root
        / "data"
        / folder_type
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

    # =================================================================
    # Read the latest JSON file for given dimension
    # =================================================================
     
def get_latest_json(folder_name:str, file_prefix:str) -> str:

    project_root = Path(__file__).resolve().parents[2]

    folder = (
             project_root
             /"data"
             /"generated"
             /folder_name
    )

    files = list(
        folder.glob(f"{file_prefix}_*json")

    )

    if not files:
        raise FileNotFoundError(
            f"No json file found for {file_prefix} in",
            f" the {folder_name}"
        )

    latest_file = max(
        files,
        key= lambda file: file.stat().st_mtime 
    )

    with open(latest_file,
              "r",
              encoding = "utf-8"
              ) as file:
        
        records = json.load(file)

    print(
        f"reading latest {file_prefix} file",
        f"{latest_file}.name"
    )

    return records 

        

