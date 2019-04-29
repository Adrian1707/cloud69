from django.test import TestCase
from django.urls import reverse
from django.test import SimpleTestCase
import pdb

from . import views

class StacksRoutes(SimpleTestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/stacks/')
        self.assertEquals(response.status_code, 200)

    def test_home_page_content(self):
        response = self.client.get('/stacks/')
        self.assertContains(response, "New Application")

    def test_new_stack_page_status_code(self):
        response = self.client.get('/stacks/new')
        self.assertEquals(response.status_code, 200)

    def test_new_stack_page_content(self):
        response = self.client.get('/stacks/new')
        self.assertContains(response, "<title>Cloud69</title>")
