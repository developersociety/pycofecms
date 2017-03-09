import pprint

from django.core.management.base import BaseCommand

from digitaldiocese_worthers.api2 import Worthers


class Command(BaseCommand):

    def handle(self, *args, **options):
        worthers = Worthers(options['api_id'], options['api_key'], options['diocese_id'])
        result = worthers.get_contacts(
            limit=5,
        )
        pprint.pprint(result)
        result = worthers.get_contact(122604)
        pprint.pprint(result)
        result = worthers.get_deleted_contacts()
        pprint.pprint(result)
        result = worthers.get_contact_fields()
        pprint.pprint(result)

    def add_arguments(self, parser):
        parser.add_argument('api_id')
        parser.add_argument('api_key')
        parser.add_argument('diocese_id')
