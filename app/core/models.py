from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Balance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(blank=True)

    def __str__(self):
        return f'{self.user} balance'


class WalletID(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    walletid = models.CharField(max_length=35, blank=True)

    def __str__(self):
        return self.walletid


class CryptoCurrency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    walletid = models.ForeignKey(WalletID, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    quantity = models.FloatField()


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    walletid = models.ForeignKey(WalletID, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE)
    day_created = models.DateField()
    time_created = models.TimeField()
    type = models.CharField(max_length=30)
    quantityCrypto = models.FloatField()
    price = models.FloatField(blank=True, null=True)