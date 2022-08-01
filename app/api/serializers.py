from rest_framework import serializers
from core.models import Balance, Transaction, CryptoCurrency, WalletID


class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ['id', 'user', 'walletid', 'name', 'quantity']
        ready_only_fields = ['id']


class WalletIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = WalletID
        fields = ['id', 'user', 'walletid']
        read_only_fields = ['id', 'user']


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['id', 'user', 'balance']
        read_only_fields = ['id', 'user']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ['id']