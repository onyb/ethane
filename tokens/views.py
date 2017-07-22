from django.shortcuts import render
from rest_framework import generics

from .models import Token
from .serializers import TokenSerializer


def token_distribution(request):
    return render(request, 'tokens/token_distribution.html')


class TokenAPIView(generics.RetrieveAPIView):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    lookup_field = 'symbol'
