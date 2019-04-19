import os
import boto3
import pdb
from django.db import models

class CloudFormationClient(object):
    def __init__(self):
        self.client = self.cf_client()

    def create_stack(self, params):
        json_string = open("/code/cloud69/static/cloud69/rails_stack.json").read()
        github_url = params.get("github_url")
        app_name = github_url.split("/")[-1]
        json_string = json_string.replace('{github_url}', github_url)
        json_string = json_string.replace('{app_name}', app_name)
        self.client.create_stack(
            StackName=params.get("app_name"),
            TemplateBody=json_string,
            OnFailure='ROLLBACK',
            Parameters=[
                {
                    'ParameterKey': 'DBName',
                    'ParameterValue': params.get("db_name"),
                },
                {
                    'ParameterKey': 'DBUser',
                    'ParameterValue': params.get("db_user"),
                },
                {
                    'ParameterKey': 'DBPassword',
                    'ParameterValue': params.get("db_password"),
                },
                {
                    'ParameterKey': 'DBAllocatedStorage',
                    'ParameterValue': params.get("db_allocated_storage"),
                },
                {
                    'ParameterKey': 'DBInstanceClass',
                    'ParameterValue': params.get("db_type"),
                },
                {
                    'ParameterKey': 'InstanceType',
                    'ParameterValue': params.get("ec2_type"),
                },
                {
                    'ParameterKey': 'WebServerCapacity',
                    'ParameterValue': params.get("web_server_capacity"),
                }
            ])

    def cf_client(self):
        return boto3.client(
            "cloudformation",
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name="eu-west-2"
        )
