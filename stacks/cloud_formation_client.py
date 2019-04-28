import os
import boto3
import pdb
import requests
from django.db import models

class CloudFormationClient(object):
    def __init__(self):
        self.client = self.cf_client()

    def get_stacks(self):
        return self.client.list_stacks(
            StackStatusFilter=['CREATE_COMPLETE', 'UPDATE_IN_PROGRESS', 'UPDATE_COMPLETE_CLEANUP_IN_PROGRESS', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_IN_PROGRESS']
        )

    def stack_parameters(self, stack_name):
        return self.client.describe_stacks(
            StackName=stack_name
        )["Stacks"][0]["Parameters"]

    def create_stack(self, params):
        json_string = open("/code/stacks/static/stacks/rails_stack.json").read()
        github_url = params.get("github_url")
        user_repo = github_url.split("github.com/")[-1]
        commit_sha = self.get_commit_sha(user_repo)
        app_name = github_url.split("/")[-1]
        self.client.create_stack(
            StackName=params.get("app_name"),
            TemplateBody=json_string,
            OnFailure='ROLLBACK',
            Parameters=self.params_list(params, github_url, commit_sha, app_name)
            )

    def update_stack(self, stack_name):
        json_string = open("/code/stacks/static/stacks/rails_stack.json").read()
        params = self.stack_parameters(stack_name)
        for param in params:
            if param["ParameterKey"] == "GithubUrl":
                github_url = param["ParameterValue"]
            if param["ParameterKey"] == "DBPassword":
                del param['ParameterValue']
                param["UsePreviousValue"] = True
            if param["ParameterKey"] == "DBUser":
                del param['ParameterValue']
                param["UsePreviousValue"] = True

        for param in params:
            if param["ParameterKey"] == "CommitSha":
                user_repo = github_url.split("github.com/")[-1]
                param["ParameterValue"] = self.get_commit_sha(user_repo)

        self.client.update_stack(
            StackName=stack_name,
            UsePreviousTemplate=True,
            Parameters=params
        )

    def delete_stack(self, name):
        self.client.delete_stack(StackName=name)

    def get_commit_sha(self, user_repo):
        response = requests.get("https://api.github.com/repos/{}/commits/master".format(user_repo))
        commit_sha = response.json()["sha"]
        return commit_sha

    def cf_client(self):
        return boto3.client(
            "cloudformation",
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name="eu-west-2"
        )

    def params_list(self, params, github_url, commit_sha, app_name):
        return [
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
                'ParameterKey': 'GithubUrl',
                'ParameterValue': github_url,
            },
            {
                'ParameterKey': 'CommitSha',
                'ParameterValue': commit_sha,
            },
            {
                'ParameterKey': 'AppName',
                'ParameterValue': app_name,
            },
            {
                'ParameterKey': 'RubyVersion',
                'ParameterValue': params.get("ruby_version"),
            },
            {
                'ParameterKey': 'InstanceType',
                'ParameterValue': params.get("ec2_type"),
            },
            {
                'ParameterKey': 'WebServerCapacity',
                'ParameterValue': params.get("web_server_capacity"),
            }
        ]
