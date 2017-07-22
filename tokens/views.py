from django.shortcuts import render
from rest_framework import generics, mixins

from .models import Token
from .serializers import TokenSerializer


def token_distribution(request):
    return render(request, 'tokens/token_distribution.html')


class TokenAPIView(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'symbol'


class TokensCollectionView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
