from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member_id = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.member_id})"
# Create your models here.


class SavingsAccount(models.Model):
    ACCOUNT_TYPES = [
        ('REG', 'Regular Savings'),
        ('FIX', 'Fixed Deposit'),
        ('TAR', 'Target Savings'),
    ]

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=3, choices=ACCOUNT_TYPES)
    current_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=0)
    interest_rate = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.5)
    created_at = models.DateTimeField(auto_now_add=True)


def get_absolute_url(self):
    return reverse('account_detail', kwargs={'pk': self.pk})


def get_account_type_display(self):
    return dict(self.ACCOUNT_TYPES)[self.account_type]


def __str__(self):
    return f"{self.account_number} ({self.get_account_type_display()})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('DEP', 'Deposit'),
        ('WTH', 'Withdrawal'),
        ('INT', 'Interest'),
    ]

    account = models.ForeignKey(
        SavingsAccount, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    transaction_type = models.CharField(
        max_length=3, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_transaction_type_display()} of ${self.amount}"
