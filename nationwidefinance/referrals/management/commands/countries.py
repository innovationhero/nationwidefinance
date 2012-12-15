from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from nationwidefinance.referrals.models import Country
from datetime import datetime
import csv

class Command(BaseCommand):
	def handle(self, excel_path, **options):
		dt = datetime.now()
		countries = csv.reader(open(excel_path, "rU"), delimiter=',',dialect=csv.excel_tab)
		for c in countries:
			print 'saving %s ' % c[0]
			country = Country()
			country.name = c[0]
			country.code = c[1]
			#country.entity_active = True
			#country.created_dt = dt
			#country.updated_dt = dt
			country.save()