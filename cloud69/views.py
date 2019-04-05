from django.http import HttpResponse
from django.template import loader
from cloud69.ec2_client import *
import pdb

def index(request):
    template = loader.get_template('cloud69/index.html')
    return HttpResponse(template.render({}, request))

def create(request):
    EC2Client().create_ec2_instance()
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))

def delete_all(request):
    EC2Client().delete_all_ec2_instances()
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))



