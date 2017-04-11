# TEST SCRIPT
from django.core.management.base import BaseCommand, CommandError
import requests

class Command(BaseCommand):
    help = "Scrapes the last 200 transactions at each service for shift drink-discounted transactions and extracts the employee ID"

    def handle(self, *args, **options):
        url = "http://192.168.33.15/endpoints/login"
        s = requests.Session()
        r = s.get(url)
        for key, value in s.cookies:
            print(key, value)
