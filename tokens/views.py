from django.shortcuts import render
from rest_framework import generics, mixins

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

import random

from .models import Token
from .serializers import TokenSerializer
from . import web3


def token_distribution(request):
    return render(request, 'tokens/token_distribution.html')


class TokenAPIView(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    renderer_classes = (JSONRenderer,)
    lookup_field = 'symbol'

    def post(self, request, *args, **kwargs):
        token = self.get_object()
        txn = token.buy(request.session['address'], request.data['eth'])
        return Response({'txn': txn})


class TokensCollectionView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EthereumAccountView(generics.GenericAPIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        address = request.session.get('address')

        if not address:
            address = request.session['address'] = random.choice(web3.eth.accounts)

        wei = web3.eth.getBalance(address)
        eth = web3.fromWei(wei, 'ether')

        content = {
            'address': address,
            'ETH': eth,
            'WEI': wei,
            'gasPrice': web3.eth.gasPrice,  # WEI
        }

        for token in Token.objects.all():
            content.update({
                token.symbol: token.get_balance_of(address)
            })

        return Response(content)
