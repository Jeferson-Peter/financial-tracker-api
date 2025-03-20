from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone


class AccountType(models.Model):
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_types')

    class Meta:
        unique_together = ('user', 'name')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"


class Account(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_type = models.OneToOneField('AccountType', on_delete=models.CASCADE)  # Ensures only one account per type
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'account_type')

    def __str__(self):
        return f"{self.account_type.name} - {self.balance}"


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name} (User: {self.user.username})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    )

    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} - {self.amount} on {self.date}"

    def save(self, *args, **kwargs):
        # Adjust the account balance based on transaction type
        if self.transaction_type == 'income':
            self.account.balance += self.amount
        elif self.transaction_type == 'expense':
            self.account.balance -= self.amount
        # Ensure balance is updated
        self.account.save()
        super().save(*args, **kwargs)

