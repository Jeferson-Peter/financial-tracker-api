from rest_framework.viewsets import ModelViewSet
from .models import AccountType, Account, Category, Transaction
from .serializers import AccountTypeSerializer, AccountSerializer, CategorySerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.exceptions import ValidationError


class AccountTypeViewSet(ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['is_default']
    search_fields = ['name']
    lookup_field = 'slug'

    def get_queryset(self):
        return AccountType.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        name = serializer.validated_data['name']

        if AccountType.objects.filter(user=user, name=name).exists():
            raise ValidationError({"detail": f"You already have an account type named '{name}'."})

        serializer.save(user=user)


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['account_type', 'balance']
    search_fields = ['account_type__name']

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transaction_type', 'account', 'category', 'date']

    def get_queryset(self):
        # Return only transactions for the authenticated user's accounts
        user = self.request.user
        return Transaction.objects.filter(account__user=user)