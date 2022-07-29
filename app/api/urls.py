from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from api.views import WalletIDViewSet, BalanceViewSet


router = DefaultRouter()
router.register('walletid', WalletIDViewSet)
router.register('balance', BalanceViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls))
]
