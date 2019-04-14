from django.http import HttpResponse
from django.template import loader, Context
from cloud69.ec2_client import *
from cloud69.models import *
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



