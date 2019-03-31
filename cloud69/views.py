from django.http import HttpResponse
from django.template import loader
import os
import boto3
import random
import string

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
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name="eu-west-2"
        )

    key_name = randomString()

    # create a file to store key locally
    outfile = open("{key_name}.pem".format(key_name=key_name), 'w')

    # call the boto ecw function to create a key pair
    key_pair = ec2.create_key_pair(KeyName=key_name)
    #
    # # capture the key and store it in a file
    KeyPairout = str(key_pair.key_material)
    outfile.write(KeyPairout)

    ec2.create_instances(
        ImageId="ami-09ead922c1dad67e4",
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName=key_name
    )

    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))

def delete_all(request):
    ec2 = boto3.resource(
        "ec2",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name="eu-west-2"
        )

    client = boto3.client(
        "ec2",
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name="eu-west-2"
    )

    ec2.instances.terminate()

    keypairs = client.describe_key_pairs()["KeyPairs"]
    for pair in keypairs:
        response = client.delete_key_pair(
            KeyName=pair['KeyName'],
        )

    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))



def randomString(stringLength=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
