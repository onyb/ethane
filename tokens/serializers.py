from rest_framework import serializers

from .models import Token


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token

        fields = ('public_name', 'symbol', 'cap', 'rate', 'ico_start_date',
                  'ico_end_date', 'contract_address', 'token_type', 'phase',
                  'eth_raised', 'token_address',)