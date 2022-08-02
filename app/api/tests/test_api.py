from venv import create
from django.contrib.auth import get_user_model
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient


from django.urls import reverse


# URL = 'http://127.0.0.1:8000/api/walletid/'
URL_WALLETID = reverse('walletid-list')
URL_BUYCRYPTO = 'http://127.0.0.1:8000/api/cryptocurrencybuy/'


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicWalletIDTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(URL_WALLETID)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class PrivateWalletIDTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@exmaple.com', username='user', password='testpsw123')
        self.client.force_authenticate(self.user)

    def test_create_walletid(self):
        res = self.client.post(URL_WALLETID)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


#  problems with transactions
# class PrivateCryptoCurrencyTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = create_user(email='user2@example.com', username='user', password='testpsw123')
#         self.admin = User.objects.create_superuser('matt', 'matt@example.com', '1234')
#         self.balance = Balance.objects.create(user=self.user, balance=30000)
#         self.walletid = WalletID.objects.create(user=self.user)
#         self.client.force_authenticate(self.user)

#     def test_buy_crypto(self):
#         data = {
#             'user': 1,
#             'walletid': self.walletid.id,
#             'name': 'stellar',
#             'quantity': 1,
#             }
#         res = self.client.post(URL_BUYCRYPTO, data)

#         self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class RegistrationTests(TestCase):
    def setUp(self):
        self.url = reverse("register")

    def test_registration(self):
        data = {"username": "testcase","password": "some_strong_psW1",
                "password2": "some_strong_psW1",
                "email": "test@gmail.com",
                "first_name": "Matthew", "last_name": "Mattest"}
        request = self.client.post(self.url, data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)




