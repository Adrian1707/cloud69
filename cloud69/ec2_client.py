import os
import random
import string
import boto3
import pdb
from django.db import models

class EC2Client(object):
    def __init__(self):
        self.client = self.ec2_client()
        self.resource = self.ec2_resource()

    def get_instances(self):
        response = self.client.describe_instances()
        return response["Reservations"][0]["Instances"]

    def create_ec2_instance(self):
        key_name = self.randomString()

        # create a file to store key locally
        outfile = open("{key_name}.pem".format(key_name=key_name), 'w')

        # call the boto ec2 function to create a key pair
        key_pair = self.resource.create_key_pair(KeyName=key_name)
        #
        # # capture the key and store it in a file
        KeyPairout = str(key_pair.key_material)
        outfile.write(KeyPairout)

        self.resource.create_instances(
            ImageId="ami-09ead922c1dad67e4",
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName=key_name
        )

    def delete_all_ec2_instances(self):
        self.resource.instances.terminate()

        keypairs = self.client.describe_key_pairs()["KeyPairs"]
        for pair in keypairs:
            response = self.client.delete_key_pair(
                KeyName=pair['KeyName'],
            )

    def ec2_resource(self):
        return boto3.resource(
            "ec2",
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name="eu-west-2"
            )

    def ec2_client(self):
        return boto3.client(
            "ec2",
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name="eu-west-2"
        )

    def randomString(self, stringLength=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))
