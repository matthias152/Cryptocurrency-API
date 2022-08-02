from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from datetime import date, datetime


def create_test_user():
    user = get_user_model().objects.create_user(
        'testuser',
        'test@example.com',
        'testpass123',
    )
    return user


class ModelTests(TestCase):
    def test_create_walletid(self):
        user = create_test_user()

        walletid = models.WalletID.objects.create(
            user=user,
            walletid='justatestwalletid'
        )

        self.assertEqual(str(walletid), walletid.walletid)

    def test_create_balance(self):
        user = create_test_user()

        balance = models.Balance.objects.create(
            user=user,
            balance='120.50'
        )

        self.assertEqual(str(balance), 'testuser balance')
        self.assertEqual(float(120.5), float(balance.balance))

    def test_create_cryptocurrency(self):
        user = create_test_user()
        walletid = models.WalletID.objects.create(
            user=user,
            walletid='justatestwalletid'
        )

        cryptocurrency = models.CryptoCurrency.objects.create(
            user=user,
            walletid=walletid,
            name='Bitcoin',
            quantity='0.523'
        )
        
        self.assertEqual(cryptocurrency.walletid, walletid)

    def test_create_transaction(self):
        user = create_test_user()
        walletid = models.WalletID.objects.create(
            user=user,
            walletid='justatestwalletid'
        )
        cryptocurrency = models.CryptoCurrency.objects.create(
            user=user,
            walletid=walletid,
            name='Ethereum',
            quantity=20,
        )
        today = date.today()
        curr_time = datetime.now().time()

        transaction = models.Transaction.objects.create(
            user=user,
            walletid=walletid,
            cryptocurrency=cryptocurrency,
            day_created=today,
            time_created=curr_time,
            type='sell',
            quantityCrypto=30.5,
            price=20.42,
        )

        self.assertEqual(transaction.walletid.walletid, 'justatestwalletid')
