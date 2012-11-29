"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from nationwidefinance.referrals import tasks
from nationwidefinance.referrals import facebook


class CeleryTests(TestCase):

    def test_post_to_facebook(self):
        
    	tasks.post_to_facebook()
    	self.assertEqual('1','2')




