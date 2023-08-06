from .credentials import *
import boto3
import pymysql
import json

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


def get_file_data(filename):
    conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
    cur = conn.cursor()
    query = f"SELECT * FROM {TABLE_NAME} WHERE filename = '{filename}'"
    cur.execute(query)
    data = cur.fetchone()
    conn.close()
    return data


def update_db(filename, downloads):
    conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
    cur = conn.cursor()
    query = f"UPDATE {TABLE_NAME} SET downloads={downloads} WHERE filename='{filename}'"
    cur.execute(query)
    conn.commit()
    conn.close()


def delete_s3_file(filename):
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
    except Exception as e:
        print(f"Error deleting file: {e}")
    return True


def upload_file(file):
    filename = file.name
    s3_client.upload_fileobj(file, BUCKET_NAME, filename)
    s3_file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return s3_file_url


def save_file_info(filename, url, download_limit, downloads=0):
    """Save data into RDS"""
    conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
    cur = conn.cursor()
    query = "INSERT INTO harsh (filename, url, download_limit, downloads) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (filename, url, download_limit, downloads))
    conn.commit()
    conn.close()


def reset_db():
    conn = pymysql.connect(host=ENDPOINT, user=USR, password=PASSWORD, database=DBNAME)
    query = f"DELETE FROM {TABLE_NAME};"
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    reset_db()
    # data = get_file_data(filename="Screen Shot 2023-07-10 at 2.42.38 PM.png")
    # print(data)
