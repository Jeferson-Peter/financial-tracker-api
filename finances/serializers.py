from rest_framework import serializers
from .models import AccountType, Account, Category, Transaction


class AccountSerializer(serializers.ModelSerializer):
    account_type_name = serializers.CharField(source='account_type.name', read_only=True)  # Adiciona o nome do tipo de conta

    class Meta:
        model = Account
        fields = ['id', 'balance', 'account_type', 'account_type_name']  # Inclui o campo account_type_name

    def validate(self, attrs):
        user = self.context['request'].user
        account_type = attrs.get('account_type')
        account_id = self.instance.id if self.instance else None

        # Check if the user already has another account with the same type
        if Account.objects.filter(
                user=user, account_type=account_type
        ).exclude(id=account_id).exists():
            raise serializers.ValidationError(
                {"detail": f"You already have an account for '{account_type.name}'."}
            )
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Account.objects.create(**validated_data)

    def update(self, instance, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().update(instance, validated_data)

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'name', 'is_default', 'slug', 'description']

    def create(self, validated_data):
        return AccountType.objects.create(**validated_data)  # Save the instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

    def create(self, validated_data):
        # Assign the authenticated user automatically
        validated_data['user'] = self.context['request'].user
        return Category.objects.create(**validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        category_id = self.instance.id if self.instance else None  # ID da categoria sendo editada

        if Category.objects.filter(user=user, name=attrs['name']).exclude(id=category_id).exists():
            raise serializers.ValidationError({"detail": f"Category '{attrs['name']}' already exists."})
        return attrs


class TransactionSerializer(serializers.ModelSerializer):
    account_name = serializers.CharField(source="account.account_type.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Transaction
        fields = [
            "id",
            "account",
            "account_name",
            "amount",
            "transaction_type",
            "date",
            "description",
            "category",
            "category_name",
        ]

    def validate(self, attrs):
        if attrs['transaction_type'] == 'expense' and attrs['amount'] > attrs['account'].balance:
            raise serializers.ValidationError("Insufficient balance for this expense.")
        return attrs

    def create(self, validated_data):
        # Automatically assign the authenticated user if needed
        validated_data['account'].user = self.context['request'].user
        return super().create(validated_data)