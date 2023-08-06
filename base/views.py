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

        emails = [email for email in email_data if email]

        uploaded_file = request.FILES.get("image_file")
        url = upload_file(uploaded_file)
        filename = uploaded_file.name

        lambda_client = boto3.client("lambda", region_name=AWS_REGION)

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
