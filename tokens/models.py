import json
import os
import subprocess

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from . import web3
from .utils import generate_migration, generate_contracts


class Token(models.Model):
    public_name = models.CharField(max_length=200)

    symbol = models.CharField(max_length=4)

    decimals = models.IntegerField(
        default=18, validators=[MaxValueValidator(20), MinValueValidator(0)]
    )

    cap = models.IntegerField(blank=True, null=True)

    start_block_offset = models.IntegerField(
        default=2, validators=[MinValueValidator(1)]
    )

    end_block_offset = models.IntegerField(
        default=300, validators=[MinValueValidator(300)]
    )

    rate = models.FloatField(
        default=1.0, validators=[MinValueValidator(0.0)]
    )

    ico_start_date = models.DateTimeField()
    ico_end_date = models.DateTimeField()

    @property
    def class_name(self):
        return ''.join(
            map(lambda s: s.title(), self.public_name.split())
        )

    @property
    def crowdsale_class_name(self):
        return self.class_name + self.token_type + 'Crowdsale'

    @property
    def crowdsale_meta(self):
        meta_json_path = os.path.join(
            settings.SOLIDITY_ABI_DIR,
            '{}.json'.format(self.crowdsale_class_name)
        )

        if not os.path.exists(meta_json_path):
            return {}
        else:
            with open(meta_json_path) as f:
                return json.load(f)

    @property
    def crowdsale_abi(self):
        return self.crowdsale_meta.get('abi')

    @property
    def contract_address(self):
        if not self.pk:
            return '-'

        networks = self.crowdsale_meta.get('networks', {}).values()
        return sorted(networks, key=lambda n: n['updated_at'])[-1]['address']

    @property
    def token_type(self):
        return 'Capped' if self.cap else 'Uncapped'

    @property
    def wei_raised(self):
        contract = web3.eth.contract(address=self.contract_address, abi=self.crowdsale_abi)
        return contract.call().weiRaised()

    @property
    def eth_raised(self):
        if not self.pk:
            return '-'

        return web3.fromWei(self.wei_raised, 'ether')

    @property
    def token_address(self):
        if not self.pk:
            return '-'

        contract = web3.eth.contract(address=self.contract_address,
                                     abi=self.crowdsale_abi)
        return contract.call().token()

    @property
    def token_abi(self):
        return self.token_meta.get('abi')

    @property
    def token_meta(self):
        meta_json_path = os.path.join(
            settings.SOLIDITY_ABI_DIR,
            '{}.json'.format(self.class_name)
        )

        if not os.path.exists(meta_json_path):
            return {}
        else:
            with open(meta_json_path) as f:
                return json.load(f)

    @property
    def _cap_reached(self):
        if self.token_type == 'Uncapped':
            return False

        contract = web3.eth.contract(address=self.contract_address,
                                     abi=self.crowdsale_abi)
        return contract.call().hasEnded()

    @property
    def phase(self):
        if not self.pk:
            return '-'

        now = timezone.now()

        if now < self.ico_start_date:
            return 'UPCOMING'
        elif now < self.ico_end_date and not self._cap_reached:
            return 'ACTIVE'
        elif self._cap_reached or not self.cap:
            return 'COMPLETED'
        else:
            return 'FAILED'

    def get_balance_of(self, address):
        token = web3.eth.contract(address=self.token_address,
                                  abi=self.token_abi)

        return token.call().balanceOf(address) / self.decimals

    def buy(self, address, amount):
        contract = web3.eth.contract(address=self.contract_address,
                                     abi=self.crowdsale_abi)

        return contract.web3.eth.sendTransaction({
            'from': address, 'to': self.contract_address,
            'value': web3.toWei(amount, 'ether')
        })

    def save(self, *args, **kwargs):
        generate_contracts(self)
        generate_migration(self)

        self.compile()
        self.deploy()

        super().save(*args, **kwargs)

    def compile(self):
        return subprocess.check_call(
            ['truffle', 'compile'],
            cwd=os.path.join(settings.BASE_DIR, 'core')
        )

    def deploy(self):
        return subprocess.check_call(
            ['truffle', 'migrate'],
            cwd=os.path.join(settings.BASE_DIR, 'core')
        )
