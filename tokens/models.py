import os
import re
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from jinja2 import Template

from .conf import PHASES, TOKEN_TYPES


class Token(models.Model):
    public_name = models.CharField(max_length=200)

    contract_address = models.CharField(max_length=42, default='0x')

    symbol = models.CharField(max_length=4)

    decimals = models.IntegerField(
        default=18,
        validators=[MaxValueValidator(20), MinValueValidator(0)]
    )

    phase = models.CharField(
        max_length=8,
        choices=PHASES,
        blank=True
    )

    cap = models.IntegerField(
        blank=True, null=True
    )

    token_type = models.CharField(
        max_length=20,
        choices=TOKEN_TYPES,
        blank=True
    )

    start_block_offset = models.IntegerField(
        default=2,
        validators=[MinValueValidator(1)]
    )

    end_block_offset = models.IntegerField(
        default=300,
        validators=[MinValueValidator(300)]
    )

    rate = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0)]
    )

    ico_start_date = models.DateTimeField(blank=True, null=True)
    ico_end_date = models.DateTimeField(blank=True, null=True)

    @property
    def class_name(self):
        return ''.join(
            map(lambda s: s.title(), self.public_name.split())
        )

    def get_contract_address(self):
        out = subprocess.check_output(
            ['npm', 'run', 'networks'],
            cwd=os.path.join(settings.BASE_DIR, 'core')
        )

        return re.search(
            r'{}Crowdsale: ([A-z\d]+)'.format(self.class_name),
            out.decode()
        ).group(1)

    def clean(self):
        now = timezone.now()

        if not self.ico_start_date:
            self.ico_start_date = now

        if now < self.ico_start_date:
            self.phase = 'PHASE_01'
        elif not self.ico_end_date or now < self.ico_end_date:
            self.phase = 'PHASE_02'
        elif now > self.ico_end_date:
            self.phase = 'PHASE_03'

        if not self.cap:
            self.token_type = TOKEN_TYPES[1][0]

    def save(self, *args, **kwargs):
        self.clean()

        self.generate_contracts()
        self.generate_migration()

        self.compile()
        self.deploy()

        self.contract_address = self.get_contract_address()

        super().save(*args, **kwargs)

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
            'TOKEN_START_BLOCK_OFFSET': self.start_block_offset,
            'TOKEN_END_BLOCK_OFFSET': self.end_block_offset,
            'ETH_TO_TOKEN_RATE': self.rate
        }

        last_migration = sorted(
            f
            for f in os.listdir(settings.SOLIDITY_MIGRATIONS_DIR)
            if os.path.isfile(os.path.join(settings.SOLIDITY_MIGRATIONS_DIR, f))
        ).pop()

        migration_data = open(
            os.path.join(settings.SOLIDITY_MIGRATIONS_DIR,
                         last_migration),
            'r'
        ).read()

        last_idx = int(re.match('\d+', last_migration).group())

        in_fname = os.path.join(settings.SOLIDITY_TEMPLATES_DIR, 'TokenMigration.js.in')
        out_fname = os.path.join(
            settings.SOLIDITY_MIGRATIONS_DIR,
            '{}_deploy_{}.js'.format(last_idx + 1, self.class_name.lower())
        )

        with open(in_fname, 'r') as in_f:
            out = Template(in_f.read()).render(**context)
            if out == migration_data:
                return False
            else:
                with open(out_fname, 'w') as out_f:
                    out_f.write(out)
                    return True

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
