from django.contrib import admin
from core import models

# Register your models here.
admin.site.register(models.Balance)
admin.site.register(models.WalletID)
admin.site.register(models.CryptoCurrency)
admin.site.register(models.Transaction)