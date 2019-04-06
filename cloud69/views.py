from django.http import HttpResponse
from django.template import loader, Context
from cloud69.ec2_client import *
import pdb

def index(request):
    instances = EC2Client().get_instances()
    template = loader.get_template('cloud69/index.html')
    html = template.render({'instances': instances}, request)
    return HttpResponse(html)

def create(request):
    EC2Client().create_ec2_instance()
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))

def delete_all(request):
    EC2Client().delete_all_ec2_instances()
    template = loader.get_template('cloud69/success.html')
    return HttpResponse(template.render({}, request))



