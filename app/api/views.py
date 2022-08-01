from crypt import crypt
from jsonschema import ValidationError
from rest_framework import (
    viewsets,
    mixins,
    status,
)

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from core.models import (
    WalletID,
    Balance,
    CryptoCurrency,
    Transaction,
)

from api.serializers import (
    WalletIDSerializer,
    BalanceSerializer,
    CryptoCurrencySerializer,
    TransactionSerializer,
)

import random, string, requests
from datetime import date, datetime
from django.urls import reverse_lazy, reverse
from pycoingecko import CoinGeckoAPI


coingecko = CoinGeckoAPI()
today = date.today()
time = datetime.now().time()

def get_coin_price(coin):
    coin_price = coingecko.get_price(ids=str(coin).lower(), vs_currencies='usd')[str(coin).lower()]['usd']
    return float(coin_price)


def create_transaction(day, time, type, quantity, price, user, walletid, crypto):
    url = 'http://127.0.0.1:8000/api/transactions/'
    # url = reverse('api:transaction-list')

    req = requests.post(url, data={
        'day_created': day,
        'time_created': time,
        'type': type,
        'quantityCrypto': quantity,
        'price': price,
        'user': user,
        'walletid': walletid,
        'cryptocurrency': crypto,
        }, auth=('matt', '1234'))

    return req


def try_get_user_crypto(user, name):
    try:
        user_crypto = CryptoCurrency.objects.get(user=user, name=name)
    except:
        user_crypto = False
    
    return user_crypto


class CryptoCurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoCurrencySerializer
    queryset = CryptoCurrency.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        auth_user = self.request.user

        data = serializer.validated_data
        cryptoname = data.get('name', None)
        quantity_send = data.get('quantity', None)
        receiver_user = data.get('user', None)

        sender_crypto = CryptoCurrency.objects.get(user=auth_user, name=cryptoname)

        # try:
        #     receiver_crypto = CryptoCurrency.objects.get(user=receiver_user, name=cryptoname)
        # except:
        #     receiver_crypto = False
        receiver_crypto = try_get_user_crypto(receiver_user, cryptoname)

        if sender_crypto.quantity < float(quantity_send):
            raise ValidationError("You cant send that amount. It's too much.")
        else:
            if receiver_crypto:
                create_transaction(today, time, "receive", quantity_send, 0, receiver_crypto.user.id, receiver_crypto.walletid.id, receiver_crypto.id)
                create_transaction(today, time, "send", quantity_send, 0, sender_crypto.user.id, sender_crypto.walletid.id, sender_crypto.id)
                receiver_crypto.quantity += quantity_send
                sender_crypto.quantity -= quantity_send
                sender_crypto.save()
                receiver_crypto.save()
                return
            create_transaction(today, time, "receive", quantity_send, 20, receiver_crypto.user.id, receiver_crypto.walletid.id, receiver_crypto.id)
            create_transaction(today, time, "receive", quantity_send, 20, sender_crypto.user.id, sender_crypto.walletid.id, sender_crypto.id)
            sender_crypto.quantity -= quantity_send
            sender_crypto.save()

            serializer.save()

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)


class CryptoCurrencyBuyViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoCurrencySerializer
    queryset = CryptoCurrency.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        auth_user = self.request.user

        auth_user_walletid = WalletID.objects.get(user=auth_user)
        data = serializer.validated_data

        cryptoname = data.get('name', None)
        quantity_buy = data.get('quantity', None)
        currency = get_coin_price(cryptoname)
        full_price = quantity_buy * currency

        crypto_buy = try_get_user_crypto(auth_user, cryptoname)
        balance = Balance.objects.get(user=auth_user)

        if full_price <= balance.balance and crypto_buy:
            create_transaction(today, time, "buy", quantity_buy, currency, auth_user_walletid.user.id, auth_user_walletid.id, crypto_buy.id)
            balance.balance -= full_price
            balance.save()
            crypto_buy.quantity += quantity_buy
            crypto_buy.save()
            return
        elif full_price <= balance.balance:
            balance.balance -= full_price
            balance.save()
            serializer.save()
            crypto_buy_after = try_get_user_crypto(auth_user, cryptoname)
            create_transaction(today, time, "buy", quantity_buy, currency, auth_user_walletid.user.id, auth_user_walletid.id, crypto_buy_after.id)
            return
        else:
            raise ValidationError("Not enough money")


class CryptoCurrencySellViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoCurrencySerializer
    queryset = CryptoCurrency.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']

    def perform_create(self, serializer):
        auth_user = self.request.user

        auth_user_walletid = WalletID.objects.get(user=auth_user)
        data = serializer.validated_data

        cryptoname = data.get('name', None)
        quantity_sell = data.get('quantity', None)
        currency = get_coin_price(cryptoname)
        full_price = quantity_sell * currency

        crypto_sell = try_get_user_crypto(auth_user, cryptoname)
        balance = Balance.objects.get(user=auth_user)

        if crypto_sell and crypto_sell.quantity >= quantity_sell:
            create_transaction(today, time, "sell", quantity_sell, currency, auth_user_walletid.user.id, auth_user_walletid.id, crypto_sell.id)
            balance.balance += full_price
            crypto_sell.quantity -= quantity_sell
            balance.save()
            crypto_sell.save()
        else:
            raise ValidationError("You dont have that amount of cryptocurrency.")


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

    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)
        

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
    
    def get_queryset(self):
        queryset = self.queryset
        return queryset.filter(user=self.request.user)

    
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()
    permission_classes = []
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [IsAdminUser]

        return super(TransactionViewSet, self).get_permissions()