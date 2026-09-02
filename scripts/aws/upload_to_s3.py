from pathlib import Path
import boto3
from botocore.exceptions import ClientError


BUCKET_NAME = "retail-sales-analytics-898565151550-us-east-1-an"

s3 = boto3.client("s3")

def upload_latest_file(local_folder: str, s3_folder: str) -> None:

    folder = Path(local_folder)

    # Find JSON files
    files = list(folder.glob("*.json"))

    if not files:
        print(f"No JSON files found in {local_folder}")
        return

    # Find latest file
    latest_file = max(
        files,
        key=lambda file: file.stat().st_mtime
    )

    # S3 object path
    s3_key = f"{s3_folder}/{latest_file.name}"

    # Check whether file already exists
    try:

        s3.head_object(
            Bucket=BUCKET_NAME,
            Key=s3_key
        )

        # If no exception, file already exists
        print(
            f"SKIPPED: {latest_file.name} "
            f"already exists in S3"
        )

    except ClientError as error:

        error_code = error.response["Error"]["Code"]

        if error_code == "404":

            # File does not exist → upload
            s3.upload_file(
                str(latest_file),
                BUCKET_NAME,
                s3_key
            )

            print(
                f"UPLOADED: {latest_file.name} "
                f"→ s3://{BUCKET_NAME}/{s3_key}"
            )

        else:
            raise

if __name__ == "__main__":

    datasets ={

        "sales": (
            "data/generated/sales",
            "landing/sales"
        ),

        "products":(
            "data/generated/products",
            "landing/products"
        ),

        "categories":(
            "data/generated/categories",
            "landing/categories"
        ),

        "subcategories":(
            "data/generated/subcategories",
            "landing/subcategories"
        ),

        "dates":(
            "data/generated/dates",
            "landing/dates"
        ),

        "geography":(
            "data/generated/geography",
            "landing/geography"
        ),

        "payments":(
            "data/generated/payments",
            "landing/payments"
        ),

        "customers":(
                    "data/generated/customers",
                    "landing/customers"
        )

    }

    for dataset, paths in datasets.items():

        local_folder, s3_folder = paths

        print("\n uploding dataset {dateset}")

        upload_latest_file(
            local_folder,
            s3_folder
        )

