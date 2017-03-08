import pprint

from digitaldiocese_worthers.api2 import Worthers
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        worthers = Worthers(options['api_id'], options['api_key'], options['diocese_id'])
        pprint.pprint(worthers.get_contacts(limit=1))

    def add_arguments(self, parser):
        parser.add_argument('api_id')
        parser.add_argument('api_key')
        parser.add_argument('diocese_id')
