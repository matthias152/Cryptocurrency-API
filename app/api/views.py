from jsonschema import ValidationError
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import (
    WalletID,
    Balance,
    CryptoCurrency,
    Transaction,
)

from api.serializers import (
    WalletIDSerializer,
    BalanceSerializer
)
import random, string


class WalletIDViewSet(viewsets.ModelViewSet):
    serializer_class = WalletIDSerializer
    queryset = WalletID.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    #  if there is an walletid, it wont save new one
    def perform_create(self, serializer):
        random_walletid = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=35))
        queryset = WalletID.objects.filter(user=self.request.user)
        
        if queryset.exists():
            raise ValidationError('You already have an WalletID.')

        serializer.save(user=self.request.user, walletid=random_walletid)
        

class BalanceViewSet(viewsets.ModelViewSet):
    serializer_class = BalanceSerializer
    queryset = Balance.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'patch']

    def perform_create(self, serializer):
        queryset = Balance.objects.filter(user=self.request.user)

        if queryset.exists():
            raise ValidationError('User can have only one balance.')

        serializer.save(user=self.request.user)