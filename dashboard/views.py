from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView
from .models import SavingsAccount, Transaction
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.


class MemberDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    # ...

    def test_func(self):
        """Verify the user has a member profile"""
        return hasattr(self.request.user, 'member')

    def handle_no_permission(self):
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect('/create_member_profile/')


class MemberDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        member = getattr(self.request.user, 'member', None)
        if not member:
            return redirect('create_member_profile')

        # Get all accounts for the member
        accounts = member.accounts.all()

        # Calculate total savings
        total_savings = sum(account.current_balance for account in accounts)

        # Get recent transactions (last 5)
        recent_transactions = Transaction.objects.filter(
            account__in=accounts
        ).order_by('-created_at')[:5]

        context.update({
            'member': member,
            'accounts': accounts,
            'total_savings': total_savings,
            'recent_transactions': recent_transactions,
        })
        return context


class AccountDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = SavingsAccount
    template_name = 'accounts/account_detail.html'

    def test_func(self):
        account = self.get_object()
        return account.member.user == self.request.user
        # Ensure the member belongs to the logged-in user
