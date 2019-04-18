from django.http import HttpResponse
from django.template import loader, Context
from cloud69.ec2_client import *
from cloud69.models import *
import json
import pdb

def index(request):
    instances = EC2Client().get_instances()
    template = loader.get_template('cloud69/index.html')
    instance_models = []
    for instance in instances:
        if instance['State']["Name"] != 'terminated':
            instance_models.append(EC2Instance.create(instance_response = instance))

    html = template.render({'instance_models': instance_models }, request)
    return HttpResponse(html)

def create(request):
    EC2Client().create_ec2_instance()
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))

def delete(request):
    instance_id = request.POST.dict().get("instance_id")
    EC2Client().delete_instance(instance_id)
    template = loader.get_template("cloud69/success.html")
    return HttpResponse(template.render({}, request))

def delete_all(request):
    EC2Client().delete_all_ec2_instances()
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))

def new_stack(request):
    json_string = open("/code/cloud69/static/cloud69/rails_stack.json").read()
    json_string = json_string.replace('{github_url}', "https://github.com/Adrian1707/todo_list")
    json_string = json_string.replace('{app_name}', "https://github.com/Adrian1707/todo_list".split("/")[-1])
    cloud_formation_template_dict = json.loads(json_string)
    template = loader.get_template("cloud69/new_stack")
    return HttpResponse(template.render({}, request))

def create_stack(request):
    github_url = request.POST.dict().get("github_url")
    cloud_formation_template_dict = open('/static/rails_stack.json').read()
    json.dumps(data)
