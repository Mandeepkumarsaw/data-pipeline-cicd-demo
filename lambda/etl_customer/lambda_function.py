import csv
import io
import json
import os

import boto3
from etl_customer.transform import row_to_item

# Fixed S3 bucket and file path
S3_BUCKET = "testingrawdata-etl"
S3_KEY = "data-etl-test1/customer.csv"

# DynamoDB table name
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "etl-test")


def lambda_handler(event, context):
    try:
        # Initialize AWS clients
        s3 = boto3.client("s3")
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(DYNAMODB_TABLE)

        # Always use fixed bucket and key
        bucket = S3_BUCKET
        key = S3_KEY

        # Read CSV file from S3
        response = s3.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")

        # Parse CSV data
        reader = csv.DictReader(io.StringIO(body))
        records_written = 0

        # Write records to DynamoDB
        with table.batch_writer() as batch:
            for row in reader:
                batch.put_item(Item=row_to_item(row, key))
                records_written += 1

        # Success response
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "ETL completed successfully",
                "bucket": bucket,
                "key": key,
                "records_written": records_written,
                "table": DYNAMODB_TABLE
            })
        }

    except Exception as e:
        # Error response
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }