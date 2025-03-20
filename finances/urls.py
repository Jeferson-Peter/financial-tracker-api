from rest_framework.routers import DefaultRouter
from .views import AccountTypeViewSet, AccountViewSet, CategoryViewSet, TransactionViewSet

router = DefaultRouter()
router.register('account-types', AccountTypeViewSet, basename='accounttype')
router.register('accounts', AccountViewSet, basename='account')
router.register('categories', CategoryViewSet, basename='category')
router.register('transactions', TransactionViewSet, basename='transaction')

urlpatterns = router.urls
