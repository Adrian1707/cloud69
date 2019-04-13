from django.db import models
import pdb

# Create your models here.


class EC2Instance(models.Model):

    @classmethod
    def create(cls, instance_response):
        instance = cls(instance_response)
        instance.response = instance_response
        return instance

    def name(self):
        for tag in self.tags():
            if tag["Key"] == "Name":
                return tag["Value"]

    def instance_id(self):
        return self.response["InstanceId"]

    def tags(self):
        t = []
        for tag in self.response["Tags"]:
            t.append(tag)
        return t
