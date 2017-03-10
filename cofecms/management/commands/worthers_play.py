import pprint

from django.core.management.base import BaseCommand

from cofecms.api import CofeCMS


class Command(BaseCommand):

    def handle(self, *args, **options):
        worthers = CofeCMS(options['api_id'], options['api_key'], options['diocese_id'])
        result = worthers.get_contacts(
            limit=10, search_params={'keyword': 'smith', 'keyword_names_only': 'on'},
            fields={'contact': ['forenames', 'surname']},
        )
        for row in result.all():
            self.stdout.write(pprint.pformat(row))

    def add_arguments(self, parser):
        parser.add_argument('api_id')
        parser.add_argument('api_key')
        parser.add_argument('diocese_id')
