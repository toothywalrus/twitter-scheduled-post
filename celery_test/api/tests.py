"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

# from django.test import TestCase


# class SimpleTest(TestCase):
#     def test_basic_addition(self):
#         """
#         Tests that 1 + 1 always equals 2.
#         """
#         self.assertEqual(1 + 1, 2)

from .models import WebPage
import nose.tools as nt


class TestFruit(object):

    def setup(self):
        self.webpage = WebPage()
        self.webpage.html = "dfdf"
        self.webpage.url = "http://google.com"

    def test_html(self):
        nt.assert_equal(self.webpage.html, "dfdf")
        nt.assert_equal(self.webpage.location, "http://google.com")
