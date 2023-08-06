from .credentials import *
import boto3
import pymysql
import json

s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
)


def upload_file(file):
    filename = file.name
    s3_client.upload_fileobj(file, BUCKET_NAME, filename)
    s3_file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return s3_file_url
