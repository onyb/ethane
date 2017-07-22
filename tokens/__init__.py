from django.conf import settings

from web3 import Web3, KeepAliveRPCProvider

__all__ = ('web3',)

web3 = Web3(
    KeepAliveRPCProvider(host=settings.ETHEREUM_NODE_HOST,
                         port=settings.ETHEREUM_NODE_PORT)
)
