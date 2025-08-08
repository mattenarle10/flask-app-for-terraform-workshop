import os
import boto3

region = os.environ.get("AWS_REGION", "us-west-2")
table_name = os.environ.get("DYNAMODB_TABLE_NAME", "products-table")
bucket_name = os.environ.get("S3_BUCKET_NAME", None)

dynamodb = boto3.resource("dynamodb", region_name=region)
table = dynamodb.Table(table_name)

s3 = None
if bucket_name:
    s3 = boto3.client("s3", region_name=region)

__all__ = [
    "region",
    "table_name",
    "bucket_name",
    "dynamodb",
    "table",
    "s3",
]


