from json import loads, dumps
from optparse import make_option
from StringIO import StringIO

from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('-c', '--country',
                    dest='country',
                    help='country',
                    metavar='COUNTRY'),)


    def handle(self, *args, **kwargs):
        country = kwargs['country']
        response = StringIO()
        call_command('dumpdata', stdout=response)
        response.seek(0)
        data = filter(lambda x: x['model'].startswith('flis'),
                   loads(response.read()))
        for item in data:
            item['fields']['country'] = country
        print dumps(data, indent=4)