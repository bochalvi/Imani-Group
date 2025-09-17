from django.urls import path
from .views import MemberDashboardView, AccountDetailView

APP_NAME = 'dashboard'
urlpatterns = [
    path('dashboard/', MemberDashboardView.as_view(), name='member_dashboard'),
    path('accounts/<int:pk>/', AccountDetailView.as_view(), name='account_detail'),
]
