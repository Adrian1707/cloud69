from django.http import HttpResponse
from django.template import loader, Context
from cloud69.cloud_formation_client import *
from cloud69.models import *
import json
import boto3
import pdb

def index(request):
    # stacks = CloudFormationClient().get_stacks()
    stacks = {
        "StackSummaries": [
            {
                "StackName": "Quote API",
            },
            {
                "StackName": "Pricing API",
            },
            {
                "StackName": "Pricing Admin",
            },
            {
                "StackName": "Dify",
            },
            {
                "StackName": "Batching",
            },
            {
                "StackName": "Microservice Authenticator",
            }
        ]
    }
    template = loader.get_template('cloud69/index.html')

    html = template.render({'stacks': stacks["StackSummaries"] }, request)
    return HttpResponse(html)

def new_stack(request):
    template = loader.get_template("cloud69/new_stack.html")
    return HttpResponse(template.render({"ec2_instance_types": ec2_instance_types, "db_instance_types": db_instance_types}, request))

def delete_stack(request):
    name = request.POST.dict().get("stack_name")
    CloudFormationClient().delete_stack(name)
    template = loader.get_template("cloud69/delete.html")
    return HttpResponse(template.render({}, request))

def create_stack(request):
    CloudFormationClient().create_stack(request.POST.dict())
    template = loader.get_template("cloud69/success.html")
    return HttpResponse(template.render({}, request))

def ec2_instance_types():
    return ["t1.micro", "t2.nano", "t2.micro", "t2.small", "t2.medium", "t2.large", "m1.small", "m1.medium", "m1.large", "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge", "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge", "m4.large", "m4.xlarge", "m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "c1.medium", "c1.xlarge", "c3.large", "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge", "c4.large", "c4.xlarge", "c4.2xlarge", "c4.4xlarge", "c4.8xlarge", "g2.2xlarge", "g2.8xlarge", "r3.large", "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge", "i2.xlarge", "i2.2xlarge", "i2.4xlarge", "i2.8xlarge", "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge", "hi1.4xlarge", "hs1.8xlarge", "cr1.8xlarge", "cc2.8xlarge", "cg1.4xlarge"]

def db_instance_types():
    return ["db.t1.micro", "db.m1.small", "db.m1.medium", "db.m1.large", "db.m1.xlarge", "db.m2.xlarge", "db.m2.2xlarge", "db.m2.4xlarge", "db.m3.medium", "db.m3.large", "db.m3.xlarge", "db.m3.2xlarge", "db.m4.large", "db.m4.xlarge", "db.m4.2xlarge", "db.m4.4xlarge", "db.m4.10xlarge", "db.r3.large", "db.r3.xlarge", "db.r3.2xlarge", "db.r3.4xlarge", "db.r3.8xlarge", "db.m2.xlarge", "db.m2.2xlarge", "db.m2.4xlarge", "db.cr1.8xlarge", "db.t2.micro", "db.t2.small", "db.t2.medium", "db.t2.large"]
