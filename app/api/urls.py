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
    RegisterView,
)


router = DefaultRouter()
router.register('walletid', WalletIDViewSet)
router.register('balance', BalanceViewSet)
router.register('cryptocurrency', CryptoCurrencyViewSet)
router.register('cryptocurrencybuy', CryptoCurrencyBuyViewSet)
router.register('cryptocurrencysell', CryptoCurrencySellViewSet)
router.register('transaction', TransactionViewSet)

# app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
