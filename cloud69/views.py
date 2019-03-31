from django.http import HttpResponse
from django.template import loader
import os
import boto3


def index(request):
    client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )
    s3_buckets = client.list_buckets()["Buckets"]
    for bucket in s3_buckets:
        print(bucket["Name"])
    template = loader.get_template('cloud69/index.html')
    return HttpResponse(template.render({}, request))

def create(request):
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))
