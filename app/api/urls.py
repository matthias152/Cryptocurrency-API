from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from api.views import (
    WalletIDViewSet,
    BalanceViewSet,
    CryptoCurrencyViewSet,
    TransactionViewSet,
    CryptoCurrencyBuyViewSet,
    CryptoCurrencySellViewSet,
)


router = DefaultRouter()
router.register('walletid', WalletIDViewSet)
router.register('balance', BalanceViewSet)
router.register('cryptocurrency', CryptoCurrencyViewSet)
router.register('cryptocurrencybuy', CryptoCurrencyBuyViewSet)
router.register('cryptocurrencysell', CryptoCurrencySellViewSet)
router.register('transactions', TransactionViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
