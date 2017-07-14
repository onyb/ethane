import os

from django.core.management.base import BaseCommand, CommandError
from jinja2 import Template

from settings import CONTRACTS_DIR
from ...models import Token


class Command(BaseCommand):
    help = 'Generate Solidity contracts for a Token in the database'

    def add_arguments(self, parser):
        parser.add_argument('token', type=int)

    def handle(self, *args, **options):
        token_pk = options['token']
        try:
            token = Token.objects.get(pk=token_pk)
        except Token.DoesNotExist:
            raise CommandError('Token "%s" does not exist' % token_pk)
        else:
            self.generate_token_contracts(token)

            self.stdout.write(
                self.style.SUCCESS('Successful: "%s"' % token_pk)
            )

    def generate_token_contracts(self, token):
        context = {
            'TOKEN_TYPE': token.token_type,
            'TOKEN_CLASS_NAME': token.class_name,
            'TOKEN_PUBLIC_NAME': token.public_name,
            'TOKEN_SYMBOL_NAME': token.symbol,
            'TOKEN_DECIMALS': token.decimals
        }

        in_fname = os.path.join(CONTRACTS_DIR, 'Token.sol.in')
        out_fname = os.path.join(CONTRACTS_DIR, token.class_name + '.sol')

        with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
            template = Template(in_f.read())
            out_f.write(template.render(**context))

        in_fname = os.path.join(CONTRACTS_DIR, 'Crowdsale.sol.in')
        out_fname = os.path.join(CONTRACTS_DIR,
                                 token.class_name + 'Crowdsale.sol')

        with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
            template = Template(in_f.read())
            out_f.write(template.render(**context))
