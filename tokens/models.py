import os
import re
import subprocess

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from jinja2 import Template

from .conf import PHASES


class Token(models.Model):
    public_name = models.CharField(max_length=200)

    symbol = models.CharField(max_length=4)

    decimals = models.IntegerField(
        default=18,
        validators=[MaxValueValidator(20), MinValueValidator(0)]
    )

    phase = models.CharField(
        max_length=8,
        choices=PHASES,
        default=PHASES[0][0],
    )

    token_type = models.CharField(
        max_length=20,
        default='MintableToken',
    )

    @property
    def class_name(self):
        return ''.join(
            map(lambda s: s.title(), self.public_name.split())
        )

    @property
    def contract_address(self):
        out = subprocess.check_output(
            ['npm', 'run', 'networks'],
            cwd=os.path.join(settings.BASE_DIR, 'core')
        )

        return re.search(
            r'{}Crowdsale: ([A-z\d]+)'.format(self.class_name),
            out.decode()
        ).group(1)

    def save(self, *args, **kwargs):
        self.generate_contracts()
        self.generate_migration()

        super().save(*args, **kwargs)

        self.compile()
        self.deploy()

    def generate_contracts(self):
        context = {
            'TOKEN_CLASS_NAME': self.class_name,
            'TOKEN_PUBLIC_NAME': self.public_name,
            'TOKEN_SYMBOL_NAME': self.symbol,
            'TOKEN_DECIMALS': self.decimals
        }

        in_fname = os.path.join(settings.SOLIDITY_TEMPLATES_DIR, 'Token.sol.in')
        out_fname = os.path.join(settings.SOLIDITY_CONTRACTS_DIR, self.class_name + '.sol')

        with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
            template = Template(in_f.read())
            out_f.write(template.render(**context))

        in_fname = os.path.join(settings.SOLIDITY_TEMPLATES_DIR, 'Crowdsale.sol.in')
        out_fname = os.path.join(settings.SOLIDITY_CONTRACTS_DIR,
                                 self.class_name + 'Crowdsale.sol')

        with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
            template = Template(in_f.read())
            out_f.write(template.render(**context))

    def generate_migration(self):
        context = {
            'TOKEN_CLASS_NAME': self.class_name,
            'TOKEN_PUBLIC_NAME': self.public_name,
            'TOKEN_SYMBOL_NAME': self.symbol,
            'TOKEN_DECIMALS': self.decimals
        }

        migration = sorted(
            f
            for f in os.listdir(settings.SOLIDITY_MIGRATIONS_DIR)
            if os.path.isfile(os.path.join(settings.SOLIDITY_MIGRATIONS_DIR, f))
        ).pop()

        idx = int(re.match('\d+', migration).group()) + 1

        in_fname = os.path.join(settings.SOLIDITY_TEMPLATES_DIR, 'TokenMigration.js.in')
        out_fname = os.path.join(
            settings.SOLIDITY_MIGRATIONS_DIR,
            '{}_deploy_{}.js'.format(idx, self.class_name.lower())
        )

        with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
            template = Template(in_f.read())
            out_f.write(template.render(**context))

    def compile(self):
        return subprocess.check_output(
            ['npm', 'run', 'compile'],
            cwd=os.path.join(settings.BASE_DIR, 'core')
        )

    def deploy(self):
        return subprocess.check_output(
            ['npm', 'run', 'deploy'],
            cwd=os.path.join(settings.BASE_DIR, 'core')
        )
