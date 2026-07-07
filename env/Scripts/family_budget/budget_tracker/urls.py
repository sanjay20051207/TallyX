from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('budget/set/', views.set_budget_view, name='set_budget'),
    path('expense/add/', views.add_expense_view, name='add_expense'),
    path('expense/edit/<str:expense_id>/', views.edit_expense_view, name='edit_expense'),
    path('expense/delete/<str:expense_id>/', views.delete_expense_view, name='delete_expense'),
]