
"""
Project : FMCG Sales and Supply Chain Analytics

Purpose : Common utility functions for file operations.
"""

import json
from datetime import datetime
from pathlib import Path


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]


# ============================================================
# SAVE JSON FILE
# ============================================================

def save_json(
    records: list,
    file_prefix: str,
    folder_type: str,
    data_group: str = ""
) -> Path:
    """
    Save records as a timestamped JSON file.

    Example:
    data/generated/master/categories/categories_20261112.json
    """

    allowed_folders = {
        "generated",
        "rejected",
        "archive"
    }

    if folder_type not in allowed_folders:
        raise ValueError(
            f"Invalid folder type: {folder_type}. "
            f"Allowed folders: {allowed_folders}"
        )

    if not isinstance(records, list):
        raise TypeError("Records must be a list.")

    if not file_prefix or Path(file_prefix).name != file_prefix:
        raise ValueError("Invalid file prefix.")

    # --------------------------------------------------------
    # Validate optional data group
    # --------------------------------------------------------

    group_path = Path(data_group)

    if group_path.is_absolute() or ".." in group_path.parts:
        raise ValueError("Invalid data group path.")

    # --------------------------------------------------------
    # Output folder
    # --------------------------------------------------------

    output_folder = (
        PROJECT_ROOT
        / "data"
        / folder_type
        / group_path
        / file_prefix
    )

    output_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Generate unique timestamped filename
    # --------------------------------------------------------

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    file_name = f"{file_prefix}_{timestamp}.json"

    file_path = output_folder / file_name

    # --------------------------------------------------------
    # Save JSON
    # --------------------------------------------------------

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            records,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nJSON file saved successfully.")
    print(f"Location: {file_path}")

    return file_path


# ============================================================
# READ LATEST JSON FILE
# ============================================================

def get_latest_json(
    folder_name: str,
    file_prefix: str
) -> list:
    """
    Read the latest JSON file for a given dataset.

    Example:
    get_latest_json("master/categories", "categories")
    """

    relative_folder = Path(folder_name)

    if (
        relative_folder.is_absolute()
        or ".." in relative_folder.parts
    ):
        raise ValueError("Invalid folder path.")

    folder = (
        PROJECT_ROOT
        / "data"
        / "generated"
        / relative_folder
    )

    files = list(
        folder.glob(f"{file_prefix}_*.json")
    )

    if not files:
        raise FileNotFoundError(
            f"No JSON file found for '{file_prefix}' "
            f"in '{folder}'."
        )

    latest_file = max(
        files,
        key=lambda file: file.stat().st_mtime
    )

    with open(
        latest_file,
        "r",
        encoding="utf-8"
    ) as file:

        records = json.load(file)

    print(
        f"\nReading latest {file_prefix} file: "
        f"{latest_file.name}"
    )

    return records
