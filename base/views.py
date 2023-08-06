from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from .utils import *
import boto3
import json

# Create your views here.


def index(request):
    return render(request, "index.html")


def upload(request):
    if request.method == "POST":
        data = request.POST
        email_data = data.getlist("email-input")

        # email_data = request.form.getlist("email-input")
        print(email_data)
        emails = [email for email in email_data if email]
        print(emails)

        uploaded_file = request.FILES.get("image_file")
        url = upload_file(uploaded_file)
        filename = uploaded_file.name
        download_limit = len(emails)
        save_file_info(filename, url, download_limit)

        lambda_client = boto3.client(
            "lambda",
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_KEY,
            region_name=AWS_REGION,
        )
        # url = f"http://52.54.78.147/download?filename={filename}"
        url = f"http://127.0.0.1:8000/download?filename={filename}"

        lambda_payload = {"filename": filename, "emails": emails, "url": url}
        res = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps(lambda_payload),
        )

        if res["StatusCode"] == 200:
            return render(request, "submit.html")
        else:
            return HttpResponse("<h1>Something Went Wrong.</h1>")


def download(request):
    try:
        filename = request.GET.get("filename")
        data = get_file_data(filename=filename)
        if data:
            downloads = data[3]
            download_limit = data[2]
            url = data[1]

            if downloads >= download_limit:
                delete_s3_file(filename)
                return HttpResponse("<h1> The Download Limit has been reached. </h1>")

            downloads += 1
            update_db(filename, downloads)
            return redirect(url)

        else:
            return "<h1> File Not Found. </h1>"
    except Exception as err:
        # logging.error(str(err))
        return str(err)
