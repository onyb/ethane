from django.core.management.base import BaseCommand, CommandError

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

        self.stdout.write(
            self.style.SUCCESS('Successful: "%s"' % token_pk)
        )
