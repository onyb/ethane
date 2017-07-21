import os
import re

from django.conf import settings
from jinja2 import Template


def generate_contracts(token):
    context = {
        'TOKEN_CLASS_NAME': token.class_name,
        'TOKEN_PUBLIC_NAME': token.public_name,
        'CROWDSALE_CLASS_NAME': token.crowdsale_class_name,
        'TOKEN_SYMBOL_NAME': token.symbol,
        'TOKEN_DECIMALS': token.decimals
    }

    in_fname = os.path.join(settings.SOLIDITY_TEMPLATES_DIR, 'Token.sol.in')
    out_fname = os.path.join(settings.SOLIDITY_CONTRACTS_DIR, token.class_name + '.sol')

    with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
        template = Template(in_f.read())
        out_f.write(template.render(**context))

    in_fname = os.path.join(
        settings.SOLIDITY_TEMPLATES_DIR, token.token_type + 'Crowdsale.sol.in'
    )
    out_fname = os.path.join(settings.SOLIDITY_CONTRACTS_DIR,
                             token.class_name + token.token_type + 'Crowdsale.sol')

    with open(in_fname, 'r') as in_f, open(out_fname, 'w') as out_f:
        template = Template(in_f.read())
        out_f.write(template.render(**context))


def generate_migration(token):
    context = {
        'TOKEN_CLASS_NAME': token.class_name,
        'TOKEN_TYPE': token.token_type,
        'CROWDSALE_CLASS_NAME': token.crowdsale_class_name,
        'TOKEN_START_BLOCK_OFFSET': token.start_block_offset,
        'TOKEN_END_BLOCK_OFFSET': token.end_block_offset,
        'ETH_TO_TOKEN_RATE': token.rate,
        'TOKEN_CAP': token.cap
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
        '{}_deploy_{}.js'.format(last_idx + 1, token.crowdsale_class_name.lower())
    )

    with open(in_fname, 'r') as in_f:
        out = Template(in_f.read()).render(**context)
        if out == migration_data:
            return False
        else:
            with open(out_fname, 'w') as out_f:
                out_f.write(out)
                return True
